# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

device_config = {
    'zynqmp': {
        'dt_node': 'fd4a0000.display',
        'drivers': [{'xlnx-drm' : 'xlnx'}, {'zynqmp-dpsub': 'zynqmp-dpsub'}],
    },
}

supported_boards = {
    'kv260': [
        {'label': 'display_connectivity', 'display_device': 'zynqmp'},
        {'label': 'display_modetest', 'display_device': 'zynqmp', 'fmt': 'AR24'},
    ],
    'kr260': [
        {'label': 'display_connectivity', 'display_device': 'zynqmp'},
        {'label': 'display_modetest', 'display_device': 'zynqmp', 'fmt': 'AR24'},
    ],
}
