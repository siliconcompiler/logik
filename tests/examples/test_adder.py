# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import os
import subprocess

import pytest


@pytest.mark.timeout(300)
def test_py(setup_example_test, monkeypatch):
    adder_dir = setup_example_test('adder')

    monkeypatch.chdir(adder_dir)
    # create_cmdline() parses sys.argv directly; without this, pytest's own
    # arguments (e.g. -v matching argparse's -version prefix) cause it to exit.
    monkeypatch.setattr('sys.argv', ['adder.py'])

    import adder
    adder.hello_adder()


@pytest.mark.timeout(300)
def test_cli(setup_example_test):
    adder_dir = setup_example_test('adder')

    proc = subprocess.run([os.path.join(adder_dir, 'adder.py')], cwd=adder_dir)
    assert proc.returncode == 0
