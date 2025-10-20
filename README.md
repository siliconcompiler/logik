![Logik](https://raw.githubusercontent.com/siliconcompiler/logik/main/images/logik_logo_with_text.png)

[![Regression](https://github.com/siliconcompiler/logik/actions/workflows/regression.yml/badge.svg)](https://github.com/siliconcompiler/logik/actions/workflows/regression.yml)
[![Lint](https://github.com/siliconcompiler/logik/actions/workflows/lint.yml/badge.svg)](https://github.com/siliconcompiler/logik/actions/workflows/lint.yml)

-----------------------------------------------------------------------------------

Logik is an open source FPGA tool chain with support for high level language parsing, synthesis, placement, routing, bit-stream generation, and analysis. Users enter design sources, constraints, and compile options through a simple [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler/) Python API. Once setup is complete, automated compilation can be initiated with a single line run command.

Logik depends on the [Logiklib](https://github.com/siliconcompiler/logiklib) which contains the architecture descriptions and device setup files needed to drive the Logik flow.

![logik_flow](https://raw.githubusercontent.com/siliconcompiler/logik/main/images/logik_flow.svg)

Logik supports most of the features you would expect in a commercial proprietary FPGA tool chain.

| Feature                  | Status |
|--------------------------|--------|
| Design languages         | SystemVerilog, Verilog, VHDL
| ALU synthesis            | Supported
| RAM synthesis            | Supported
| Timing constraints (SDC) | Supported
| Pin Constraints (PCF)    | Supported
| Bitstream generation     | Supported
| IP management            | Supported
| Remote compilation       | Supported
| Multi-clock designs      | Supported
| Supported devices        | Logiklib devices

## Getting Started

The Logik tool chain is available through PyPi and can be installed using pip.

```sh
python -m pip install --upgrade logik
```

All open source FPGA pre-requisites can be installed via the SiliconCompiler `sc-install` utility.

```sh
sc-install -group fpga
```

The following example illustrate some essential Logik features. For complete documentation of all options available, see the [SiliconCompiler project](https://github.com/siliconcompiler/siliconcompiler/blob/main/README.md).

```python

import siliconcompiler

from logik.flows.logik_flow import LogikFlow

from logiklib.zeroasic.z1000 import z1000


def hello_adder():
    # 1. Create a Design object to hold source files and constraints.
    design = siliconcompiler.Design('adder')

    design.add_file('adder.v', fileset="rtl")
    design.set_topmodule('adder', fileset="rtl")

    # 2. Create an FPGA object with a -remote command line option
    project = siliconcompiler.FPGA(design)

    project.add_fileset('rtl')

    # 2. Create an FPGA object and associate the design with it.
    fpga = z1000.z1000()

    # 3. Load the specific FPGA part, which also sets the default flow and libraries.
    project.set_fpga(fpga)

    #  Use the specific flow for this build.
    project.set_flow(LogikFlow())

    # # Customize steps for this design
    project.option.set_quiet(True)

    # Run the compilation.
    project.run()

    # Display the results summary.
    project.summary()


if __name__ == "__main__":
    hello_adder()

```

## Examples

* [Ethernet](./examples/eth_mac_1g/eth_mac_1g.py): Ethernet MAC compiled for the `z1000` architecture
* [Adder](examples/adder/adder.py): Small adder example compiled for the `z1000` architecture.
* [Picorv32](examples/picorv32/picorv32.py): picorv32 RISC-V CPU example compiled for the `z1062` architecture.

## Documentation

* [Logik Documentation](https://logik.readthedocs.io/en/latest/)
* [SiliconCompiler Documentation](https://docs.siliconcompiler.com/en/stable/)


## Installation

Logik is available as wheel packages on PyPI for macOS, Windows and Linux platforms. For a Python 3.8-3.12 environment, just use pip to install.

```sh
python -m pip install --upgrade logik
```

Running natively on your local machine will require installing a number of prerequisites:

* [Silicon Compiler](https://github.com/siliconcompiler/siliconcompiler): Hardware compiler framework
* [Slang](https://github.com/MikePopoloski/slang): SystemVerilog Parser
* [GHDL](https://ghdl.github.io/ghdl/): VHDL parser
* [Yosys](https://github.com/YosysHQ/yosys): Logic synthesis
* [VPR](https://github.com/verilog-to-routing/vtr-verilog-to-routing): FPGA place and route
* [FASM](https://github.com/chipsalliance/fasm): FPGA assembly parser and generator

We recommend using the SiliconCompiler `sc-install` utility to automatically install the correct versions of all open source FPGA tool dependencies.

```sh
sc-install -group fpga
```

Detailed installation instructions can be found in the [SiliconCompiler Installation Guide](https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools).


## License

[Apache License 2.0](LICENSE)

## Issues / Bugs
We use [GitHub Issues](https://github.com/siliconcompiler/logik/issues) for tracking requests and bugs.
