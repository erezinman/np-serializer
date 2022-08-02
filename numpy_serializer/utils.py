from typing import Any
import io
from typing import IO


def is_stream(cls_or_self: Any) -> bool:
    """
    Checks if the given item or a class is a stream (e.g. any IO, or `open(...)`).

    Parameters
    ----------
    cls_or_self: instance or type
        The instance or type that might be a stream.

    Returns
    -------
    result: bool

    """

    if not isinstance(cls_or_self, type):
        cls_or_self = type(cls_or_self)
    return issubclass(cls_or_self, (IO, io.IOBase, io.RawIOBase, io.BufferedIOBase, io.TextIOBase))
