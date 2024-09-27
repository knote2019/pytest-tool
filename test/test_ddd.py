import collections

import pytest
import torch
import torch.distributed as dist
import torch.multiprocessing as mp

from test.common.testcase import TestCase

Parameters = collections.namedtuple('Parameters', ['tp_size', 'dtype', 'bias'])
parameters_list = [
    Parameters(1, torch.float16, True),
    Parameters(2, torch.bfloat16, False),
]


def te_linear(rank, parameters):
    dist.init_process_group("nccl", init_method='tcp://127.0.0.1:5678', world_size=parameters.tp_size,
                                    rank=rank)
    print("kkk")
    torch.distributed.destroy_process_group()


class TestDDD(TestCase):
    @pytest.mark.parametrize("parameters", parameters_list)
    def test_ddd(self, parameters):
        world_size = parameters.tp_size
        mp.spawn(te_linear, args=(parameters,), nprocs=world_size)
