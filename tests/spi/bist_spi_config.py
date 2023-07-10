# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kd240': [
        {
            'label': 'ad7797_torque_sensor_id_read',
            'controller': 'a0060000',
            'channel_select': '0',
            'spi_device': 'dh2228fv'  # Spi device driver used for the torque sensor AD7797
        },
        {
            'label': 'ad7797_torque_sensor_temperature_read',
            'controller': 'a0060000',
            'channel_select': '0',
            'spi_device': 'dh2228fv'  # Spi device driver used for the torque sensor AD7797
        }
    ]
}
