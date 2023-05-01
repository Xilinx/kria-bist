# Copyright (C) 2022-2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for execution
import pytest
from bist_mtd_config import supported_boards


def pytest_generate_tests(metafunc):
    """
    Collection and parametrization of tests

    Args:
            metafunc: Has a parametrize function,way to provide multiple variants of values for parametrization

    Data Structure:
            val(list): Lookup for board parameters
            test_id(list): Lookup for Test labels.Tests are parametrized based on label

    """
    board = metafunc.config.getoption("board")
    val = []
    test_id = []

    # Create a list of configs(based on the board) and test IDs for parametrization
    if board in supported_boards.keys():
        val = supported_boards[board]
        for value in supported_boards[board]:
            test_id.append(value['label'])

    else:
        val = pytest.skip("Not supported")

    # Parametrize tests based on test IDs
    metafunc.parametrize("id", val, ids=test_id)