# Copyright (C) 2022 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from gpio import *


@pytest.mark.gpio
def test_gpio(id):
    """
    Function to parse GPIO Configurations

    :arg id: List of configurations

    """
    # Parse the configurations
    width = (id["width"])
    offset = (id["offset"])

    # Function call to Test GPIO Loopback
    run_gpio_loopback(width, offset)
