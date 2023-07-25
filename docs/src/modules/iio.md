# BIST IIO Test Module

## Overview

This module verifies values read from the starter kit's IIO devices.

## Tests

The IIO module contains a single self-validating functional test. This test
uses the libiio python bindings to read a value from a specified IIO device and
verify that it is within the range specified in the config.

The config parameters for this test are described below:

* label: The test label
* device: The name of the IIO device
* channel: The name of the current channel
* min_current: The lower limit for the reading
* max_current: The upper limit for the reading

## Test Execution

Example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m iio			// Run all tests in this module
pytest-3 --board kv260 -k ina260_current	// Run ina260_current test
```

This test will print out the measured value and pass if it is within the
expected range.

## Test Debug

* Make sure the BIST firmware is loaded since the readings can vary for
  different designs.

## Known Issues and Limitations

* The ina260_current test is limited to verifying the current value read from
  the INA260 while the BIST firmware is loaded.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
