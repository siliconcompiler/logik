import argparse
import importlib
import os
import sys

import logiklib.zeroasic
import logiklib
import siliconcompiler
from logik import __version__
from logik.flows.logik_flow import LogikFlow

# TODO check conformity with other tools
# TODO: topmodule?
# TODO: --place, etc.

# logik adder -v adder.v -sdc adder.sdc -arch z1010
# TODO no python exceptions tolerated


def setup_logik(sources, arch_name, sdc, pcf, remote) -> siliconcompiler.Project:
    design = siliconcompiler.Design('logik_design')

    # Add sources
    for source in [sources]:
        design.add_file(source, fileset="rtl")

    # Set topmodule  #TODO: auto-detection?
    design.set_topmodule('adder', fileset="rtl")

    # Add constraints
    if sdc:
        pass  # TODO
    if pcf:
        pass  # TODO

    project = siliconcompiler.FPGA(design)

    # Set architecture
    try:
        arch_module = importlib.import_module(f'logiklib.zeroasic.{arch_name}.{arch_name}')
    except ModuleNotFoundError:
        path = list(logiklib.zeroasic.__path__)[0]
        available = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('_')]
        print(f"Error: Architecture '{arch_name}' not found in logiklib.")
        print(f"Available architectures: {' '.join(sorted(available))}")
        sys.exit(1)

    # Configure project
    project.add_fileset('rtl')

    fpga = getattr(arch_module, arch_name)()
    project.set_fpga(fpga)

    project.set_flow(LogikFlow())

    return project


def run_logik():
    program_name = "logik"
    description = f"""
    Logik {__version__}\n\n:
    An open-source FPGA flow using Yosys, VPR, and GenFasm.
    """

    parser = argparse.ArgumentParser(
        prog=program_name,
        description=description,
        formatter_class=argparse.HelpFormatter)

    parser.add_argument("-v", "--verilog", help="Path to the Verilog source file(s).")
    parser.add_argument("-sv", "--sverilog", help="Path to the SystemVerilog source file(s).")
    parser.add_argument("--vhdl", help="Path to the VHDL source file(s).")  # TODO
    parser.add_argument("-sdc", "--sdc", help="Path to the SDC file(s).")
    parser.add_argument("-pcf", "--pin-constraints", help="Path to the PCF file(s).")
    parser.add_argument("-arch", "--arch", help="Path to the architecture file(s).")
    # parser.add_argument("-top", "--topmodule", help="Name of the top-level module.")  # TODO autoset
    parser.add_argument("-remote", action="store_true", help="Run the flow on a remote server.")
    parser.add_argument("--version", action="store_true", help="Show dependency versions and exit.")

    args = parser.parse_args()

    if args.version:
        print_versions()
        return

    sources = args.verilog
    arch_name = args.arch
    sdc = args.sdc
    pcf = args.pin_constraints

    project = setup_logik(sources, arch_name, sdc, pcf, args.remote)

    project.run()

    project.summary()

    # print fmax, area


def print_versions():
    print(f"Logik version: {__version__}")
    print(f"SiliconCompiler version: {siliconcompiler.__version__}")
    print(f"LogikLib version: {logiklib.__version__}")
    # yosys
    # print(f"VPR version: {siliconcompiler.tools..vpr.__version__}")
    # opensta
    # wildebeest


if __name__ == "__main__":
    run_logik()