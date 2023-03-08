# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_tpm import *

@pytest.mark.tpm
def test_tpm(id, helpers):
    label = id['label']
    if label == 'tpm2_getcap':
        test_result = run_tpm2_getcap_test(label, helpers)
    elif label == 'tpm2_selftest':
        test_result = run_tpm2_selftest_test(label, helpers)
    elif label == 'tpm2_getrandom':
        test_result = run_tpm2_getrandom_test(label, helpers)
    elif label == 'tpm2_hash':
        test_result = run_tpm2_hash_test(label, helpers)
    elif label == 'tpm2_pcrread':
        test_result = run_tpm2_pcrread_test(label, helpers)
    elif label == 'tpm2_pcrextend':
        test_result = run_tpm2_pcrextend_test(label, helpers)
    elif label == 'tpm2_pcrreset':
        test_result = run_tpm2_pcrreset_test(label, helpers)
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
