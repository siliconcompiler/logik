# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import pytest

import siliconcompiler

from logik.demo.z1000 import z1000


@pytest.mark.skip(reason="need new cad tarballs from logiklib")
def test_file_paths():
    project = siliconcompiler.FPGA("test")
    project.set_fpga(z1000())
    project.set('option', 'builddir', '.')
    assert project.check_filepaths()
