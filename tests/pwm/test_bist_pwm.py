# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_pwm import *

@pytest.mark.pwm
def test_pwm(id, helpers):
    if id['label'] == 'fan':
        assert run_fancontrol_test(id['label'], helpers)
