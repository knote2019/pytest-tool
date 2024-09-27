import collections

import pytest
import torch
import torch.multiprocessing as mp

from test.common.testcase import TestCase

Parameters = collections.namedtuple('Parameters', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    Parameters(1, torch.float16, True),
    Parameters(2, torch.bfloat16, False),
]


class TestDDD(TestCase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def test_ddd(self, parameters):
        mp.spawn(self.te_linear, nprocs=parameters.tp_size, join=True)

    def te_linear(self, rank):
        self.init_process_group(self.parameters.tp_size, rank)
        print("kkk")
        self.destroy_process_group()
