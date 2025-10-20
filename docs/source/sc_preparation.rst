===========================================
 Preparing the Silicon Compiler Run Script
===========================================

Developing a Silicon Compiler run script for RTL-to-bitstream flow execution follows the same fundamental approach as developing a script for any Silicon Compiler flow execution.
Additional resources for understanding Silicon Compiler fundamentals are available at `docs.siliconcompiler.com <https://docs.siliconcompiler.com/en/stable>`_

For most designs, the example Silicon Compiler run scripts provided with Logik can be used as templates for creating your own.
The commands used in these examples and the general method for constructing run scripts are described below.

Constructing a Silicon Compiler run script can be broken down into the following steps:

* :ref:`import_modules`
* :ref:`Create_main_function`
* :ref:`Create_design_object`
* :ref:`Select_part_name`
* :ref:`Import_libraries`
* :ref:`Set_timing_constraints`
* :ref:`Set_pin_constraints`
* :ref:`Create_project_object`
* :ref:`Select_part_name`
* :ref:`Select_flow`
* :ref:`Add_options`
* :ref:`Add_execution_calls`
  
.. _import_modules:

Import Modules
==============

All Silicon Compiler run scripts are pure Python scripts that import Silicon Compiler functionality like any other Python module.
Similarly, the Logik RTL-to-bitstream flow is enabled as a set of Python modules that integrate to Silicon Compiler.

The minimum import requirements in a Logik Silicon Compiler run script are:

::

   import siliconcompiler
   from logik.targets import logik_target


Additional module imports may be required depending on project-specific requirements.

.. _Create_main_function:

Create Main Function
====================

Since the Silicon Compiler run script is just a Python script, executing it from the command line requires the same infrastructure as any other Python script.
In most design flows, the most convenient way to enable this will be to simply encapsulate the script in a `main()` function:

In Python, an executable `main()` function is implemented with the following code:

::

   def main(<main_function_parameters (optional)>):

       #Insert your main function here

   if __name__ == "__main__":
       main()

Experienced Python programmers may prefer to use their own scripting methodology for executing the script instead of the above.
Any approach that conforms to both Python and Silicon Compiler requirements should work.

.. _Create_design_object:

Create Design Object
====================

Silicon Compiler design information is encapsulated in a Python class called Design.

The Design class constructor requires one parameter: the name of the top level module in your RTL design.
A complete Design instantiation takes the form

::

   design = siliconcompiler.Design('<your_top_module_name>')


All design-specific data is housed within this class; it should be the first (or nearly the first) line in your main function.

Throughout this documentation, "design" will be used to refer to the Design class instance.
However, there is no requirement that the instance be assigned to this variable name.

.. _Import_libraries:

Add Source Files
================

All HDL source files must be added to the Silicon Compiler design object for inclusion.  Adding source files is a two-step process:

1.  Set source file data root
2.  Add all source files located at the given data root

The procedure below may be repeated for as many data roots as required.

.. _Set_dataroot:

Setting a Source File Data Root
-------------------------------

Setting a source file data root achieves two goals:

1.  It defines a group of source files housed in a common directory tree as a named IP package in Silicon Compiler
2.  It tells Silicon Compiler where source files are located.  This location could be either a filesystem path or a web URL (e.g. Github repository).

To name a IP package and specify its data root, the `set_dataroot` member function of the Design class is called:
::

    design.set_dataroot(<package_name>, <package_location>, [version])

`<package_name>` is a unique string ID defining the IP package located at `<package_location>`.  `<package_location>` can be either a filesystem path or a URL.  `[version]` is optional, but may be used with package locations that are github repository URLs to specify a particular version (tag or commit hash) of that repository to check out.

.. _Set_input_source_files:

Adding Source Files
-------------------

For each HDL file, include the following call in your Silicon Compiler run script

::

   with design.active_dataroot(<package_name>):
       design.add_file(<your_hdl_file_name>, fileset=<fileset_name>)

Enclosing the `add_file()` call within a `with` statement ensures that, for designs with multiple data roots, the correct data root is applied to each file.  Any number of files with a common data root may be embedded in a single `with` statement.

Specifying a fileset ensures that files within a given IP package are organized and handled correctly by Silicon Compiler.  In the examples provided with Logik, filesets are used to distinguish HDL files from constraint files.  HDL files are assigned to the fileset `rtl`, SDC constraints are assigned to the fileset `sdc`, and pin constraint files to the `pcf` fileset.  For more implementation details concerning filesets, consult `Silicon Compiler fileset documentation <https://docs.siliconcompiler.com/en/latest/reference_manual/schema.html#param-fpgadevice-fileset>`_

.. note::

   Silicon Compiler supports multiple front end options, including flows for high-level synthesis.
   For all front end compilation considerations not described above, please consult `Silicon Compiler Frontend documentation <https://docs.siliconcompiler.com/en/stable/user_guide/tutorials/hw_frontends.html>`_

For large designs, the above calls can be integrated into loops that iterate over lists of files

.. _Set_timing_constraints:

Set Timing Constraints
======================

.. note::

   The demo architecture provided with this distrbution implements a unit delay model.
   Provided examples demonstrate the RTL-to-bitstream flow without an SDC file.

Timing constraints must be provided in a single SDC file.  The SDC file must be added to the Silicon Compiler design object for inclusion.  The API for inclusion is identical to that for adding source files:

::

   with design.active_dataroot(<package_name>):
       design.add_file('<your_sdc_file_name>', fileset=<sdc_fileset>)

.. note::

   If no SDC file is provided, the flow will still run to completion.
   Timing analysis will be disabled during the place and route steps.

.. _Set_pin_constraints:

Set Pin Constraints
===================

Pin constraints may be provided in one of two files:

* A JSON pin constraints file (PCF)
* A VPR XML placement constraints file

.. note::

   If you need to specify placement constraints for design logic blocks in addition to specifying pin constraints, the XML placement constraints file must be used.

JSON Pin Constraint Specification
---------------------------------

The JSON pin constraint file is unique to this flow.
For additional information on creating the JSON pin constraint file, see :doc:`pin_constraints`.

The JSON placement constraints file must be added to the Silicon Compiler design object for inclusion.  The API for inclusion is identical to that for adding source files:

::

   with design.active_dataroot(<package_name>):
      design.add_file('<your_pcf_file_name>', fileset=<pcf_fileset>)

.. note::

   The .pcf file extension must be used

VPR XML Placement Constraint Specification
------------------------------------------

VPR XML placement constraints are portable to any VPR-based place and route flow.
For additional information on creating a VPR XML placement constraint file, see `VPR's documentation for placement constraints <https://docs.verilogtorouting.org/en/latest/vpr/placement_constraints/>`_.

The XML placement constraints file must be added to the Silicon Compiler Design object for inclusion.

::
   
   with design.active_dataroot(<package_name>):
      design.add_file('<your_xml_file_name>', fileset=<xml_fileset>)

in your Silicon Compiler run script.

.. _Create_project_object:

Create Project Object
=====================

Silicon Compiler includes a Project object for encapsulating all aspects of how a design will be implemented.  Like the Design object, the Project is simply a Python class defined in Silicon Compiler.  The primary items encapsulated within the Project are the design data from the Design object described above, the target FPGA device to be used for the project, and settings to control Logik's RTL to bitstream flow.

When using Logik, a specialized Project object for FPGAs is used; this object is of type FPGA.

The FPGA class constructor requires one parameter: an instance of a Design object.  In your run script, you can instantiate this as follows:

::

   project = siliconcompiler.FPGA('<your_design_name>')


Following the variable names used above, `<your_design_name>` would be replaced with `design`.

Add filesets to Project
-----------------------

All filenet names used in specifying design data must be added to the project.  This is done with the Project class's `add_fileset` function.  Typically there will be three filesets to add:  one for HDL files, one for SDC, and one for pin constraints:

::

    project.add_fileset('rtl')
    project.add_fileset('sdc')
    project.add_fileset('pcf')

.. _Select_part_name:

Select Part Name
================

Silicon Compiler associates each FPGA/eFPGA architecture with an object called a part driver.  The part driver is a Python class tailored to that FPGA/eFPGA for housing metadata specific to its architecture.  This metadata includes architecture parameters, associated data files, and other architecture-specific information.

Because part drivers are just Python classes, they can be imported from anywhere.  However, the common case is that the part driver will be imported from `Logiklib <https://github.com/siliconcompiler/logiklib>`_, a dedicated open source Github repository of Logik part drivers and associated CAD files.

At the top of your Python run script, include an `import` statement to import the FPGA part for your project:

::

   from logiklib.<vendor>.<part_name> import <part_name>

The format above illustrates Logiklib's python package organization for part drivers, which is by vendor and then by part name.  For example, to import the Zero ASIC z1000 architecture, the call is

::

   from logiklib.zeroasic.z1000 import z1000

The presense of this `import` statement allows the z1000 FPGA to be selected for use in the project using the `set_fpga()` function:

::

   project.set_fpga(<part_name>)

.. _Select_flow:

Select Flow
===========

Logik's RTL-to-bitstream flow is encapsulated in a Python class called LogikFlow.  This class derives from Silicon Compiler's Flow class.  A project's tool execution flow is selected by passing a Flow object to the project via the `set_flow()` function.  This means that all Logik projects should import Logik's flow:

::

   from logik.flows.logik_flow import LogikFlow

and then set it accordingly:

::

   project.set_flow(LogikFlow())

.. _Add_options:

Add Design and Project Options
==============================

Numerous options can be added to your run script to control Silicon Compiler behavior or configure tools in the RTL-to-bitstream flow to behave as desired.

Some options are configured on a per-design basis; others on a per-project basis.
For complete Silicon Compiler option specifications, refer to `Silicon Compiler's documentation for supported option settings <https://docs.siliconcompiler.com/en/stable/reference_manual/schema.html#param-option-ref>`_.

In particular, any compiler directives that are required for HDL synthesis should be specified as Silicon Compiler options.
These are furnished with Design class member function calls of the form

::

   design.add_define(<compiler_directive>, fileset=<fileset>)


Similarly, any HDL parameters that must be set explicitly for synthesis can be set with the `set_param()` function:

::

   design.set_param(<parameter>, <value>, fileset=<fileset>)

In both cases, `<fileset>` should have the same value as that used for HDL files (e.g. `rtl`).
   
.. _Add_execution_calls:

Add Execution Calls
===================

The final two lines of every run script should be the same:

::
   
   project.run()
   project.summary()
   
The `run()` call invokes the RTL-to-bitstream flow with all settings specified.
The `summary()` call reports results of the run in tabular form.
Included in the summary results are key design metrics such as FPGA resource utilization and tool execution runtimes.
