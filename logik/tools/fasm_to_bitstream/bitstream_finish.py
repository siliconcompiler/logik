# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from logik.tools.fasm_to_bitstream import \
    fasm_to_bitstream as fasm_utils

from siliconcompiler.tool import Task


class BitstreamFinishTask(Task):
    def __init__(self):
        super().__init__()

    def tool(self):
        return "fasm_to_bitstream"

    def task(self):
        return "bitstream_finish"

    def setup(self):
        '''
        Perform bitstream finishing
        '''
        super().setup()

        fpga = self.project.get('fpga', 'device')
        fpga_obj = self.project.get('library', fpga, field='schema')
        # dd_required_key(...) you can pass in an object the fpga and then finish the keypath
        # but this will need to be "tool", "???", "bitstream_map"
        self.add_required_key(fpga_obj, "tool", 'convert_bitstream', 'bitstream_map')

        self.add_input_file(ext="fasm")
        self.add_output_file(ext="json")
        self.add_output_file(ext="bin")

    def run(self):
        fpga = self.project.get('fpga', 'device')
        fpga_obj = self.project.get('library', fpga, field='schema')

        # topmodule = self.top()
        fasm_file = f"inputs/{self.design_topmodule}.fasm"

        bitstream_map = fpga_obj.find_files("tool", 'convert_bitstream', 'bitstream_map')

        json_outfile = f"outputs/{self.design_topmodule}.json"
        binary_outfile = f"outputs/{self.design_topmodule}.bin"

        # Finishing steps are as follows:
        # 1. Convert FASM to IR
        config_bitstream = fasm_utils.fasm2bitstream(fasm_file, bitstream_map)

        # 2.  Write IR to JSON for inspection purposes
        fasm_utils.write_bitstream_json(config_bitstream, json_outfile)

        # 3.  Flatten the IR to a 1D address space
        flattened_bitstream = fasm_utils.generate_flattened_bitstream(config_bitstream)

        # 4.  Format the flattened bitstream to binary
        binary_bitstream = fasm_utils.format_binary_bitstream(flattened_bitstream)

        # 5.  Write binary to file
        fasm_utils.write_bitstream_binary(binary_bitstream, binary_outfile)

        return 0
