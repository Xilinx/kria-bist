# Copyright (C) 2022-2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import glob
import itertools
from periphery import GPIO


def gpio_get_chip():
    """
    Find correct devpath for GPIO under test

    Returns:
            string: GPIO devpath
    """
    chips = glob.glob('/dev/gpiochip*')
    for chip in chips:
        gpio = GPIO(chip, 0, "in")
        label = gpio.chip_label
        # Check for a label in format "<8-digit hex value>.gpio"
        if (len(label) == 13) and label.split('.')[1] == 'gpio':
            try:
                int(label.split('.')[0], 16)
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

    Args:
            chip: GPIO devpath
            offset: Write offset, value written at this offset
            value: Value to be written
    """
    # Open legitimate GPIO out line, write the value, close GPIO line
    gpio_out = GPIO(chip, int(offset), "out")
    gpio_out.write(bool(value))
    gpio_out.close()


def gpio_read(chip, offset):
    """
    Reads value at given offset

    Args:
            chip: GPIO devpath
            offset: Read offset, value read from this offset

    Returns:
                int: Value read from given offset
    """
    # Open legitimate GPIO in line, read the value, close GPIO line
    gpio_in = GPIO(chip, int(offset), "in")
    read_val = int(gpio_in.read())
    gpio_in.close()
    return read_val


def gpio_write_range(chip, offset, width, values):
    """
    Args:
            chip: GPIO devpath
            offset: Write offset, value written at this offset
            width: Number of bits to write
            values: Tuple of int values
    """
    # Function call to write values to a GPIO line
    for i in range(width):
        gpio_write(chip, offset + i, values[i])


def gpio_read_range(chip, offset, width):
    """
    Args:
            chip: GPIO devpath
            offset: Read offset,value read from this offset
            width: Number of bits to read

    Returns:
                tuple: Tuple of int values
    """
    r_pattern = []

    # Function call to read values from a GPIO line
    for i in range(width):
        r_pattern.append(gpio_read(chip, offset + i))
    return tuple(r_pattern)


def generate_patterns(width):
    """
    Generate bit patterns, with only one bit set, for all permutations of <width> number of bits

    Args:
            width: Number of bits

    Returns:
                list: List of tuples of type int with binary pattern
    """
    patterns = []
    for i in range(width):
        # Generate binary patterns with only one set bit & add padding based on total bits(width)
        # Convert tuple of type str to tuple of type int
        patterns.append(tuple(int(digit) for digit in format(1 << i, 'b').zfill(width)))
    return patterns


def run_gpio_loopback(label, width, offset, helpers):
    """
    GPIO Loopback test execution

    Args:
            label: Interface under test
            width: Width of the GPIO under test
            offset: Offset of the GPIO under test
            helpers: Handle for logging

    """
    logger = helpers.logger_init(label)
    logger.start_test()
    width = width // 2
    w_offset = int(offset)
    r_offset = int(offset) + width

    # Function call to get legitimate GPIO devpath
    chip = gpio_get_chip()
    # Function call to generate patterns(1's and 0's)
    patterns = generate_patterns(width)

    # Write pattern(1's and 0's) of specified width(number of bits) at given offsets
    # Read pattern(1's and 0's) from given offsets(loopbacked pins)
    # Perform comparison of both patterns and conclude match/mismatch
    for w_pattern in patterns:
        gpio_write_range(chip, w_offset, width, w_pattern)
        r_pattern = gpio_read_range(chip, r_offset, width)

        wp = "".join(map(str, w_pattern))
        rp = "".join(map(str, r_pattern))
        result = "Match" if rp == wp else "Mismatch"

        if rp == wp:
            logger.info("Write pattern: " + wp + ", Read pattern " + rp + " : " + result)
            pattern_match = True

        else:
            logger.info("Write pattern: " + wp + ", Read pattern " + rp + " : " + result)
            pattern_match = False
            break
    
    logger.test_passed() if pattern_match else logger.test_failed()
    logger.stop_test()
    return pattern_match
