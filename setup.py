#!/usr/bin/env python
import os
from itertools import chain

from setuptools import setup, find_namespace_packages

with open(os.path.normpath(os.path.join(__file__, '../numpy_serializer/VERSION'))) as f:
    version = f.read()

setup(name="np-serializer",
      version=version,
      author="Erez Zinman",
      description="A `numpy.ndarray` serializer that supports saving views in an optimized manner.",
      url="https://github.com/erezinman/np-serializer",
      packages=find_namespace_packages(include=['numpy_serializer*']),
      install_requires=['numpy'])
