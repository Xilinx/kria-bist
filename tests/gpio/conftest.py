# Copyright (C) 2022 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for execution
import pytest


# Supported Boards
supported = {
    'kv260': [
        {'label': 'pmod0', 'width': '8', 'offset': '0'},
    ],

    'kd240': [
        {'label': 'pmod0', 'width': '8', 'offset': '0'},
        {'label': 'gate_drive_en', 'width': '1', 'offset': '8'},
        {'label': 'brake_cntrl', 'width': '1', 'offset': '9'},
        {'label': 'one_wire', 'width': '1', 'offset': '10'},
    ],

    'kr260': [
        {'label': 'pmod0', 'width': '8', 'offset': '0'},
        {'label': "pmod1", 'width': '8', 'offset': '8'},
        {'label': "pmod2", 'width': '8', 'offset': '16'},
        {'label': "pmod3", 'width': '8', 'offset': '24'},
        {'label': "rpi", 'width': '28', 'offset': '32'},
    ]
}


def pytest_generate_tests(metafunc):
    """
    Collection and parametrization of tests

    :arg metafunc: has a parametrize function,way to provide multiple variants of values for parametrization
    :list val: Lookup for board parameters
    :list test_id: Lookup for Test labels. Tests are parametrized based on label

    """
    board = metafunc.config.getoption("board")
    val = []
    test_id = []

    # Create a list of configs(based on the board) and test IDs for parametrization
    if board in supported.keys():
        val = supported[board]
        for value in supported[board]:
            test_id.append(value['label'])

    else:
        val = pytest.skip("Not supported")

    # Parametrize tests based on test IDs
    metafunc.parametrize("id", val, ids=test_id)
