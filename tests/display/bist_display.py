# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import re

def get_display_status(display_device):
    """
    Get current status from display chip

    Args:
            display_device: DP name of display device

    Returns:
            string: Status connected/disconnected
    """
    modetest_cmd = f"modetest -D {display_device} -c"
    modetest_output = subprocess.run(modetest_cmd.split(' '), capture_output=True, check=True, text=True)
    matches = re.search(r"\bconnected\b", modetest_output.stdout)
    if matches:
        return "connected"
    else:
        return "disconnected"

def get_display_property_key(prop, key, display_device):
    """
    Return value for key under a property

    Args:
            prop: Property name in modetest_output
            key: Key name under property in modetest_output
            display_device: DP name of display device

    Returns:
            str/None: string of the key properties/None if key properties is just whitespace 
    """
    modetest_cmd = f"modetest -D {display_device} -c"
    modetest_output = subprocess.run(modetest_cmd.split(' '), capture_output=True, check=True, text=True)
    # Search for property in modetest_output
    output = re.split(r'(\d+ [\w-]+:)', modetest_output.stdout)
    for i in range(len(output)):
        if prop in output[i]:
            prop_output = output[i+1]
            break

    # Search for key in property output
    output = re.split(r'([\w-]+:)', prop_output)
    for i in range(len(output)):
        if key in output[i]:
            val = output[i+1]
            # check if value is only whitespace
            if val.isspace():
                return None
            return val
    return None


def run_display_connectivity_test(label, display_device, helpers):
    """
    DP Connectivity Test

    Args:
            label: Label for Interface under test
            display_device: DP name of display device
            helpers: Handle for logging
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Function call to get Display status,property/key
    status = get_display_status(display_device)
    edid_value = get_display_property_key('EDID', 'value', display_device)
    if status == "disconnected" or edid_value == None:
        logger.error("DisplayPort/HDMI cable not connected")
        return False
    logger.info("EDID read successfully")
    logger.debug("EDID value: " + edid_value)
    return True
