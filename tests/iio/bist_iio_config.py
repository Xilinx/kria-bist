# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {
            'label': 'ina260_current',
            'device': 'ina260',
            'channel': 'current0',
            'min_current': 750,
            'max_current': 1050
        }
    ],

    'kr260': [
        {
            'label': 'ina260_current',
            'device': 'ina260',
            'channel': 'current0',
            'min_current': 850,
            'max_current': 1250
        }
    ]
}
