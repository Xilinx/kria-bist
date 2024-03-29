# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {
            'label': 'som_eeprom',
            'eeprom_addr': '50',
            'field': 'FRU Board Product Name',
            'value': 'K26'
        },
        {
            'label': 'carrier_card_eeprom',
            'eeprom_addr': '51',
            'field': 'FRU Board Product Name',
            'value': 'KV'
        }
    ],

    'kr260': [
        {
            'label': 'som_eeprom',
            'eeprom_addr': '50',
            'field': 'FRU Board Product Name',
            'value': 'K26'
        },
        {
            'label': 'carrier_card_eeprom',
            'eeprom_addr': '51',
            'field': 'FRU Board Product Name',
            'value': 'KR'
        }
    ],

    'kd240': [
        {
            'label': 'som_eeprom',
            'eeprom_addr': '50',
            'field': 'FRU Board Product Name',
            'value': 'K24'
        },
        {
            'label': 'carrier_card_eeprom',
            'eeprom_addr': '51',
            'field': 'FRU Board Product Name',
            'value': 'KD'
        }
    ]
}
