# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

ps_i2c_k26_som = {
    'da9062'      : 0x30,
    'da9130'      : 0x32,
    'da9131'      : 0x33,
    'eeprom_som'  : 0x50,
    'slg7x644092' : 0x68,
    'slg7x644091' : 0x70
}

ps_i2c_kv_cc = {
    'usb5477'   : 0x2d,
    'ina260'    : 0x40,
    'eeprom_cc' : 0x51,
    'stdp4320'  : 0x73
}

axi_i2c_kv_cc = {
    'i2c_mux' : 0x74
}

ps_i2c_kr_cc = {
    'slg7xl45106' : 0x11,
    'ina260'      : 0x40,
    'eeprom_cc'   : 0x51,
    'i2c_mux'     : 0x74
}

ps_i2c_k24_som = {
    'da9062'      : 0x30,
    'da9131'      : 0x33,
    'eeprom_som'  : 0x50,
    'slg7x644092' : 0x68,
    'slg7x644091' : 0x70
}

ps_i2c_kd_cc = {
    'slg7xl45106' : 0x11,
    'usb5477'     : 0x2d,
    'ina260'      : 0x40,
    'eeprom_cc'   : 0x51
}

supported_boards = {
    'kv260': [
        {
            'label'       : "ps_i2c_bus_main",
            'controller'  : "ff030000", # Address of the controller
            'mux_channel' : None,
            'i2c_devices' : {**ps_i2c_k26_som, **ps_i2c_kv_cc}
        },
        {
            'label'       : "axi_i2c_bus_main",
            'controller'  : "80030000.i2c", # Address of the controller
            'mux_channel' : None,
            'i2c_devices' : {**axi_i2c_kv_cc}
        },
        {
            'label'       : "axi_i2c_bus_ch0",
            'controller'  : "80030000.i2c", # Address of the controller
            'mux_channel' : 0,
            'i2c_devices' : {**axi_i2c_kv_cc, **{'ap1302' : 0x3c}}
        }
    ],
    'kr260': [
        {
            'label'       : "ps_i2c_bus_main",
            'controller'  : "ff030000", # Address of the controller
            'mux_channel' : None,
            'i2c_devices' : {**ps_i2c_k26_som, **ps_i2c_kr_cc}
        },
        {
            'label'       : "ps_i2c_bus_ch0",
            'controller'  : "ff030000", # Address of the controller
            'mux_channel' : 0,
            'i2c_devices' : {**ps_i2c_k26_som, **ps_i2c_kr_cc, **{'usb5477' : 0x2d}}
        },
        {
            'label'       : "ps_i2c_bus_ch1",
            'controller'  : "ff030000", # Address of the controller
            'mux_channel' : 1,
            'i2c_devices' : {**ps_i2c_k26_som, **ps_i2c_kr_cc, **{'usb5477' : 0x2d}}
        }
    ],
    'kd240': [
        {
            'label'       : "ps_i2c_bus_main",
            'controller'  : "ff030000", # Address of the controller
            'mux_channel' : None,
            'i2c_devices' : {**ps_i2c_k24_som, **ps_i2c_kd_cc}
        }
    ]
}
