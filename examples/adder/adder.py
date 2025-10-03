#!/usr/bin/env python3

# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import siliconcompiler

from logik.flows import logik_flow

from logik.demo import z1000


def hello_adder():
    # 1. Create a Design object to hold source files and constraints.
    design = siliconcompiler.Design('adder')

    design.add_file('adder.v', fileset="rtl")
    design.set_topmodule('adder', fileset="rtl")

    # 2. Create an FPGA object
    project = siliconcompiler.FPGA(design)

    project.add_fileset('rtl')

    # 2. Create an FPGA object and associate the design with it.
    fpga = z1000.z1000()

    # Enable command-line processing for options like -remote.
    # fpga.create_cmdline(switchlist=['-remote'])  # TODO

    # 3. Load the specific FPGA part, which also sets the default flow and libraries.
    project.set_fpga(fpga)

    # 4. Use the specific flow for this build.
    # Note: z1000 might already load a flow, but it's good practice to specify it.
    project.set_flow(logik_flow.LogikFlow())

    # # 5. Set any general options.
    project.set('option', 'quiet', True)

    project.set('option', 'continue', True, step="place")

    # 6. Run the compilation.
    project.run()

    # 7. Display the results summary.
    project.summary()


if __name__ == "__main__":
    hello_adder()
