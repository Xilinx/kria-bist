# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_eeprom import *

@pytest.mark.eeprom
def test_eeprom(id, helpers):
    label = id['label']
    eeprom_addr = id['eeprom_addr']
    field = id['field']
    value = id['value']

    assert run_eeprom_test(label, eeprom_addr, field, value, helpers)
