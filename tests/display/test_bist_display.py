# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_display import *


@pytest.mark.display
def test_display(id, helpers):
    """
    Function to parse Display Test Configurations

    Args:
            id: List of configurations
            helpers: Handle for logging
    """
    # Parse the configurations
    label = (id["label"])
    display_device = (id["display_device"])
    # Funtion call to Test DP connectivity
    test_result = run_display_connectivity_test(label, display_device, helpers)

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
