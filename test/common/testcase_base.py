import gc
import os

import pytest
import torch

from test.common.config import Config
from test.common.util import load_tensor
from test.common.util import save_tensor


class TestCaseBase:
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
        # case start.
        print(f"\n>>> >>> >>> [ {self.class_name} ][ {self.method_name} ] start >>> >>> >>>")
        print(f"class_name = {self.class_name}")
        print(f"method_name = {self.method_name}")
        print(f"parameters = {self.parameters}")
        # get string of parameters.
        fields_and_values = '-'.join(
            [f"{field}-{getattr(self.parameters, field)}" for field in self.parameters._fields])
        # set current case golden path.
        self.golden_path = f"{Config.golden_root_path}/{self.module_name}_{self.class_name}_{self.method_name}/{fields_and_values}"
        print(f"golden_path = {self.golden_path}")
        # create golden folder.
        os.makedirs(self.golden_path, exist_ok=True)

    # *******************************************************************************
    # compare_tensor.
    # *******************************************************************************
    def compare_tensor(self, golden_file_name: str, actual_tensor: torch.Tensor) -> bool:
        golden_file_path = f"{self.golden_path}/{golden_file_name}"
        if Config.enable_golden:
            print(f"save tensor from {golden_file_path}")
            save_tensor(golden_file_path, actual_tensor)
            return True
        else:
            print(f"load tensor from {golden_file_path}")
            expect_tensor = load_tensor(golden_file_name)
            torch.allclose(actual_tensor, expect_tensor)

    # *******************************************************************************
    # teardown_method.
    # *******************************************************************************
    def teardown_method(self, method):
        print(method)
        gc.collect()
        print(f"\n<<< <<< <<< [ {self.class_name} ][ {self.method_name} ] stop <<< <<< <<<")
