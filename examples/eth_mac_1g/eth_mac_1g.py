#!/usr/bin/env python3

# This is the logik run script for demonstrating RTL-to-bitstream
# with Alex Forencich's 1G Ethernet MAC

import siliconcompiler

from logik.flows.logik_flow import LogikFlow

from logik.demo import z1000  # Temporary
# from logik.z1000_local_cad import z1000  # Temporary


def build():
    design = siliconcompiler.Design('eth_mac_1g_wrapper')

    # Define source files from verilog-ethernet repo

    # First we need to register the verilog-ethernet repo
    # as a package
    design.set_dataroot(
        'verilog-ethernet',
        'git+https://github.com/alexforencich/verilog-ethernet.git',
        '77320a9471d19c7dd383914bc049e02d9f4f1ffb')

    # Then we can pull in the specific RTL we need from that
    # repository -- Silicon Compiler will download and cache the files
    # for us
    with design.active_dataroot('verilog-ethernet'):
        for source_file in ('eth_mac_1g.v',
                            'axis_gmii_rx.v',
                            'axis_gmii_tx.v',
                            'lfsr.v'):
            design.add_file(f'rtl/{source_file}', fileset='rtl')

    # Add in our top-level wrapper, stored locally
    design.set_dataroot('ethmac_example', __file__)
    with design.active_dataroot('ethmac_example'):
        design.add_file('eth_mac_1g_wrapper.v', fileset='rtl')
        design.set_topmodule("eth_mac_1g_wrapper", fileset="rtl")

        # Add timing constraints
        design.add_file('eth_mac_1g.sdc', fileset='sdc')

        # Define pin constraints
        design.add_file("constraints/z1000/pin_constraints.pcf",
            fileset='pcf')

    project = siliconcompiler.FPGA(design)

    project.add_fileset('rtl')
    project.add_fileset('sdc')
    project.add_fileset('pcf')

    fpga = z1000.z1000()

    project.set_fpga(fpga)

    project.set_flow(LogikFlow())

    project.set('option', 'quiet', True)

    project.run()
    project.summary()


if __name__ == '__main__':
    build()
