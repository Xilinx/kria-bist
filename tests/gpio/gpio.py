# Copyright (C) 2022 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT


def run_gpio_loopback(width, offset):
    """
    GPIO Loopback test execution

    :arg width  : Width of the GPIO under test
    :arg offset : Offset of the GPIO under test

    """
    print("\n Width is: " + str(width))
    print("\n Offset is: " + str(offset))
