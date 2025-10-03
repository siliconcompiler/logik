# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import siliconcompiler

from logik.demo.z1000 import z1000


def test_file_paths(part):
    project = siliconcompiler.FPGA("test")
    project.set_fpga(z1000())

    assert project.check_filepaths()
