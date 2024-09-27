import os

import pynvml
import torch


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
# save_tensor.
# *******************************************************************************
def save_tensor(file_name: str, tensor: torch.Tensor):
    torch.save(tensor, file_name)


# *******************************************************************************
# load_tensor.
# *******************************************************************************
def load_tensor(file_name: str) -> torch.Tensor:
    return torch.load(file_name, weights_only=True)
