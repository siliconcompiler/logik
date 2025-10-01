from siliconcompiler.tools.vpr import VPRFPGA
from siliconcompiler.tools.yosys import YosysFPGA
from siliconcompiler.tools.opensta import OpenSTAFPGA


class LogikFPGA(YosysFPGA, VPRFPGA, OpenSTAFPGA):
    '''
    Class for logik FPGA devices
    '''
    def __init(self):
        super().__init__()

    def set_convert_bitstream_bitstream_map(self, file: str, dataroot: str = None):
        with self.active_dataroot(self._get_active_dataroot(dataroot)):
            return self.set("tool", "convert_bitstream", "bitstream_map", file)