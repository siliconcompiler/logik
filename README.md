
![image info](images/logik_logo_with_text.png)

-----------------------------------------------------------------------------------

Logik is a light weight FPGA tool chain based on mature open source technologies, including:

* [Silicon Compiler](https://github.com/siliconcompiler/siliconcompiler): Hardware compiler framework
* [Yosys](https://github.com/YosysHQ/yosys): Logic synthesis
* [VPR](https://github.com/verilog-to-routing/vtr-verilog-to-routing): FPGA place and route
* [GHDL](https://ghdl.github.io/ghdl/): VHDL parser
* [Surelog](https://github.com/chipsalliance/Surelog): SystemVerilog parser
* [FASM](https://github.com/chipsalliance/fasm): FPGA assembly parser and generator

Design sources, constraints, and compile configuration is specified by the user through a simple Python interface. Compilation is managed by the SiliconCompiler framework. Logik supports most of the features you would expect in a commercial proprietary FPGA tool chain.  

| Feature                  | Status |
|--------------------------|--------|
| Design languages         | Verilog, SystemVerilog, VHDL
| ALU synthesis            | Supported
| RAM synthesis            | Supported
| Timing constraints (SDC) | Supported
| Pin Constraints (PCF)    | Supported
| Bitstream generation     | Supported
| IP management            | Supported
| Remote compilation       | Supported
| Multi-clock designs      | In progress
| FPGA devices             | ZA

![image info](images/logik_flow.svg)

## Getting Started

The Logik project is available through PyPi and can be installed using pip. If you want to run locally on your machine, you will need to [install all of the pre-requisites]((#installation)) or launch the [Logik Docker image](#running-docker).

```sh
python -m pip install --upgrade logik
```

The following example illustrate some essential Logik features. The source code for the example is located in the [./examples/adder](./examples/adder/) directory. For complete documentation of all options available, see the [SiliconCompiler project](https://github.com/siliconcompiler/siliconcompiler/blob/main/README.md). 

```python
from siliconcompiler import Chip
from logik.targets import logik_target

def hello_adder():

    # Create compilation object
    chip = Chip('adder')                                  

    # Specify design sources
    chip.input('adder.v')

    # Specify pin constraints
    chip.input('adder.pcf')

    # Compiler options
    chip.set('option', 'quiet', True)
    chip.set('option', 'remote', True)

    # Select target fpga
    chip.set('fpga', 'partname', 'logik_demo')

    # Load target settings
    chip.load_target(logik_target)                        

    # Run compiler
    chip.run()

    # Display compiler results
    chip.summary()

if __name__ == "__main__":
    hello_adder()
```

The resulting FPGA bitstream is generated at './adder/build/adder/job0/bitstream/0/outputs/adder.bin'.


To test out your generated bitstream, you can upload it to a emulated FPGA device running in the Zero ASIC [Digital Twin Platform](https://www.zeroasic.com/emulation?demo=fpga).


## More Examples

* [UMI "Hello World"](./examples/umi_hello/)
* [UMI FIR Filter](./examples/umi_fir_filter)
* [EBRICK demo](./examples/ebrick_demo_fpga/)

## Documentation

* [Logic User Guide]()
* [Logik Reference Manual]()
* [SiliconCompiler Documentation](https://docs.siliconcompiler.com/en/stable/)


## Installation

Logik is available as wheel packages on PyPI for macOS, Windows and Linux platforms. For working Python 3.8-3.12 environment, just use pip to install.

```sh
python -m pip install --upgrade logik
```

Running natively on your local machine will require a number of prerequisite tools (Yosys, Surelog, VPR) a Automated Ubuntu based install scripts are included for convenience within the SiliconCompiler project. Detailed instructions for installing all tools can be found in the [SiliconCompiler Installation Guide](https://docs.siliconcompiler.com/en/stable/user_guide/installation.html#external-tools).


## Running Docker

A docker container is available for folks who prefer that route.

```sh
docker run -it -v "${PWD}/sc_work:/sc_work" ghcr.io/siliconcompiler/sc_runner:latest
```


## License

[MIT](LICENSE)

## Issues / Bugs
We use [GitHub Issues](https://github.com/zeroasiccorp/logik/issues) for tracking requests and bugs.
