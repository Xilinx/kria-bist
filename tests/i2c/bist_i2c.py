# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import periphery
import re


def i2c_bus_lookup(controller, mux_channel, logger):
    """
    I2C bus lookup

    Args:
            controller: I2C controller
            mux_channel: Channel number of the mux on controller
            logger: Calling function's logger object

    Returns:
            str: I2C bus number
    """
    i2cdetect_cmd = "i2cdetect -l"  # List I2C buses on the board
    i2cdetect_result = subprocess.run(i2cdetect_cmd.split(), capture_output=True, text=True)
    if i2cdetect_result.returncode:
        logger.error(f"Error executing command: {i2cdetect_cmd}")
        return None
    output_lines = i2cdetect_result.stdout.splitlines()
    i2c_bus_number = None
    for line in output_lines:
        if controller in line:
            i2c_bus_number = re.match(r"i2c-(\d+)",line).group(1)
            break
    if not i2c_bus_number:
        logger.error(f"I2C bus could not be detected for controller {controller}")
        return None
    if mux_channel is None:
        logger.debug(f"I2C bus of controller {controller}: i2c-{i2c_bus_number}")
        return i2c_bus_number
    mux_pattern = f"i2c-{i2c_bus_number}-mux \\(chan_id {mux_channel}\\)"
    for line in output_lines:
        if re.search(mux_pattern, line):
            i2c_bus_number = re.match(r"i2c-(\d+)",line).group(1)
            logger.debug(f"I2C bus of mux channel {mux_channel} on controller {controller}: i2c-{i2c_bus_number}")
            return i2c_bus_number
    logger.error(f"I2C bus could not be detected for mux channel {mux_channel} on controller {controller}")
    return None


def check_i2c_device(i2c_devices, i2c_bus_number, logger):
    """
    Check for I2C devices on the bus

    Args:
            i2c_devices: Dictionary of I2C devices and their addresses under test
            i2c_bus_number: To check for I2C devices on the bus
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    i2c_bus = periphery.I2C(f"/dev/i2c-{i2c_bus_number}")  # Open the I2C bus with given bus number
    all_i2c_devices_present = True
    for device_type, device_address in i2c_devices.items():
        try:
            # Try to read a byte from the address passed in the dictionary
            i2c_bus.transfer(device_address, [periphery.I2C.Message([0x00], read=True)])
            logger.debug(f"Device '{device_type}' detected at address {hex(device_address)}")
        except Exception:
            # Exception occurs when device is not found
            logger.error(f"Device '{device_type}' could not be detected on i2c-{i2c_bus_number} bus at expected device address {hex(device_address)}")
            all_i2c_devices_present = False
    i2c_bus.close()  # Close the I2C bus with given bus number
    if not all_i2c_devices_present:
        return False
    return True


def run_i2c_device_detect_test(label, controller, mux_channel, i2c_devices, helpers):
    """
    I2C device detect test

    Args:
            label: Test label
            controller: I2C controller
            mux_channel: Channel number of the mux on controller
            i2c_devices: Dictionary of I2C devices and their addresses under test
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Obtain I2C bus number based on the controller and mux channel
    i2c_bus_number = i2c_bus_lookup(controller, mux_channel, logger)
    if i2c_bus_number is None:
        return False
    # Check for I2C devices on the bus
    devices_found = check_i2c_device(i2c_devices, i2c_bus_number, logger)
    if devices_found is False:
        return False
    logger.info(f"All expected I2C devices on the bus have been successfully detected")
    return True