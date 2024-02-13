#ebrick_fpga_flow.py

import siliconcompiler
import re

from siliconcompiler import SiliconCompilerError
from siliconcompiler.flows._common import setup_frontend

from siliconcompiler.tools.yosys import syn_fpga as yosys_syn
from siliconcompiler.tools.vpr import place as vpr_place
from siliconcompiler.tools.vpr import route as vpr_route
from siliconcompiler.tools.genfasm import bitstream as genfasm_bitstream

from ebrick_fpga_cad.tools.fasm_to_bitstream import bitstream_finish
from ebrick_fpga_cad.tools.generate_vpr_constraints import constraint_gen

############################################################################
# DOCS
############################################################################
def make_docs(chip):
    return setup(chip)


############################################################################
# Flowgraph Setup
############################################################################
def setup(chip, flowname='ebrick_fpga_flow'):
    '''

    '''

    flow = siliconcompiler.Flow(chip, flowname)

    flow_pipe = flow_lookup()

    flowtools = setup_frontend(chip)
    flowtools.extend(flow_pipe)

    # Minimal setup
    index = '0'
    prevstep = None
    for step, tool_module in flowtools:
        # Flow
        flow.node(flowname, step, tool_module)
        if prevstep:
            flow.edge(flowname, prevstep, step)
        # Hard goals
        for metric in ('errors', 'warnings', 'drvs', 'unconstrained',
                       'holdwns', 'holdtns', 'holdpaths',
                       'setupwns', 'setuptns', 'setuppaths'):
            flow.set('flowgraph', flowname, step, index, 'goal', metric, 0)
        # Metrics
        for metric in ('luts', 'dsps', 'brams', 'registers',
                       'pins', 'peakpower', 'leakagepower'):
            flow.set('flowgraph', flowname, step, index, 'weight', metric, 1.0)
        prevstep = step

    return flow


##################################################
def flow_lookup():
    
    flow = [
        ('syn', yosys_syn),
        ('constraint_gen', constraint_gen),
        ('place', vpr_place),
        ('route', vpr_route),
        ('genfasm', genfasm_bitstream),
        ('bitstream', bitstream_finish),
    ]
    
    return flow


##################################################
if __name__ == "__main__":
    flow = make_docs(siliconcompiler.Chip('<flow>'))
    flow.write_flowgraph(f"{flow.top()}.png", flow=flow.top())
