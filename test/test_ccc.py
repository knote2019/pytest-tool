import collections

import pytest
import torch

from test.common.testcase import TestCase

Parameters = collections.namedtuple('Parameters', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    Parameters(1, torch.float16, True),
    Parameters(2, torch.bfloat16, False),
]


class TestCCC(TestCase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def test_ccc(self, parameters):
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
        self.raise_exception("compare failed !!!")
