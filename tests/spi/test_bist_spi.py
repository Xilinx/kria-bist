# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_spi import *


@pytest.mark.spi
def test_spi(id, helpers):
    """
    Function to parse File System test configurations

    Args:
            id: List of configurations
            helpers: Handle for logging
    """
    # Parse the configurations
    label = id['label']
    controller = id['controller']
    channel_select = id['channel_select']
    spi_device = id['spi_device']
    if label == 'ad7797_torque_sensor_id_read':
        test_result = run_ad7797_id_test(label, controller, channel_select, spi_device, helpers)
    elif label == 'ad7797_torque_sensor_temperature_read':
        test_result = run_ad7797_temperature_test(label, controller, channel_select, spi_device, helpers)
    else:
        assert False

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
