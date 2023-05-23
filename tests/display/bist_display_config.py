# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {'label': 'display_connectivity', 'display_device': 'fd4a0000.display'},
        {'label': 'display_modetest', 'display_device': 'fd4a0000.display', 'fmt': 'AR24'},
    ],
    'kr260': [
        {'label': 'display_connectivity', 'display_device': 'fd4a0000.display'},
        {'label': 'display_modetest', 'display_device': 'fd4a0000.display', 'fmt': 'AR24'},
    ],
}
