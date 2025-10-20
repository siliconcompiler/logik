Logik
-------------------------------------------------------------

[![Regression](https://github.com/siliconcompiler/logik/actions/workflows/regression.yml/badge.svg)](https://github.com/siliconcompiler/logik/actions/workflows/regression.yml)
[![Lint](https://github.com/siliconcompiler/logik/actions/workflows/lint.yml/badge.svg)](https://github.com/siliconcompiler/logik/actions/workflows/lint.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Logik is an open source FPGA tool chain with support for high level language parsing, synthesis, placement, routing, bit-stream generation, and analysis. Users enter design sources, constraints, and compile options through a simple [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler/) Python API. Once setup is complete, automated compilation can be initiated with a single line run command. Logik relies on the [Logiklib](https://github.com/siliconcompiler/logiklib) project for all architecture and device descriptions.

![logik_flow](https://raw.githubusercontent.com/siliconcompiler/logik/main/images/logik_flow.svg)

Logik supports most of the features you would expect in a commercial proprietary FPGA tool chain.

| Feature                  | Status |
|--------------------------|--------|
| Design languages         | SystemVerilog, Verilog, VHDL
| DSP synthesis            | Supported
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
sc-install opensta
```

The following example illustrate some essential Logik features. For complete documentation of all options available, see the [SiliconCompiler project](https://github.com/siliconcompiler/siliconcompiler/blob/main/README.md).

```python

import siliconcompiler
from logik.flows.logik_flow import LogikFlow
from logiklib.zeroasic.z1000 import z1000

# 1. Create a Design object to hold source files and constraints.
design = siliconcompiler.Design('adder')
design.add_file('adder.v', fileset="rtl")
design.set_topmodule('adder', fileset="rtl")

# 2. Create an FPGA project
project = siliconcompiler.FPGA(design)

# 3. Assign file sets to use for elaboration
project.add_fileset('rtl')

# 4. Select the rtl2bits flow to use
project.set_flow(LogikFlow())

# 5. Load FPGA part settings and associated flow and libraries.
project.set_fpga(z1000.z1000())

# 6. User defined options
project.option.set_quiet(True)

# 7. Run compilatin
project.run()

#6. Display summary of results
project.summary()

```

> [!NOTE]
> The required files can be found at: [heartbeat example](https://github.com/siliconcompiler/logik/tree/main/examples/adder)

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
* [Yosys](https://github.com/YosysHQ/yosys): Logic synthesis platform
* [Wildebeest](https://github.com/zeroasiccorp/wildebeest): High performance synthesis yosys plugin
* [VPR](https://github.com/verilog-to-routing/vtr-verilog-to-routing): FPGA place and route
* [FASM](https://github.com/chipsalliance/fasm): FPGA assembly parser and generator
* [OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA): Production grade static timing analysis engine

We recommend using the SiliconCompiler `sc-install` utility to automatically install the correct versions of all open source FPGA tool dependencies.

```sh
sc-install -group fpga
```

Detailed installation instructions can be found in the [SiliconCompiler Installation Guide](https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools).


## License

The Logik project is licensed under the open source [Apache License 2.0](LICENSE). For licensing terms of all dependencies, visit depedency repository.

## Issues / Bugs
We use [GitHub Issues](https://github.com/siliconcompiler/logik/issues) for tracking requests and bugs.
