# BIST Tty Test Module

## Overview

This module tests the tty interface(s) on the AMD Kria&trade; starter kits.

Note that this test is expected to fail in on KD240 with Ubuntu classic-22.04-kd05 version as the RS485 driver is in the process of being upstreamed for certified Ubuntu image. This test will still pass with Ubuntu 22.04-kd03 image on KD240, and it will also pass for KR260's RS485 over AXI lite interface.

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
* RS485 does not function in Ubuntu 22.04 kd05 as the driver is in the process of 
being upstreamed. The driver is also [not present in PetaLinux 2023.2 KD240 BSP](https://support.xilinx.com/s/article/000035701?language=en_US). Thus, this test is expected to fail in that version.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
