# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_eth import *

@pytest.mark.eth
def test_eth(id, helpers):
    label = id['label']
    phy_addr = id['phy_addr']
    if 'ping' in label:
        test_result = run_eth_ping_test(label, phy_addr, helpers)
    elif 'perf' in label:
        test_result = run_eth_perf_test(label, phy_addr, helpers)
    else:
        assert False

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
