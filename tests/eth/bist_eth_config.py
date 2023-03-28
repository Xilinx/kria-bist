# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {'label': 'ethernet1_ping', 'phy_addr': '1'},
        {'label': 'ethernet1_perf', 'phy_addr': '1'}
    ],

    'kr260': [
        {'label': 'ethernet1_ping', 'phy_addr': '2'},
        {'label': 'ethernet1_perf', 'phy_addr': '2'},
        {'label': 'ethernet2_ping', 'phy_addr': '3'},
        {'label': 'ethernet2_perf', 'phy_addr': '3'},
        {'label': 'ethernet3_ping', 'phy_addr': '4'},
        {'label': 'ethernet3_perf', 'phy_addr': '4'},
        {'label': 'ethernet4_ping', 'phy_addr': '8'},
        {'label': 'ethernet4_perf', 'phy_addr': '8'}
    ]
}
