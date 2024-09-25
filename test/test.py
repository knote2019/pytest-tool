from collections import namedtuple

import pytest
import torch

from test.common.pytestcase import PyTestCase

ParameterTuple = namedtuple('ParameterTuple', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    ParameterTuple(1, torch.float16, True),
    ParameterTuple(2, torch.bfloat16, False),
]


class TestCase1(PyTestCase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def testcase(self, parameters):
        print(locals())
        tp_size = parameters.tp_size
        dtype = parameters.dtype
        bias = parameters.bias

        pass
