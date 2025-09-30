# Copyright 2024 Zero ASIC Corporation

from siliconcompiler.flows.fpgaflow import FPGAVPROpenSTAFlow

from siliconcompiler.tools.vpr import VPRFPGA
from siliconcompiler.tools.yosys import YosysFPGA
from siliconcompiler.tools.opensta import OpenSTAFPGA


# ####################################################
# # Setup for z1000 FPGA
# ####################################################

class z1000(YosysFPGA, VPRFPGA):
    '''
    Logik driver for z1000
    '''
    def __init__(self):
        super().__init__()
        self.set_name("z1000")

        self.define_tool_parameter('convert_bitstream', 'bitstream_map', 'file',
                                   'TODO help string')  # TODO change name from convert bitstream,
                                    # bitstream map -> map

        self.set_dataroot("logik", "python://logik")
        self.package.set_vendor("ZeroASIC")
        self.set_lutsize(4)

        self.add_yosys_registertype(["dff", "dffr", "dffe", "dffer"])
        self.add_yosys_featureset(["async_reset", "enable"])
        with self.active_dataroot("logik"):
            self.set_yosys_flipfloptechmap("z1000_cad/tech_flops.v")

        self.set_vpr_devicecode("z1000")
        self.set_vpr_clockmodel("route")
        self.set_vpr_channelwidth(50)
        self.add_vpr_registertype(["dff", "dffr", "dffe", "dffer"])
        with self.active_dataroot("logik"):
            self.set_vpr_archfile("z1000_cad/z1000.xml")
            self.set_vpr_graphfile("z1000_cad/z1000_rr_graph.xml")
            self.set_vpr_constraintsmap("z1000_cad/z1000_constraint_map.json")

        with self.active_dataroot("logik"):
            self.set_convert_bitstream_bitstream_map('z1000_cad/z1000_bitstream_map.json')

        self.set_vpr_router_lookahead("classic")


    def set_convert_bitstream_bitstream_map(self, file: str, dataroot: str = None):
        with self.active_dataroot(self._get_active_dataroot(dataroot)):
            return self.set("tool", "convert_bitstream", "bitstream_map", file)
