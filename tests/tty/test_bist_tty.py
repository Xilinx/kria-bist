# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_tty import *

@pytest.mark.tty
def test_tty(id, helpers):
    label = id['label']
    controller_name = id['controller_name']

    assert run_rs485_temp_humidity_sensor_read(label, controller_name, helpers)
