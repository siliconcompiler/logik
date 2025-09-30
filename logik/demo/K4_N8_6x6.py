# Copyright 2024 Zero ASIC Corporation

from siliconcompiler.flows.fpgaflow import FPGAVPROpenSTAFlow

from siliconcompiler.tools.vpr import VPRFPGA
from siliconcompiler.tools.yosys import YosysFPGA
from siliconcompiler.tools.opensta import OpenSTAFPGA


# ####################################################
# # Setup for K4_N8_6x6 FPGA
# ####################################################

class K4_N8_6x6(YosysFPGA, VPRFPGA):
    '''
    Logik driver for K4_N8_6x6
    '''
    def __init__(self):
        super().__init__()
        self.set_name("K4_N8_6x6")

        self.define_tool_parameter('convert_bitstream', 'bitstream_map', 'file',
                                   'TODO help string')  # TODO change name from convert bitstream,
                                    # bitstream map -> map

        self.set_dataroot("logik", "python://logik")
        self.package.set_vendor("ZeroASIC")
        self.set_lutsize(4)

        self.add_yosys_registertype(["dff", "dffr", "dffe", "dffer"])
        self.add_yosys_featureset(["async_reset", "enable"])
        with self.active_dataroot("logik"):
            self.set_yosys_flipfloptechmap("K4_N8_6x6_2_multisource_cad/tech_flops.v")

        self.set_vpr_devicecode("K4_N8_6x6")
        self.set_vpr_clockmodel("route")
        self.set_vpr_channelwidth(50)
        self.add_vpr_registertype(["dff", "dffr", "dffe", "dffer"])
        with self.active_dataroot("logik"):
            self.set_vpr_archfile("K4_N8_6x6_2_multisource_cad/K4_N8_6x6.xml")
            self.set_vpr_graphfile("K4_N8_6x6_2_multisource_cad/K4_N8_6x6_rr_graph.xml")
            self.set_vpr_constraintsmap("K4_N8_6x6_2_multisource_cad/K4_N8_6x6_constraint_map.json")

        with self.active_dataroot("logik"):
            self.set_convert_bitstream_bitstream_map('K4_N8_6x6_2_multisource_cad/K4_N8_6x6_bitstream_map.json')

        self.set_vpr_router_lookahead("classic")

        # with self.active_dataroot("logik"):
        #     with self.active_fileset("K4_N8_6x6_opensta_liberty_files"):
        #         self.add_file("data/demo_fpga/vtr_primitives.lib")
        #         self.add_file("data/demo_fpga/tech_flops.lib")
        #         self.add_opensta_liberty_fileset()

    def set_convert_bitstream_bitstream_map(self, file: str, dataroot: str = None):
        with self.active_dataroot(self._get_active_dataroot(dataroot)):
            return self.set("tool", "convert_bitstream", "bitstream_map", file)
