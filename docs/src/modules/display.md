# BIST Display Test Module

## Overview

This module verifies the connectivity and functionality of display device connected to the AMD
Kria&trade; starter kits.

## Tests

There are two tests for each board. One of them is a self-validating functional
test and the other is a user-validating functional test. The tests use the
libdrm-tests(modetest command) to test this module.

* run_display_connectivity_test: Self-validating test that verifies the cable
connectivity by reading the 'EDID' value.
   
   The test reads the 'EDID' value from the display device and logs it. If the EDID 
   value is read successfully, the test is a pass or else it is marked
   as fail. The EDID value in KV260 is read from the DP splitter on the KV Carrier
   Card and not from the monitor. In this case, the connectivity test is still
   a Pass if the DP/HDMI cable is disconnected for subsequent
   display_connectivity test. The EDID value in KR260 is read from the Monitor.
   So connection/disconnection of Display Port cable decides EDID value's 
   existence.

* run_display_modetest: User-validating test that drives a test pattern on the
monitor and checks with the user if it was observed.

   The test drives a test pattern on the Monitor and you are asked a 
   question[Y/N] on the output console if the pattern was observed. The test
   result is based on your observation.

The config parameters for each test are described below:

* label: The test label
* display_device: DP name of display device
* fmt: Display format value(for display_modetest)

## Test Execution

The example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m display                // Run all tests in this module
pytest-3 --board kv260 -k display_modetest       // Run display_modetest test
```
Each test prints out the log messages that include the readings or a question
and User Input(for User Validating test) and the final test result. The 
display_connectivity also logs debug level messages with additional info,
which can be found in the automatically generated log file.

## Test Debug

* Make sure that the BIST firmware is loaded.
* Make sure that the desktop is disabled before running this module.
* Make sure that you have the correct input source selected on the Monitor.

## Known Issues and Limitations

* On KV260, EDID is read from the DP splitter on the SOM and not from Monitor.
In this case, the connectivity test is still a Pass if the DP/HDMI cable is
disconnected for subsequent display_connectivity test runs.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
