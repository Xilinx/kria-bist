# Copyright (C) 2022-2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
import logging
from gpio import *

logger = logging.getLogger(__name__)

@pytest.mark.gpio
def test_gpio(id):
    """
    Function to parse GPIO Configurations
    
    Args:
            id: List of configurations

    """
    # Parse the configurations
    width = (id["width"])
    offset = (id["offset"])

    # Function call to Test GPIO Loopback
    run_gpio_loopback(width, offset, logger)
