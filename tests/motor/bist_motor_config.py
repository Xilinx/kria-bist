# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kd240': [
        {
            'label': 'qei_gate_drive_test',
            'speed': 5000
        },
        {
            'label': 'volt_adc_fb_modeopenloop_test',
            'speed': 5000
        },
        {
            'label': 'curr_adc_fb_modeopenloop_test',
            'speed': 5000
        },
        {
            'label': 'volt_adc_fb_modeoff_test'
        },

        {
            'label': 'curr_adc_fb_modeoff_test'
        },
        {
            'label': 'dc_link_volt_adc_fb_test'
        },
        {
            'label': 'dc_link_curr_adc_fb_test'
        }
    ]
}
