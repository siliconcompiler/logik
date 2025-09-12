# picorv32.py

from logik.flows import logik_flow
from logiklib.zeroasic.z1062 import z1062

from siliconcompiler import Chip


def build():

    design_name = 'picorv32'
    design_top_module = 'picorv32'

    chip = Chip(f'{design_name}')

    # Set default part name
    chip.set('fpga', 'partname', "z1062")

    chip.use(z1062)
    chip.use(logik_flow)
    flow_name = 'logik_flow'
    chip.set('option', 'flow', flow_name)

    # Register the picorv32 repo as a package
    chip.register_source(
        name='picorv32-logikbench',
        path='git+https://github.com/zeroasiccorp/logikbench.git',
        ref='db866c536340c071c563a063c9406888070dfbda')

    # Add source HDL files
    chip.input('logikbench/blocks/picorv32/rtl/picorv32.v',
               package='picorv32-logikbench')

    # Set the top module to {design_top_module}
    chip.set('option', 'entrypoint', f'{design_top_module}')

    # Define timing constraints
    chip.input(f'{design_name}.sdc')

    # Define pin constraints
    chip.input(f'constraints/z1062/{design_name}.pcf')

    chip.set('option', 'quiet', True)

    chip.run()
    chip.summary()


if (__name__ == '__main__'):
    build()
