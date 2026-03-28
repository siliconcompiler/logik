# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os

import pytest
import siliconcompiler


@pytest.fixture
def setup_example_test(monkeypatch):
    """
    This file is cloned from Silicon Compiler.  We follow its convention
    for organizing CI tests with pytest, so that all testing can be done with
    similar efficiency.  See Silicon Compiler documentation for details
    """

    def setup(directory):
        cad_root = ebrick_fpga_cad_root()
        ex_dir = os.path.join(cad_root, "examples", directory)

        def _mock_show(chip, filename=None, screenshot=False):
            pass

        # pytest's monkeypatch lets us modify sys.path for this test only.
        monkeypatch.syspath_prepend(ex_dir)
        # Mock chip.show() so it doesn't run.
        monkeypatch.setattr(siliconcompiler.Project, "show", _mock_show)

        return ex_dir

    return setup


def ebrick_fpga_cad_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
