System Software Requirements
============================

Supported Operating Systems
---------------------------

The following operating systems are supported without the requirement of running within a docker container:

* Ubuntu 20.04

Additional OS support is provided by running within a docker container.

General Purpose Software Requirements
-------------------------------------

The following general purpose software must be installed on your system to use this flow:

* Python 3.10 or higher
* git

Required EDA Software Tools
---------------------------

* Silicon Compiler
* Yosys
* VPR

For VHDL support, GHDL is also required.

For SystemVerilog support, slang is also required.

For links to all EDA software Github repositories and documentation pages, please consult the :doc:`external_links`.

Optional EDA Software Tools
---------------------------

While not required to run the RTL-to-bitstream flow, HDL simulation support is required to run HDL simulations on provided examples.

Either of the following open-source simulators may be used for HDL simulation:

* Icarus Verilog
* Verilator
  
For waveform viewing, there are a few open source viewers to choose from:

* Surfer
* GTKWave
  
For links to all EDA software Github repositories and documentation pages, please consult the :doc:`external_links`.

