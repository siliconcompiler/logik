# Copyright 2025 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os
import subprocess

import pytest


@pytest.mark.timeout(360)
def test_py(setup_example_test, monkeypatch):
    picorv32_dir = setup_example_test('picorv32')

    monkeypatch.chdir(picorv32_dir)

    import picorv32
    picorv32.build()


@pytest.mark.timeout(360)
def test_cli(setup_example_test):
    picorv32_dir = setup_example_test('picorv32')

    proc = subprocess.run([os.path.join(picorv32_dir, 'picorv32.py')], cwd=picorv32_dir)
    assert proc.returncode == 0
