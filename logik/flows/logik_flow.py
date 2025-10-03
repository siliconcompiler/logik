# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler import FPGA
from siliconcompiler.flows import fpgaflow

from logik.tools.fasm_to_bitstream import bitstream_finish


class LogikFlow(fpgaflow.FPGAVPRFlow):
    '''An open-source FPGA flow using Yosys, VPR, and GenFasm.

    This flow is designed for academic and research FPGAs, utilizing VPR
    (Versatile Place and Route) for placement and routing.

    The flow consists of the following steps:

    * **elaborate**: Elaborate the RTL design from sources.
    * **synthesis**: Synthesize the elaborated design into a netlist using Yosys.
    * **place**: Place the netlist components onto the FPGA architecture using VPR.
    * **route**: Route the connections between placed components using VPR.
    * **bitstream**: Generate the final bitstream using GenFasm.
    * **convert_bitstream**: Format bitstream from fasm to bits.
    '''
    def __init__(self, name: str = "logik_flow"):
        """
        Initializes the FPGAVPRFlow.

        Args:
            name (str): The name of the flow.
        """
        super().__init__(name)

        self.node("convert_bitstream", bitstream_finish.BitstreamFinishTask())
        self.edge("bitstream", "convert_bitstream")


# ##################################################
if __name__ == "__main__":
    LogikFlow().write_flowgraph(f"{LogikFlow().name}.png")
