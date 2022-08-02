import os

import pytest
import numpy as np
import numpy_serializer as nps
from numpy.lib.stride_tricks import sliding_window_view, broadcast_to

N = 10000
data = np.arange(N)

test_cases = [
    [sliding_window_view(data, N // 100), False],
    [broadcast_to(data, (100, N)), False],
    [broadcast_to(data, (100, N))[1::2, 1::2], False],
    [sliding_window_view(data, N // 100)[500::2], False],
    [data, True],
    [np.array([]), True],
    [data[1::2], True],
    [data.reshape(-1, 1, 1, 1, 1, 2, 2, 5), True],
    [data.reshape(-1, 1, 2, 2, 5).transpose([0, 2, 1, 4, 3])[::2], True],
    [sliding_window_view(
        sliding_window_view(
            broadcast_to(data, (100, N)), (N // 100, 1)).view(np.float64).squeeze()[1::2, 2::2].transpose(),
        (10, 100)).view(np.uint64)[1::1000], False],
]


@pytest.fixture(params=test_cases, scope="module")
def starting_point(request):
    data, old_behavior_expected = request.param
    new_file = '/tmp/new.bin'
    old_file = '/tmp/old.npy'

    nps.save(new_file, data)
    np.save(old_file, data)

    yield new_file, old_file, old_behavior_expected

    os.remove(new_file)
    os.remove(old_file)


def test_same(starting_point):
    new_file, old_file, _ = starting_point
    loaded1 = nps.load(new_file)
    loaded2 = np.load(old_file)
    assert np.array_equal(loaded1, loaded2)


def test_size(starting_point):
    new_file, old_file, old_behavior_expected = starting_point
    old_size, new_size = os.stat(old_file).st_size, os.stat(new_file).st_size
    assert (((not old_behavior_expected) and (old_size > new_size))
            or
            # If there's a difference, it's up serialization of `None` (up to 4 bytes)
            (old_behavior_expected and (old_size == new_size - 4)))
