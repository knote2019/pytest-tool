import torch


class GoldenTensor(torch.Tensor):
    @staticmethod
    def my_custom_method(x):
        return x.sum()
