import enum
import os

import pynvml
import torch


class Precision(enum.Enum):
    LOW = 0
    MIDDLE = 1
    HIGH = 2


# *******************************************************************************
# get_root_path.
# *******************************************************************************
def get_root_path():
    return os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


# *******************************************************************************
# enable_golden.
# *******************************************************************************
def enable_golden() -> bool:
    pynvml.nvmlInit()
    gpu_name = pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0))
    return "NVIDIA" in gpu_name


# *******************************************************************************
# show_tensor.
# *******************************************************************************
def show_tensor(tensor: torch.Tensor):
    torch.set_printoptions(precision=4, sci_mode=False)
    print(tensor)
    torch.set_printoptions()


# *******************************************************************************
# show_tensor_full.
# *******************************************************************************
def show_tensor_full(tensor: torch.Tensor):
    torch.set_printoptions(precision=4, sci_mode=False, profile="full")
    print(tensor)
    torch.set_printoptions(profile="default")


# *******************************************************************************
# update_tensor_data.
# *******************************************************************************
def update_tensor_data(tensor_old: torch.Tensor, tensor_new: torch.Tensor):
    tensor_old.data.copy_(tensor_new)


# *******************************************************************************
# get_precision_rtol_atol.
# *******************************************************************************
def get_precision_rtol_atol(dtype: torch.dtype, precision: Precision) -> (float, float):
    if precision == Precision.LOW:
        if dtype == torch.float16:
            return 1e-1, 1e-0
        else:
            return 1e-1, 1e-0
    elif precision == Precision.MIDDLE:
        if dtype == torch.float16:
            return 1e-1, 1e-1
        else:
            return 1e-1, 1e-1
    elif precision == Precision.HIGH:
        if dtype == torch.float16:
            return 1e-2, 1e-2
        else:
            return 1e-2, 1e-2


# *******************************************************************************
# is_tensor_contains_nan_and_inf.
# *******************************************************************************
def is_tensor_contains_nan_and_inf(tensor: torch.Tensor) -> bool:
    check_nan: bool = torch.isnan(tensor).any().item() is True
    check_inf: bool = torch.isinf(tensor).any().item() is True
    return check_nan or check_inf


# *******************************************************************************
# compare_tensor_with_precision.
# *******************************************************************************
def compare_tensor_with_precision(expect_tensor: torch.Tensor, actual_tensor: torch.Tensor, expect_precision: Precision,
                                  expect_mismatch_percent: float = 0.0) -> bool:
    rtol, atol = get_precision_rtol_atol(expect_tensor.dtype, expect_precision)
    compare_result_tensor = torch.isclose(expect_tensor, actual_tensor, rtol=rtol, atol=atol, equal_nan=True)
    total_number = compare_result_tensor.numel()
    mismatched_number = total_number - int(torch.sum(compare_result_tensor))
    actual_mismatch_percent = float(mismatched_number / total_number)
    return actual_mismatch_percent <= expect_mismatch_percent


# *******************************************************************************
# save_tensor.
# *******************************************************************************
def save_tensor(file_name: str, tensor: torch.Tensor):
    torch.save(tensor, file_name)


# *******************************************************************************
# load_tensor.
# *******************************************************************************
def load_tensor(file_name: str) -> torch.Tensor:
    return torch.load(file_name, weights_only=True)
