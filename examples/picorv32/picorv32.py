#!/usr/bin/env python3

import siliconcompiler
from logik.flows.logik_flow import LogikFlow

from logiklib.zeroasic.z1062 import z1062


def build():
    module_name = 'picorv32'
    design = siliconcompiler.Design(module_name)

    # Fetch picorv32 from the logikbench repo
    # Silicon Compiler will download and cache the files for us
    design.set_dataroot(
        'picorv32-logikbench',
        'git+https://github.com/zeroasiccorp/logikbench.git',
        'db866c536340c071c563a063c9406888070dfbda')

    with design.active_dataroot('picorv32-logikbench'):
        design.add_file(f'logikbench/blocks/{module_name}/rtl/{module_name}.v',
                        fileset='rtl')
        design.set_topmodule(module_name, fileset="rtl")

    design.set_dataroot('constraints', __file__)
    with design.active_dataroot('constraints'):
        # Add timing constraints
        design.add_file(f'{module_name}.sdc', fileset='sdc')

        # Define pin constraints
        design.add_file(f"constraints/z1062/{module_name}.pcf",
                        fileset='pcf')

    project = siliconcompiler.FPGA(design)

    # add design files to the project
    project.add_fileset('rtl')
    project.add_fileset('sdc')
    project.add_fileset('pcf')

    fpga = z1062.z1062()
    project.set_fpga(fpga)

    project.set_flow(LogikFlow())

    # # Customize steps for this design
    project.option.set_quiet(True)

    project.run()
    project.summary()


if __name__ == '__main__':
    build()
