import gc
import os

import pytest
import torch

from test.common.config import Config
from test.common.util import get_root_path, get_golden_root_path


class TestCaseBase:
    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        self.root_path = get_root_path()
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
        self.golden_path = f"{get_golden_root_path()}/{self.module_name}_{self.class_name}_{self.method_name}/{fields_and_values}"
        print(f"golden_path = {self.golden_path}")
        # create golden folder.
        os.makedirs(self.golden_path, exist_ok=True)

    def save_tensor(self, golden_file_name: str, tensor: torch.Tensor):
        file_name = f"{self.golden_path}/{golden_file_name}"
        print(f"save tensor to {file_name}")
        torch.save(tensor, file_name)

    def load_tensor(self, golden_file_name: str) -> torch.Tensor:
        file_name = f"{self.golden_path}/{golden_file_name}"
        print(f"load tensor from {file_name}")
        tmp = torch.load(file_name)
        return tmp

    def compare_tensor(self):
        if Config.golden_flag:
            pass
        pass

    def teardown_method(self, method):
        print(method)
        gc.collect()
        print(f"\n<<< <<< <<< [ {self.class_name} ][ {self.method_name} ] stop <<< <<< <<<")
