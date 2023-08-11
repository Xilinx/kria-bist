# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kd240': [
        {
            'label': 'can_bus_send',  # Send CAN messages from PS CAN
            'can_transmitter': 'zynq-can',  # PS CAN controller
            'can_receiver': 'mcp25625',   # AXI CAN controller
        },
        {
            'label': 'can_bus_receive',  # Receive CAN messages to PS CAN
            'can_transmitter': 'mcp25625',
            'can_receiver': 'zynq-can',
        }
    ]
}
