# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [

            {'label': 'usb1_read_performance', 'hw_path': ['1-1.1', '2-1.1']},
            {'label': 'usb1_write_performance', 'hw_path': ['1-1.1', '2-1.1']},
            {'label': 'usb2_read_performance', 'hw_path': ['1-1.2', '2-1.2']},
            {'label': 'usb2_write_performance', 'hw_path': ['1-1.2', '2-1.2']},
            {'label': 'usb3_read_performance', 'hw_path': ['1-1.3', '2-1.3']},
            {'label': 'usb3_write_performance', 'hw_path': ['1-1.3', '2-1.3']},
            {'label': 'usb4_read_performance', 'hw_path': ['1-1.4', '2-1.4']},
            {'label': 'usb4_write_performance', 'hw_path': ['1-1.4', '2-1.4']},
            {'label': 'sd_read_performance', 'hw_path': ['mmc0:', 'mmc1:']},
            {'label': 'sd_write_performance', 'hw_path': ['mmc0:', 'mmc1:']},

    ],

    'kr260': [

            {'label': 'usb1_read_performance', 'hw_path': ['3-1.1', '4-1.1']},
            {'label': 'usb1_write_performance', 'hw_path': ['3-1.1', '4-1.1']},
            {'label': 'usb2_read_performance', 'hw_path': ['3-1.2', '4-1.2']},
            {'label': 'usb2_write_performance', 'hw_path': ['3-1.2', '4-1.2']},
            {'label': 'usb3_read_performance', 'hw_path': ['1-1.2', '2-1.2']},
            {'label': 'usb3_write_performance', 'hw_path': ['1-1.2', '2-1.2']},
            {'label': 'usb4_read_performance', 'hw_path': ['1-1.3', '2-1.3']},
            {'label': 'usb4_write_performance', 'hw_path': ['1-1.3', '2-1.3']},
            {'label': 'sd_read_performance', 'hw_path': ['1-1.1']},
            {'label': 'sd_write_performance', 'hw_path': ['1-1.1']},

    ]
}
