import gc
import os

import pytest
import torch

import test.common.util as util
from test.common.config import Config


class TestCase:
    # *******************************************************************************
    # setup_method.
    # *******************************************************************************
    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        print(f"\n\n===========================================================================================")
        # get context information.
        self.module_name = str(request.module.__name__)
        self.class_name = str(request.cls.__name__)
        self.method_name = str(request.node.originalname)
        self.parameters = request.node.callspec.params["parameters"]
        self.parameters_desc = '-'.join(
            [f"{field}-{getattr(self.parameters, field)}" for field in self.parameters._fields])
        # case start.
        print(f"\n>>> >>> >>> [ {self.class_name} ][ {self.method_name} ] start >>> >>> >>>")
        print(f"class_name = {self.class_name}")
        print(f"method_name = {self.method_name}")
        print(f"parameters_desc = {self.parameters_desc}")

    # *******************************************************************************
    # calculate_world_size.
    # *******************************************************************************
    def calculate_world_size(self, parameters):
        tp_size = 1
        cp_size = 1
        if hasattr(parameters, "tp_size"):
            tp_size = parameters.tp_size
        if hasattr(parameters, "cp_size"):
            cp_size = parameters.cp_size
        world_size = tp_size * cp_size
        print(f"{self.class_name}'s world_size = {world_size}")
        return world_size

    # *******************************************************************************
    # get_method_golden_path.
    # *******************************************************************************
    def get_method_golden_path(self):
        class_golden_path = f"{Config.golden_root_path}/{self.module_name}.py/{self.class_name}"
        method_golden_path = f"{class_golden_path}/{self.method_name}/{self.parameters_desc}"
        return method_golden_path

    # *******************************************************************************
    # teardown_method.
    # *******************************************************************************
    def teardown_method(self):
        gc.collect()
        print(f"\n<<< <<< <<< [ {self.class_name} ][ {self.method_name} ] stop <<< <<< <<<")


class RankProcess:
    def __init__(self, super_self, world_size, parameters):
        self.super_self = super_self
        self.world_size = world_size
        self.parameters = parameters
        self.rank = None

    def __call__(self, rank):
        self.rank = rank
        self.setup()
        self.run(self.parameters)
        self.teardown()

    # *******************************************************************************
    # setup.
    # *******************************************************************************
    def setup(self):
        print(f"rank-{self.rank}: start !!!")
        torch.distributed.init_process_group("nccl", init_method='tcp://127.0.0.1:5678',
                                             world_size=self.world_size,
                                             rank=self.rank)
        torch.cuda.set_device(self.rank)
        torch.manual_seed(666 + self.rank)

    # *******************************************************************************
    # run.
    # *******************************************************************************
    def run(self, parameters):
        self.raise_exception("need overwrite run()")

    # *******************************************************************************
    # create_tensor.
    # *******************************************************************************
    def create_1d_tensor(self, n: int, dtype: torch.dtype) -> torch.tensor:
        device = torch.device("cuda:{}".format(self.rank))
        return torch.randn(n).to(dtype).to(device) / 10

    def create_2d_tensor(self, h: int, w: int, dtype: torch.dtype) -> torch.tensor:
        device = torch.device("cuda:{}".format(self.rank))
        return torch.randn(h, w).to(dtype).to(device) / 10

    def create_3d_tensor(self, n: int, h: int, w: int, dtype: torch.dtype) -> torch.tensor:
        device = torch.device("cuda:{}".format(self.rank))
        return torch.randn(n, h, w).to(dtype).to(device) / 10

    # *******************************************************************************
    # show.
    # *******************************************************************************
    def show(self, obj):
        print(f"rank-{self.rank}: {obj}")

    # *******************************************************************************
    # compare_tensor.
    # *******************************************************************************
    def compare_tensor(self, golden_file_name: str, actual_tensor: torch.Tensor,
                       precision: util.Precision = util.Precision.HIGH,
                       expect_mismatch_percent: float = 0.0) -> bool:
        # check NAN or INF first.
        if util.is_tensor_contains_nan_and_inf(actual_tensor):
            self.raise_exception(f"tensor contains NAN or INF")

        rank_golden_path = f"{self.super_self.get_method_golden_path()}/rank-{self.rank}"
        golden_file_path = f"{rank_golden_path}/{golden_file_name}"
        if util.enable_golden():
            os.makedirs(rank_golden_path, exist_ok=True)
            print(f"save tensor to {golden_file_path}")
            util.save_tensor(golden_file_path, actual_tensor)
            return True
        print(f"load tensor from {golden_file_path}")
        expect_tensor = util.load_tensor(golden_file_path)
        # raise exception when check failed.
        if not util.compare_tensor_with_precision(expect_tensor, actual_tensor, precision, expect_mismatch_percent):
            self.show(f"compare with {golden_file_path} failed !!!")
            self.raise_exception(f"compare with {golden_file_path} failed !!!")

    # *******************************************************************************
    # raise_exception.
    # *******************************************************************************
    def raise_exception(self, msg):
        self.clean_resource()
        raise Exception(msg)

    # *******************************************************************************
    # teardown.
    # *******************************************************************************
    def teardown(self):
        self.clean_resource()
        print(f"rank-{self.rank}: stop !!!")

    # *******************************************************************************
    # clean_resource.
    # *******************************************************************************
    def clean_resource(self):
        torch.cuda.empty_cache()
        torch.distributed.destroy_process_group()
        self.show(f"resource cleaned !!!")
