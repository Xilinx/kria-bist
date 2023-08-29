# BIST SPI Test Module

## Overview

The SPI test module verifies the presence of Torque sensor on the SPI bus of
KD240 starter kit using python-periphery.

## Tests

The module contains self-validating functional tests. The Torque sensor detection is
done with the help of two separate tests by dynamic SPI device path lookup. The
run_torque_sensor_id_test() verifies the Torque sensor AD7797 ID and run_torque_sensor_temp_test()
reads the raw value of inbuilt temperature sensor to verify the Torque sensor presence. The tests
use python-periphery SPI module to perform SPI transactions.

The config parameters for the test are described below:

* label: Test label
* controller: SPI controller address
* channel_select: Channel select of the SPI device
* spi_device: SPI device driver used for the Torque sensor AD7797

The run_torque_sensor_id_test() functional test obtains SPI device path using get_spidev_path()
dynamically during test execution. On obtaining the device path, Torque sensor is initialized by
setting the SPI clock, mode, and sending initialization sequence message using initialize_ad7797_sensor().
The Torque sensor ID read command is sent with the help of spi_transfer_command() function and the response
is analyzed. Similarly, for run_torque_sensor_temp_test(), once the device is initialized, the SPI command
sequence for reading the inbuilt temperature raw value is sent to the SPI device and the response is analyzed. 

## Test Execution

The example commands for this module are provided below:

```bash
pytest-3 --board kd240 -m spi  // Run all tests in this module
pytest-3 --board kd240 -k ad7797_torque_sensor_id_read  // Run Torque sensor ID read test
pytest-3 --board kd240 -k ad7797_torque_sensor_temperature_read  // Run Torque sensor temperature read test
```

For run_torque_sensor_id_test() functional test, the test is passed if the ID read from the SPI device response
matches the expected hex ID value. The test prints out a message indicating a mismatch between expected and obtained
device ID otherwise.

For run_torque_sensor_temp_test() functional test, the test is passed if the response received from the SPI
device is raw temperature value on sending the SPI command sequence for temperature read. The test prints out a
message indicating error in reading the temperature value otherwise.
 
## Test Debug

* Make sure to load the BIST firmware before running the SPI test as the Torque sensor is not detected otherwise.

## Known Issues and Limitations

* The SPI test is limited to verifying the presence of Torque sensor only.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
