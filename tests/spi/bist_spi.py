# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import periphery
import time
import glob
import re


def get_spidev_path(controller, spi_device, channel_select, device_name, logger):
    """
    Get SPI device path

    Args:
            controller: SPI controller responsible for the device
            spi_device: SPI device driver
            channel_select: Slave channel select
            device_name: SPI device name
            logger: Calling function's logger object

    Returns:
            str: SPI device path
    """
    spi_path = f'/sys/devices/platform/axi/{controller}.axi_quad_spi/spi_master/spi*/spi*/modalias'
    spidev_match_paths = glob.glob(spi_path)
    for path in spidev_match_paths:
        with open(path, 'r') as file:
            content = file.read()
        if spi_device in content:
            spi_bus = re.search(r'spi(\d+)', path).group(1)
            if spi_bus is not None:
                logger.info(f"Device {device_name} detected on SPI bus {spi_bus} with slave select channel {channel_select}")
                spi_dev_path = f"/dev/spidev{spi_bus}.{channel_select}"  # To choose spi bus & device (chip select)
                return spi_dev_path
    logger.error(f"Device {device_name} could not be detected on the SPI bus")
    return None


def initialize_ad7797_sensor(spi_dev_path, logger):
    """
    Initialize Torque sensor

    Args:
            spi_dev_path: SPI device path of the Torque sensor
            logger: Calling function's logger object

    Returns:
            periphery: SPI device object
    """
    spi_mode = 0  # To choose spi mode 0
    speed_hz = 1000000  # Set clock frequency to 1MHz
    try:
        # Create a SPI device object
        spi_dev = periphery.SPI(spi_dev_path, spi_mode, speed_hz)
        logger.debug(f"Opened SPI communication for Torque sensor on {spi_dev_path}")
    except periphery.spi.SPIError as e:
        logger.error(f"Error opening SPI communication for Torque sensor on {spi_dev_path} - {e}")
        return None
    # Reset Torque sensor
    try:
        spi_dev.transfer([0xFF, 0xFF, 0xFF, 0xFF])
        logger.info(f"Initialized Torque sensor on {spi_dev_path}")
        return spi_dev
    except periphery.spi_dev.SPIError as e:
        logger.error(f"Error: SPI communication failed for sensor reset - {e}")
        return None


def spi_transfer_command(spi_dev, spi_command, logger):
    """
    SPI command transfer

    Args:
            spi_dev: SPI device object
            spi_command: SPI command to be sent to the device
            logger: Calling function's logger object

    Returns:
            str: SPI device response to the command
    """
    try:
        response = spi_dev.transfer(spi_command)
        spi_command_hex = ', '.join([hex(val) for val in spi_command])
        response_hex = ', '.join([hex(val) for val in response])
        logger.debug(f"SPI command sent: {spi_command_hex}")
        logger.debug(f"Response received: {response_hex}")
        return response
    except periphery.spi_dev.SPIError as e:
        logger.error(f"Error: SPI communication failed for command: {spi_command} - {e}")
        return None


def run_ad7797_id_test(label, controller, channel_select, spi_device, helpers):
    """
    Torque sensor ID read test

    Args:
            label: Test label
            controller: SPI controller responsible for torque sensor
            channel_select: Torque sensor slave select channel
            spi_device: Torque sensor device driver
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    spi_torque_sensor_id = '0x5b'
    # Get spi device path of the form /dev/spidevX.Y - X represents spi bus and Y represents slave channel select
    spi_dev_path = get_spidev_path(controller, spi_device, channel_select, "AD7797", logger)
    if spi_dev_path is None:
        return False
    # Obtain spi device object on initializing Torque sensor
    spi_dev = initialize_ad7797_sensor(spi_dev_path, logger)
    if spi_dev is None:
        return False
    # Spi command to read ID register on the device
    spi_read_id_command = [0x60,0x80]
    spi_response = spi_transfer_command(spi_dev, spi_read_id_command, logger)
    if spi_response is None:
        return False
    logger.info(f"Expected device ID for the sensor AD7797: {spi_torque_sensor_id}")
    # Consider the response from second index [1] as device responds with a default/dummy byte on index [0]
    id_read = hex(spi_response[1])
    logger.info(f"Obtained device ID: {id_read}")
    if id_read != spi_torque_sensor_id:
        logger.error(f"Torque sensor AD7797 ID read does not match the expected ID value")
        return False
    logger.info(f"Torque sensor AD7797 ID read successful. Obtained ID value matches the expected ID value")
    return True


def run_ad7797_temperature_test(label, controller, channel_select, spi_device, helpers):
    """
    Torque sensor temp read test

    Args:
            label: Test label
            controller: SPI controller responsible for torque sensor
            channel_select: Torque sensor slave select channel
            spi_device: Torque sensor device driver
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Get spi device path of the form /dev/spidevX.Y for X represents spi bus and Y represents slave channel select
    spi_dev_path = get_spidev_path(controller, spi_device, channel_select, "AD7797", logger)
    if spi_dev_path is None:
        return False
    # Obtain spi device object on initializing Torque sensor
    spi_dev = initialize_ad7797_sensor(spi_dev_path, logger)
    if spi_dev is None:
        return False
    '''
       Spi commands to read temperature from the Torque sensor:
            1: Write configuration register - [0x10, 0x17, 0x16, 0x80]
            2: Read configuration register - [0x50, 0x80, 0x80] (Verify config register data for debug purpose only)
            3: Read temperature from data register - [0x58, 0x80, 0x80, 0x80]
    '''
    # Spi command to write configuration register
    spi_write_conf_command = [0x10, 0x17, 0x16, 0x80]
    spi_write_conf_response = spi_transfer_command(spi_dev, spi_write_conf_command, logger)
    if spi_write_conf_response is None:
       return False
    # Spi command to read configuration register
    spi_read_conf_command = [0x50, 0x80, 0x80]
    spi_read_conf_response = spi_transfer_command(spi_dev, spi_read_conf_command, logger)
    if spi_read_conf_response is None:
        return False
    # Sleep for 1s before reading the temperature in order to avoid reading incorrect values
    time.sleep(1)
    # Spi command to read temperature from data register
    spi_read_temp_command = [0x58, 0x80, 0x80, 0x80]
    spi_read_temp_response = spi_transfer_command(spi_dev, spi_read_temp_command, logger)
    if spi_read_temp_response is None:
        return False
    # Consider the response from second index [1] as device responds with a default/dummy byte on index [0]
    formatted_temp_values = []
    # The response from data register consists of 4 bytes of data. Join each byte to obtain temperature raw value
    for temp_value in spi_read_temp_response[1:]:
        formatted_temp_value = format(temp_value, '02X')
        formatted_temp_values.append(formatted_temp_value)
    spi_temp_response_str = ''.join(formatted_temp_values)
    logger.debug(f"Raw temperature value from data register: {spi_temp_response_str}")
    # On PowerOn/Reset default value on data register is 0x000000.
    # Hence, response of all '0's or 'F's indicates failure to initiate temp read/ incorrect response
    if (spi_temp_response_str == 0x000000) or (spi_temp_response_str == 0xFFFFFF):
        logger.error(f"Error reading temperature of Torque sensor AD7797")
        return False
    logger.info(f"Torque sensor AD7797 temperature read successful")
    return True
