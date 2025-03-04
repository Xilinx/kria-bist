# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import glob
import os
from pymodbus.client import ModbusSerialClient

def get_tty_dev_path(controller_name, logger):
    """
    Fetch the tty dev path for the uart controller name
    Args:
            controller_name: Uart controller name
            logger: Handle for logging
    
    Returns:
            str: Tty dev path or None
    """
    serial_path = f'/sys/devices/platform/axi/{controller_name}.serial/'
    tty_path_list = []
    # Recusrsively walk through directory structure
    for root, dirs, files in os.walk(serial_path):
        # Look for directories that start with 'tty'
        if 'tty' in dirs:
            tty_dir = os.path.join(root, 'tty')
            # Check for files starting with 'tty' within 'tty' directory
            for file in os.listdir(tty_dir):
                if file.startswith('tty'):
                    tty_path_list.append(os.path.join(tty_dir, file))
    if not tty_path_list:
        logger.error("No tty device found for the controller_name: " + controller_name)
        return None
    tty_number = tty_path_list[0].split('/')[-1]
    tty_device_path = f"/dev/{tty_number}"
    logger.debug("Controller_name: " + controller_name + ", tty device path: " + tty_device_path)
    return tty_device_path


def run_rs485_temp_humidity_sensor_read(label, controller_name, helpers):
    """
    Measure Temperate and humidity from RS485-temp sensor
    Args:
            label: Interface under test
            controller_name: Uart controller name
            helpers: Handle for logging
    Returns:
            bool: True if values recorded, False if not
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Fetch the tty dev path for uart controller
    tty_dev_path = get_tty_dev_path(controller_name, logger)
    if tty_dev_path is None:
        return False
    try:
        client = ModbusSerialClient(method='rtu',port=tty_dev_path,baudrate=9600,bytesize=8,parity='N',stopbits=1)
    except:
        logger.error("Connection with RS485 could not be established. Please make sure the sensor is connected correctly")
        return False
    client.connect()
    values = client.read_holding_registers(address=0x0,count=0x4,slave=1)
    if values.isError():
        logger.error("Values were not recorded. Please make sure the sensor is connected correctly")
        logger.test_failed() 
        logger.stop_test()
        return False
    logger.info("Temperature: " + str(values.registers[0] / 10) + " Deg C")
    logger.info("Humidity: " + str(values.registers[1] / 10) + " %")
    client.close()
    logger.test_passed() 
    logger.stop_test()
    return True
