from collections import namedtuple

import pytest
import torch

from test.common.test_case import TestCaseBase

Parameters = namedtuple('Parameters', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    Parameters(1, torch.float16, True),
    Parameters(2, torch.bfloat16, False),
]


class TestCase1(TestCaseBase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def testcase1(self, parameters):
        print(parameters.tp_size)
        print(parameters.dtype)
        print(parameters.bias)

        a = torch.tensor([[0.1, 1.2], [3.4, 4.5], [6.7, 7.8]])
        print(a)
        self.save_tensor("a.pth", a)

        b = self.load_tensor("a.pth")
        print(b)
