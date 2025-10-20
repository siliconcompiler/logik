# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import siliconcompiler

from data.z1000 import z1000


def test_file_paths():
    project = siliconcompiler.FPGA("test")
    project.set_fpga(z1000())
    project.set('option', 'builddir', '.')
    assert project.check_filepaths()
