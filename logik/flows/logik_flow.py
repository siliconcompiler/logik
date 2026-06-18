# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

from siliconcompiler.flows import fpgaflow
from siliconcompiler.tools.vpr.place import PlaceTask
from siliconcompiler.tools.vpr.route import RouteTask

from logik.tools.fasm_to_bitstream import bitstream_finish


class LogikPlaceTask(PlaceTask):
    """VPR place task with the design-image dump disabled.

    See :class:`LogikRouteTask` for why the image dump is turned off.
    """

    def __init__(self) -> None:
        super().__init__()
        self.set("var", "enable_images", False)


class LogikRouteTask(RouteTask):
    """VPR route task with the design-image dump disabled.

    VPR's ``--graphics_commands ... save_graphics`` image dump runs at the end
    of both the place and route steps. ``get_unique_pb_graph_node_id``
    null-derefs on a clock-only pb_graph_node while laying out the image,
    segfaulting both steps on parts that have such a node (e.g. z1015). The
    image is only a debug artifact, so the Logik flow disables it for every
    part. Parts that never hit the crash are unaffected -- they simply skip a
    layout image they did not depend on.
    """

    def __init__(self) -> None:
        super().__init__()
        self.set("var", "enable_images", False)


class LogikFlow(fpgaflow.FPGAVPROpenSTAFlow):
    """An open-source FPGA flow using Yosys, VPR, and GenFasm.

    This flow is designed for academic and research FPGAs, utilizing VPR
    (Versatile Place and Route) for placement and routing.

    The flow consists of the following steps:

    * **elaborate**: Elaborate the RTL design from sources.
    * **synthesis**: Synthesize the elaborated design into a netlist using Yosys.
    * **place**: Place the netlist components onto the FPGA architecture using VPR.
    * **route**: Route the connections between placed components using VPR.
    * **timing**: Perform static analysis using OpenSTA.
    * **bitstream**: Generate the final bitstream using GenFasm.
    * **convert_bitstream**: Format bitstream from fasm to bits.

    The VPR place and route steps run with the design-image dump disabled (see
    :class:`LogikRouteTask`); previously this was applied per-project by the
    z1015 part driver's ``configure_vpr`` helper.
    """

    def __init__(self, name: str = "logik_flow") -> None:
        """
        Initializes the FPGAVPRFlow.

        Args:
            name (str): The name of the flow.
        """
        super().__init__(name)

        # Swap the stock VPR place/route tasks for the Logik variants that
        # disable the crashing graphics dump. Re-binding the existing nodes
        # keeps the edges set up by the parent flow intact.
        self.node("place", LogikPlaceTask())
        self.node("route", LogikRouteTask())

        self.node("convert_bitstream", bitstream_finish.BitstreamFinishTask())
        self.edge("bitstream", "convert_bitstream")


if __name__ == "__main__":
    LogikFlow().write_flowgraph(f"{LogikFlow().name}.png")
