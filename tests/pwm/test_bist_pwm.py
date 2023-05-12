# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_pwm import *

@pytest.mark.pwm
def test_pwm(id, helpers):
    label = id['label']
    if label == 'fan':
        test_result = run_fancontrol_test(label, helpers)

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
