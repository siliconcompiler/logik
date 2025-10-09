# Copyright 2024 Zero ASIC Corporation

from logik.devices.logik_fpga import LogikFPGA


# ####################################################
# # Setup for z1000 FPGA
# ####################################################

class z1000(LogikFPGA):
    '''
    Logik driver for z1000
    '''
    def __init__(self):
        super().__init__()
        part_name = "z1000"
        self.set_name(part_name)

        self.define_tool_parameter('convert_bitstream', 'bitstream_map', 'file',
                                   'map for fasm->bitstream conversion')

        self.set_dataroot(
            part_name, f"github://siliconcompiler/logiklib/v0.1.0/{part_name}_cad.tar.gz", "0.1.0")

        self.package.set_vendor("ZeroASIC")
        self.set_lutsize(4)

        self.add_yosys_registertype(["dff", "dffr", "dffe", "dffer"])
        self.add_yosys_featureset(["async_reset", "enable"])
        with self.active_dataroot(part_name):
            self.set_yosys_flipfloptechmap("techlib/tech_flops.v")

        self.set_vpr_devicecode(part_name)
        self.set_vpr_clockmodel("route")
        self.set_vpr_channelwidth(50)
        self.add_vpr_registertype(["dff", "dffr", "dffe", "dffer"])
        with self.active_dataroot(part_name):
            self.set_vpr_archfile("cad/z1000.xml")
            self.set_vpr_graphfile("cad/z1000_rr_graph.xml")
            self.set_vpr_constraintsmap("cad/z1000_constraint_map.json")

        with self.active_dataroot(part_name):
            self.set_convert_bitstream_bitstream_map('cad/z1000_bitstream_map.json')

        self.set_vpr_router_lookahead("classic")
