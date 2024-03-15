from ebrick_fpga_cad.tools.fasm_to_bitstream import \
    fasm_to_bitstream as fasm_utils


def setup(chip):
    '''
    Perform bitstream finishing
    '''

    tool = 'fasm_to_bitstream'
    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    task = chip._get_task(step, index)

    part_name = chip.get('fpga', 'partname')

    # Require that a lut size is set for FPGA scripts.
    chip.add('tool', tool, 'task', task, 'require',
             ",".join(['fpga', part_name, 'file', 'bitstream_map']),
             step=step, index=index)


def run(chip):
    part_name = chip.get('fpga', 'partname')

    topmodule = chip.top()
    fasm_file = f"inputs/{topmodule}.fasm"

    bitstream_maps = chip.find_files('fpga', part_name, 'file', 'bitstream_map')

    if len(bitstream_maps) == 1:
        json_outfile = f"outputs/{topmodule}_bitstream.json"
        config_bitstream = fasm_utils.fasm2bitstream(fasm_file, bitstream_maps[0])
        fasm_utils.write_bitstream_json(config_bitstream, json_outfile)
    elif len(bitstream_maps) == 0:
        chip.error("fasm_to_bitstream requires a bitstream map file",
                   fatal=True)
    else:
        chip.error("Only one bitstream map file can be passed to fasm_to_bitstream.py", fatal=True)

    return 0
