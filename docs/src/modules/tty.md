# BIST Tty Test Module

## Overview

This module tests the tty interface(s) on the AMD Kria&trade; starter kits.

## Tests

The Tty module contains one self-validating test. This test uses the pymodbus
python package. The package establishes a client connection with the connected
RS485 temperature sensor's tty terminal and reads the holding registers 
containing the temperature and humidity values.

The config parameters for this test are described below:
   * label: The test label
   * controller_name: Uart controller name

## Test Execution

The example commands for this module are provided below (KD240):

```bash
pytest-3 --board kd240 -m tty                                     // Run all tests in this module
pytest-3 --board kd240 -k rs485_temp_humidity_sensor_read         // Run inidvidual test
```
The test prints out the log messages that include the readings from the sensor
and final test result. The readings have the temperature and humidity 
values recorded by the sensor. The test pass depends on the successful reading 
of both the values. The test typically fails when the connection with the serial 
client could not be established or values were not recorded; this typically 
points to improper connections.

## Test Debug

* Make sure that the BIST firmware is loaded.
* Make sure that the sensor is connected correctly.

## Known Issues and Limitations

* Occasionally, erroneous values (for example 3276.8) are reported for 
temperature/humidity sensor data and this is due to error in the sensor itself, 
which can be ignored and the test rerun to clear the error.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
