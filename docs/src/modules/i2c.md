# BIST I2C Test Module

## Overview

The I2C test module verifies the presence of expected devices on the i2c buses of the AMD
Kria&trade; starter kits using python-periphery.

## Tests

The module contains self-validating functional test. It uses "i2cdetect" command-line
utility to check for the i2c bus number based on the controller and mux channel
information. The test then performs i2c read operation on the devices expected to be present
on the identified i2c bus by specifying the device addresses and verifies their presence.

The config parameters for the test are described below:

* label: The test label
* controller: The I2C controller under test
* mux_channel: The channel number of the mux on controller under test
* i2c_devices: The dictionary of I2C devices and their addresses under test

## Test Execution

The example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m i2c  // Run all tests in this module
pytest-3 --board kv260 -k ps_i2c_bus_main  // Run i2c device detect test for PS I2C main bus
pytest-3 --board kv260 -k axi_i2c_bus_main  // Run i2c device detect test for AXI I2C main bus
pytest-3 --board kv260 -k axi_i2c_bus_ch0  // Run i2c device detect test for AXI I2C bus mux channel 0
```

For each bus passed as label, the test prints out message indicating all i2c devices are detected
on the bus in case of pass. Otherwise, it prints out the information about the missing devices name and
addresses along with detected devices.
 
## Test Debug

* Make sure to load the BIST firmware before running the i2c test as some i2c devices are not
  detected otherwise.

## Known Issues

* The i2c test is limited to verifying the presence of i2c devices specified in the configuration
  file on loading the BIST firmware only.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
