# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
import logging
from eeprom import *

logger = logging.getLogger(__name__)

@pytest.mark.eeprom
def test_eeprom(id):
    eeprom_addr = id['eeprom_addr']
    field = id['field']
    value = id['value']

    run_eeprom_test(eeprom_addr, field, value, logger)
