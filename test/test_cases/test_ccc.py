import collections

import pytest
import torch
import torch.multiprocessing as mp

from test.common.testcase import RankProcess
from test.common.testcase import TestCase

Parameters = collections.namedtuple('Parameters', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    Parameters(1, torch.float16, True),
    Parameters(2, torch.bfloat16, False),
]


class TestCCC(TestCase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def test_ccc(self, parameters):
        world_size = self.calculate_world_size(parameters)
        rank_process = TestCaseRankProcess(self, world_size, parameters)
        print(f"\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        mp.spawn(rank_process, nprocs=world_size, join=True)
        print(f"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")


class TestCaseRankProcess(RankProcess):
    def run(self, parameters):
        self.show(f"tp_size = {parameters.tp_size}")
        self.show(f"dtype = {parameters.dtype}")
        self.show(f"bias = {parameters.bias}")

        a = self.create_1d_tensor(5, parameters.dtype)
        b = self.create_1d_tensor(5, parameters.dtype)
        c = a + b

        self.show(a)
        self.show(b)
        self.show(c)

        self.compare_tensor("c", c)
