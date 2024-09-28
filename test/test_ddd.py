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
    def test(self, parameters):
        world_size = self.calculate_world_size(parameters)
        mp.spawn(self.rank_process, nprocs=world_size, args=(world_size, parameters), join=True)

    def run(self, rank, parameters):
        print(f"tp_size = {parameters.tp_size}")
        print(f"dtype = {parameters.dtype}")
        print(f"bias = {parameters.bias}")
