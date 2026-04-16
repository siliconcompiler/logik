#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import siliconcompiler
from logiklib.zeroasic.z1000 import z1000

from logik.flows.logik_vhdl_flow import LogikVHDLFlow


def hello_adder():
    # Create a Design object to hold source files and constraints.
    design = siliconcompiler.Design("adder")

    design.set_dataroot("adder_vhdl", __file__)
    with design.active_dataroot("adder_vhdl"):
        design.add_file("adder.vhd", fileset="rtl", filetype="vhdl")
        design.set_topmodule("adder", fileset="rtl")

    # Create an FPGA object with a -remote command line option
    project = siliconcompiler.FPGA.create_cmdline(switchlist=["-remote"])
    project.set_design(design)

    project.add_fileset("rtl")

    # Create an FPGA object and associate the design with it.
    fpga = z1000.z1000()

    # Load the specific FPGA part, which also sets the default flow and libraries.
    project.set_fpga(fpga)

    # Use the VHDL flow, which substitutes GHDL for the slang elaborate step.
    project.set_flow(LogikVHDLFlow())

    # Customize steps for this design
    project.option.set_quiet(True)

    # Run the compilation.
    project.run()

    # Display the results summary.
    project.summary()


if __name__ == "__main__":
    hello_adder()
