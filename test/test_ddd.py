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
        world_size = 2
        mp.spawn(self.rank_process, nprocs=world_size, args=(world_size,), join=True)

    def run(self, rank):
        print("run")
