import argparse
import importlib
import os
import re
import sys
import subprocess

import logiklib.zeroasic
import logiklib
import siliconcompiler
from logik import __version__
from logik.flows.logik_flow import LogikFlow

# TODO error/warning coloring fixes


def setup_logik(
    sources, arch_name: str, top: str, sdcs: str, pcf: str, remote: bool, threads: int
) -> siliconcompiler.Project:
    design = siliconcompiler.Design("logik_design")

    # Add sources
    for source in [sources]:
        design.add_file(source, fileset="rtl")

    # Set topmodule  #TODO: auto-detection?
    design.set_topmodule(top, fileset="rtl")

    # Add constraints
    for sdc in [sdcs]:
        design.add_file(sdc, fileset="sdc")

    if pcf:
        design.add_file(pcf, fileset="pcf")

    project = siliconcompiler.FPGA(design)

    # Set architecture
    try:
        arch_module = importlib.import_module(
            f"logiklib.zeroasic.{arch_name}.{arch_name}"
        )
    except ModuleNotFoundError:
        path = list(logiklib.zeroasic.__path__)[0]
        available = [
            d
            for d in os.listdir(path)
            if os.path.isdir(os.path.join(path, d)) and not d.startswith("_")
        ]
        print(f"Error: Architecture '{arch_name}' not found in logiklib.")
        print(f"Available architectures: {' '.join(sorted(available))}")
        sys.exit(1)

    # Configure project
    project.add_fileset("rtl")

    fpga = getattr(arch_module, arch_name)()
    project.set_fpga(fpga)

    project.set_flow(LogikFlow())

    # TODO Set threads

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
        formatter_class=argparse.HelpFormatter,
    )

    parser.add_argument(
        "-v", "--verilog", help="Path to the Verilog/SystemVerilog source file(s)."
    )
    parser.add_argument("-sdc", "--sdc", help="Path to the SDC file(s).")
    parser.add_argument(
        "-pcf", "--pin-constraints", type=str, help="Path to the PCF file(s)."
    )
    parser.add_argument("-arch", "--arch", help="Path to the architecture file(s).")
    # TODO autoset
    parser.add_argument(
        "--top",
        "--topmodule",
        help="Name of the top-level module.",
    )
    parser.add_argument(
        "-remote", action="store_true", help="Run the flow on a remote server."
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit.")
    parser.add_argument(
        "--dep-versions", action="store_true", help="Show dependency versions and exit."
    )
    parser.add_argument(
        "-j",
        "--threads",
        type=int,
        default=1,
        help="Number of threads to use for parallel execution. 0 for auto.",
    )
    args = parser.parse_args()

    if args.version or args.dep_versions:
        if args.version:
            print(f"logik version: {__version__}")
        if args.dep_versions:
            print_dep_versions()
        return

    validate_args(args)

    sources = args.verilog
    arch_name = args.arch
    sdc = args.sdc
    pcf = args.pin_constraints
    top = args.top

    project = setup_logik(sources, arch_name, top, sdc, pcf, args.remote, args.threads)

    project.run()

    project.summary()

    # print fmax, area


def print_dep_versions():
    print(f"siliconcompiler version: {siliconcompiler.__version__}")
    print(f"logiklib version: {logiklib.__version__}")
    print(
        f"yosys version {subprocess.run(['yosys', '--version'], capture_output=True, text=True).stdout.strip()}"
    )
    output = subprocess.run(["vpr", "--version"], capture_output=True, text=True)
    full_output = output.stdout + output.stderr
    version = re.search(r"Version:\s*(\S+)", full_output).group(1)
    print(f"vpr version: {version}")
    print(
        f"opensta version: {subprocess.run(['sta', '-version'], capture_output=True, text=True).stdout.strip()}"
    )


def validate_args(args):
    if not args.verilog:
        print("Error: At least one Verilog source file must be specified with -v or --verilog.")
        sys.exit(1)
    if not args.arch:
        print("Error: Architecture must be specified with -arch or --arch.")
        sys.exit(1)
    if not args.sdc:
        print("Error: At least one SDC file must be specified with -sdc or --sdc.")
        sys.exit(1)
    if not args.top:
        print("Error: Top-level module name must be specified with --top.")
        sys.exit(1)


if __name__ == "__main__":
    run_logik()
