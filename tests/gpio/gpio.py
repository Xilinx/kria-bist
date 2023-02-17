# Copyright (C) 2022 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import glob
from periphery import GPIO

def gpio_get_chip():
    chips = glob.glob('/dev/gpiochip*')
    for chip in chips:
        gpio = GPIO(chip, 0, "in")
        label = gpio.chip_label
        # Check for a label in format "<8-digit hex value>.gpio"
        if(len(label)==13) and label.split('.')[1] == 'gpio':
            try:
                int(label.split('.')[0],16)
                device_path = gpio.devpath
                gpio.close()
                return device_path
            except ValueError:
                gpio.close()
        else:
            gpio.close()
    print('No gpiochip found with label in format "<8-digit hex value>.gpio"')

def gpio_write(chip, offset, value):
    """
    Writes value (True or False) at given offset
    """
    gpio_out = GPIO(chip, int(offset), "out")
    gpio_out.write(value)
    gpio_out.close()

def gpio_read(chip, offset):
    """
    Reads value at given offset
    """
    gpio_in = GPIO(chip, int(offset), "in")
    read_val = gpio_in.read()
    gpio_in.close()
    return read_val

def run_gpio_loopback(width, offset):
    """
    GPIO Loopback test execution

    :arg width  : Width of the GPIO under test
    :arg offset : Offset of the GPIO under test

    """
    print("\n Width is: " + str(width))
    print("\n Offset is: " + str(offset))
