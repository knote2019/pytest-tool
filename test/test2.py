import collections

import pytest
import torch

from test.common.testcase_base import TestCaseBase

Parameters = collections.namedtuple('Parameters', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    Parameters(1, torch.float16, True),
    Parameters(2, torch.bfloat16, False),
]


class TestCase2(TestCaseBase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def testcase1(self, parameters):
        print(parameters.tp_size)
        print(parameters.dtype)
        print(parameters.bias)

        a = torch.tensor([[0.1, 1.2], [3.4, 4.5], [6.7, 7.8]])
        b = torch.tensor([[0.1, 1.2], [3.4, 4.5], [6.7, 7.8]])
        c = a + b

        print(a)
        print(b)
        print(c)

        self.compare_tensor("c", c)
