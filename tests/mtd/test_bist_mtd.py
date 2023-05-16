# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_mtd import *


@pytest.mark.mtd
def test_mtd(id, helpers):
    """
    Function to parse File System test configurations

    Args:
            id: List of configurations
            helpers: Handle for logging
    """
    # Parse the configurations
    label = id['label']

    if 'read_write_performance' in label:
        mode = 'rw'
        test_result = run_qspi_performance_test(label, mode, helpers)
    elif 'read_performance' in label:
        mode = 'r'
        test_result = run_qspi_performance_test(label, mode, helpers)
    elif 'write_performance' in label:
        mode = 'w'
        test_result = run_qspi_performance_test(label, mode, helpers)
    elif "read_write" in label:
        test_result = run_qspi_read_write_test(label, helpers)
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
