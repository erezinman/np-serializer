import pickle
from typing import Union, IO

import numpy as np

from .utils import is_stream

from os import fspath, PathLike

DUMMY_ARRAY_INDICATOR = 'use_dummy'
VIEW_ARRAY_INDICATOR = 'use_view'


def save(file: Union[PathLike, IO, str], array: np.ndarray) -> None:
    if not is_stream(file):
        with open(file, 'wb') as f:
            save(f, array)
            return

    bases = []
    base = array
    while base is not None:
        bases.append(base)
        try:
            base = base.base
        except AttributeError:
            break

    best_base_idx = np.nanargmin([getattr(base, 'size', np.nan) for base in bases])

    base = bases[best_base_idx]
    np.save(file, base)

    if best_base_idx != 0:
        additional_metadata = {'shape': array.shape, 'strides': array.strides, 'dtype': str(array.dtype)}
        try:
            # In case when the "data" attribute is simple (all known cases, but not mandatory)
            additional_metadata['offset'] = (
                    array.__array_interface__['data'][0] - base.__array_interface__['data'][0])
        except (KeyError, IndexError):
            # In case it's not, copy the base, and then retry.
            base = np.copy(base)
            additional_metadata['offset'] = (
                    array.__array_interface__['data'][0] - base.__array_interface__['data'][0])
    else:
        additional_metadata = None

    pickle.dump(additional_metadata, file)


def load(file: Union[PathLike, IO, str]) -> np.ndarray:
    if not is_stream(file):
        with open(file, 'rb') as f:
            return load(f)

    base = np.load(file)
    additional_metadata: dict = pickle.load(file)

    if additional_metadata is None:
        return base

    return np.ndarray(shape=additional_metadata['shape'], dtype=additional_metadata['dtype'],
                      offset=additional_metadata['offset'], strides=additional_metadata['strides'], buffer=base)

