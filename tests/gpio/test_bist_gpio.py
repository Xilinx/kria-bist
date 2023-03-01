# Copyright (C) 2022-2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_gpio import *


@pytest.mark.gpio
def test_gpio(id, helpers):
    """
    Function to parse GPIO Configurations

    Args:
            id: List of configurations
            helpers: Handle for logging

    """
    # Parse the configurations
    label = (id["label"])
    width = (id["width"])
    offset = (id["offset"])

    # Function call to Test GPIO Loopback
    assert run_gpio_loopback(label, width, offset, helpers)
