# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_i2c import *


@pytest.mark.i2c
def test_i2c(id, helpers):
    """
    Function to parse File System test configurations

    Args:
            id: List of configurations
            helpers: Handle for logging
    """
    # Parse the configurations
    label = id['label']
    controller = id['controller']
    mux_channel = id['mux_channel']
    i2c_devices = id['i2c_devices']

    test_result = run_i2c_device_detect_test(label, controller, mux_channel, i2c_devices, helpers)

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
