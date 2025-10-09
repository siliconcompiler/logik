#!/usr/bin/env python3

# This is the logik run script for demonstrating RTL-to-bitstream
# with Alex Forencich's 1G Ethernet MAC

import siliconcompiler
from logik.flows.logik_flow import LogikFlow


from logik.z1062_local_cad import z1062  # Temporary


def build():
    design = siliconcompiler.Design('picorv32')

    # Define source files from verilog-ethernet repo

    # First we need to register the verilog-ethernet repo
    # as a package
    design.set_dataroot(
        'picorv32-logikbench',
        'git+https://github.com/zeroasiccorp/logikbench.git',
        'db866c536340c071c563a063c9406888070dfbda')

    # Then we can pull in the specific RTL we need from that
    # repository -- Silicon Compiler will download and cache the files
    # for us
    with design.active_dataroot('picorv32-logikbench'):
        design.add_file(f'logikbench/blocks/picorv32/rtl/picorv32.v', fileset='rtl')
        design.set_topmodule("picorv32", fileset="rtl")

    design.set_dataroot('constraints', __file__)
    with design.active_dataroot('constraints'):
        # Add timing constraints
        design.add_file('picorv32.sdc', fileset='sdc')

        # Define pin constraints
        design.add_file("constraints/z1062/picorv32.pcf",
            fileset='pcf')

    project = siliconcompiler.FPGA(design)

    project.add_fileset('rtl')
    project.add_fileset('sdc')
    project.add_fileset('pcf')

    fpga = z1062.z1062()
    project.set_fpga(fpga)

    project.set_flow(LogikFlow())

    # # Customize steps for this design
    project.set('option', 'quiet', True)

    project.run()
    project.summary()


if __name__ == '__main__':
    build()