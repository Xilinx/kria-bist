#####################################################
BIST Overview
#####################################################


The Built-In Self Test (BIST) application tests the interfaces on Kria starter kits to verify functionality and/or performance. If a custom design is not working as expected, this application can be used to differentiate hardware issues from design issues.

The BIST application is based on the pytest framework and designed to be modular and configurable so that it can be used across different starter kits. The tests are grouped into modules based on the interface which allows testing individual interfaces if needed. Some tests are self-validating tests, while others require user input based on observation. Each individual test either verifies the functionality or performance of an interface.




**************************************************************************
Framework
**************************************************************************


The Built-In Self Test (BIST) application is based on the `pytest <https://pytest.org/>`_ framework. Pytest allows `parametrizing <https://docs.pytest.org/parametrize.html>`_ the test functions so that they can be reused across different boards and interfaces. The tests are enumerated based on the target board and the user can choose to run all tests for the target board, selected test modules, or selected individual tests. The file structure is described in the next section.



**************************************************************************
File Structure
**************************************************************************


The source code for the BIST application can be found in the `kria-bist <https://github.com/Xilinx/kria-bist>`_ repository. The tests directory contains
a module directory for each interface, along with a top level conftest.py and
pytest.ini.

The top level conftest.py implements a Helpers class which contains helper
functions that can be used by all other test functions. This file also adds
an option to specify the target board when running pytest.

The pytest.ini file defines markers that can be used when running pytest. Each
module has a marker which can be used to run tests for the selected module(s).
The logging configuration for the test output is also defined here. By default,
INFO level (or higher) messages will be printed to the terminal and the log
file, and DEBUG level messages will only be printed to the log file.
This file also defines the command line options that are used every time pytest
is called from the tests directory.

Each test module contains 4 files: bist_module.py, bist_module_config.py,
conftest.py, and test_bist_module.py, where module is the name of the module.

The module level conftest.py contains a function which parametrizes the tests
based on the target board and the parameters in bist_module_config.py.

The bist_module_config.py contains a dictionary of supported boards for that
module. There is a key for each supported board and each key maps to a list of
tests. The length of this list corresponds to the number of tests that will be
generated for the target board and module. Each item in this list is a
dictionary which contains a label and other test-specific parameters. The label
is seen in the pytest output and can be used to differentiate individual tests.

The bist_module.py contains helper functions and run functions. The run
functions perform a specific test based on the parameters it is given and
return True or False.

The test_bist_module.py contains the test function called by pytest. The test
function receives all the parameters from the config file and uses the label
parameter to determine which run function should be called for each test. Once
the run function returns either True or False, the test function asserts this
value and this determines whether a test passed or failed.


**************************************************************************
Test Modules
**************************************************************************


The test modules are listed below. Please refer to the individual module pages for more details.


.. toctree::
   :maxdepth: 1

   Disk Test Module <modules/disk.md>
   Display Test Module <modules/display.md>
   EEPROM Test Module <modules/eeprom.md>
   Ethernet Test Module <modules/eth.md>
   GPIO Test Module <modules/gpio.md>
   I2C Test Module <modules/i2c.md>
   IIO Test Module <modules/iio.md>
   MTD Test Module <modules/mtd.md>
   PWM Test Module <modules/pwm.md>
   TPM Test Module <modules/tpm.md>
   Video Test Module <modules/video.md>



Support
=================================================================

GitHub issues will be used for tracking requests and bugs. For questions, go to `forums.xilinx.com <http://forums.xilinx.com/>`_.






..
  Copyright © 2023 Advanced Micro Devices, Inc

..
  `Terms and Conditions <http://forums.xilinx.com/>`_
