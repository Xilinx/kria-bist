# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_disk import *


@pytest.mark.disk
def test_disk(id, helpers):
    """
    Function to parse File System test configurations

    Args:
            id: List of configurations
            helpers: Handle for logging
    """
    # Parse the configurations
    label = id['label']
    hw_path = id['hw_path']

    if 'read_write_performance' in label:
        mode = 'rw'
    elif 'read_performance' in label:
        mode = 'r'
    elif 'write_performance' in label:
        mode = 'w'
    else:
        assert False

    test_result = run_disk_performance(label, hw_path, mode, helpers)

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result