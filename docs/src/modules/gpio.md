# BIST GPIO Test Module

## Overview

The GPIO module tests the GPIO pins with a loopback test between them.

## Tests

The GPIO module contains one self validating functional test. This test uses the
python3-periphery package. The package sets pins as input/output, writes values
on input pins and reads the same value back on output pins. The total width of
the GPIO is split into two parts out of which one half would be input pins and
other half would be output pins. Values are written based on this. The offset is
basically a pin number from starting offset on the GPIO that is written to or
read from.

The config parameters for this test are described below:

* label: The test label
* width: Width of the GPIO(Total width)
* offset: Offset number of the GPIO(starting offset)

## Test Execution

Example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m gpio              // Run all tests in this module
pytest-3 --board kv260 -k pmod0             // Run individual pmod0 test
```
Each test will print out log messages which include the observations/readings
and the final test result. The live log call will also be available, which can be
found in the automatically generated log file The readings will have the value
that was written, value that was read back and if values match/mismatch. The test
pass/fail depends on whether all the values match/mismatch.
The test typically fails when there is a mismatch between values which typically
means improper loopback connection.

## Test Debug

* Make sure the BIST firmware is loaded
* Make sure the GPIO pins are connected in loopback as mentioned in the target
board's setup page.

## Known Issues and Limitations

The test in the GPIO module is limited to verifying the loopback between input
and output pins

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
