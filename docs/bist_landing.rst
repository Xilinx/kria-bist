#####################################################
BIST
#####################################################


The Built-In Self Test (BIST) application tests the interfaces on AMD Kria™ starter kits to verify functionality and/or performance. If a custom design is not working as expected, this application can be used to differentiate hardware issues from design issues.

The BIST application is based on the pytest framework and designed to be modular and configurable so that it can be used across different starter kits. The tests are grouped into modules based on the interface which allows testing individual interfaces if needed. Some tests are self-validating tests, while others require user input based on observation. Each individual test either verifies the functionality or performance of an interface.



.. toctree::
   :maxdepth: 1
   :caption: Quick Start

   Install and Run BIST <docs/run.md>


.. toctree::
   :maxdepth: 1
   :caption: Overview

   Overview of BIST Application <docs/overview.rst>


.. toctree::
   :maxdepth: 1
   :caption: Other

   Known Issues <docs/known_issues.md>

.. toctree::
   :maxdepth: 1
   :caption: Repository

   Software Repository <https://github.com/Xilinx/kria-bist>


Support
=================================================================

GitHub issues will be used for tracking requests and bugs. For questions, go to `forums.xilinx.com <http://forums.xilinx.com/>`_.


..
  Copyright © 2023 Advanced Micro Devices, Inc

..
  `Terms and Conditions <http://forums.xilinx.com/>`_
