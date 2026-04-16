# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler.flows import fpgaflow
from siliconcompiler.tools.ghdl import convert as ghdl_convert

from logik.tools.fasm_to_bitstream import bitstream_finish


class LogikVHDLFlow(fpgaflow.FPGAVPROpenSTAFlow):
    """An open-source FPGA flow for VHDL designs using GHDL, Yosys, VPR, and GenFasm.

    GHDL runs the elaboration step, which converts VHDL to
    Verilog before passing to Yosys synthesis.

    The flow consists of the following steps:

    * **elaborate**: Convert VHDL to Verilog using GHDL.
    * **synthesis**: Synthesize the elaborated design into a netlist using Yosys.
    * **place**: Place the netlist components onto the FPGA architecture using VPR.
    * **route**: Route the connections between placed components using VPR.
    * **timing**: Perform static analysis using OpenSTA.
    * **bitstream**: Generate the final bitstream using GenFasm.
    * **convert_bitstream**: Format bitstream from fasm to bits.
    """

    def __init__(self, name: str = "logik_vhdl_flow") -> None:
        """
        Initializes the LogikVHDLFlow.

        Args:
            name (str): The name of the flow.
        """
        super().__init__(name)

        # Replace the slang elaborate node with GHDL
        self.remove_node("elaborate")
        self.node("elaborate", ghdl_convert.ConvertTask())
        self.edge("elaborate", "synthesis")

        self.node("convert_bitstream", bitstream_finish.BitstreamFinishTask())
        self.edge("bitstream", "convert_bitstream")


if __name__ == "__main__":
    LogikVHDLFlow().write_flowgraph(f"{LogikVHDLFlow().name}.png")
