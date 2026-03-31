import argparse
import importlib
import os

import logiklib.zeroasic
import logiklib
import siliconcompiler
from logik import __version__
from logik.flows.logik_flow import LogikFlow

# TODO check conformity with other tools
# TODO: topmodule?
# TODO: --place, etc.

# logik adder -v adder.v -sdc adder.sdc -arch z1010


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

    parser.add_argument("-remote", action="store_true", help="Run the flow on a remote server.")

    args = parser.parse_args()

    sources = args.verilog
    arch_name = args.arch
    sdc = args.sdc
    pcf = args.pin_constraints

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
        return

    # Configure project
    project.add_fileset('rtl')

    fpga = getattr(arch_module, arch_name)()
    project.set_fpga(fpga)

    project.set_flow(LogikFlow())

    project.run()

    project.summary()

    # print fmax, area


if __name__ == "__main__":
    run_logik()