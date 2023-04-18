# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {'label': 'pmod0', 'width': 8, 'offset': '0'},
    ],

    'kd240': [
        {'label': 'pmod0', 'width': 8, 'offset': '0'},
        {'label': 'gate_drive_en', 'width': 1, 'offset': '8'},
        {'label': 'brake_cntrl', 'width': 1, 'offset': '9'},
        {'label': 'one_wire', 'width': 1, 'offset': '10'},
    ],

    'kr260': [
        {'label': 'pmod0', 'width': 8, 'offset': '0'},
        {'label': 'pmod1', 'width': 8, 'offset': '8'},
        {'label': 'pmod2', 'width': 8, 'offset': '16'},
        {'label': 'pmod3', 'width': 8, 'offset': '24'},
        {'label': 'rpi', 'width': 28, 'offset': '32'},
    ]
}
