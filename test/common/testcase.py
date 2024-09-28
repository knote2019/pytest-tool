import gc
import os

import pytest
import torch

from test.common.config import Config
from test.common.util import enable_golden
from test.common.util import load_tensor
from test.common.util import save_tensor


class TestCase:
    # *******************************************************************************
    # setup_method.
    # *******************************************************************************
    @pytest.fixture(autouse=True)
    def setup_method(self, request):
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

    def rank_process(self, rank, world_size, parameters):
        print(f"rank {rank} start !!!")
        torch.distributed.init_process_group("nccl", init_method='tcp://127.0.0.1:5678',
                                             world_size=world_size,
                                             rank=rank)
        torch.cuda.set_device(rank)
        torch.manual_seed(666 + rank)
        # ----------------------------
        torch.distributed.barrier()
        self.run(rank, parameters)
        torch.distributed.barrier()
        # ----------------------------
        torch.distributed.destroy_process_group()
        print(f"rank {rank} stop !!!")

    def run(self, rank: int, parameters):
        pass

    # *******************************************************************************
    # compare_tensor.
    # *******************************************************************************
    def compare_tensor(self, golden_file_name: str, actual_tensor: torch.Tensor, rank) -> bool:
        golden_file_path = f"{self.get_rank_golden_path(rank)}/{golden_file_name}"
        if enable_golden():
            print(f"save tensor from {golden_file_path}")
            save_tensor(golden_file_path, actual_tensor)
            return True
        else:
            print(f"load tensor from {golden_file_path}")
            expect_tensor = load_tensor(golden_file_path)
            return torch.allclose(actual_tensor, expect_tensor)

    def get_rank_golden_path(self, rank):
        class_golden_path = f"{Config.golden_root_path}/{self.module_name}.py/{self.class_name}"
        rank_golden_path = f"{class_golden_path}/{self.method_name}/{self.parameters_desc}/rank{rank}"
        print(f"rank_golden_path = {rank_golden_path}")
        if enable_golden():
            os.makedirs(rank_golden_path, exist_ok=True)
        return rank_golden_path

    # *******************************************************************************
    # raise_exception.
    # *******************************************************************************
    def raise_exception(self, msg):
        raise Exception(msg)

    # *******************************************************************************
    # teardown_method.
    # *******************************************************************************
    def teardown_method(self):
        gc.collect()
        torch.cuda.empty_cache()
        print(f"\n<<< <<< <<< [ {self.class_name} ][ {self.method_name} ] stop <<< <<< <<<")
