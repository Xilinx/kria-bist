# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import pytest
from bist_iio import *

@pytest.mark.iio
def test_iio(id, helpers):
    if id['label'] == 'ina260_current':
        assert run_ina260_current_test(id['label'], id['device'], id['channel'], id['min_current'], id['max_current'], helpers)
