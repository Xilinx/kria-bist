# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import re
import os
import signal
import time
from timeout_handler import input_timeout, TimeoutException


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


def get_plane_id(prop, display_device):
    """
    Return the plane_id for display device

    Args:
            prop: Property name in modetest_output
            display_device: DP name of display device

    Returns:
            str/None: Plane ID as a string/None if not found
    """
    modetest_cmd = f"modetest -D {display_device} -c"
    modetest_output = subprocess.run(modetest_cmd.split(' '), capture_output=True, check=True, text=True)
    output = re.split(r'[\n\t]', modetest_output.stdout)
    # Search for property in modetest_output
    for i in output:
        if prop == i:
            index = output.index(prop)
            break
    # Search for first number after index of prop which is the plane_id
    for i in range(index, len(output)):
        plane_id = re.match(r"\d+", output[i])
        if plane_id:
            return plane_id.group()
    return None


def run_modetest_pipeline(plane_id, fmt, logger):
    """
    Args:
            plane_id: Plane ID of display device
            fmt: Display format value
            logger: Handle for logging

    Returns:
            bool: True if output observed, False if not observed or user input timed out
    """
    modetest_cmd = f"modetest -M xlnx -s {plane_id}:#0@{fmt}"
    try:
        logger.info("Please observe output on Monitor")
        process = subprocess.Popen(modetest_cmd.split(' '), stdout=subprocess.PIPE)
        time.sleep(10)
        os.kill(process.pid, signal.SIGKILL)
        while(1):
            logger.info("Did you see color bar test pattern on Monitor [Y/N]?")
            user_timeout = 30
            var = input_timeout(user_timeout).strip().upper()
            if var == 'Y':
                logger.info("User reports pattern was observed on Monitor")
                ret_val = True
                break
            elif var == 'N':
                logger.error("User reports pattern was not observed on Monitor")
                ret_val = False
                break
            else:
                logger.info("Invalid input, please try again")
    except TimeoutException:
        logger.error("No user input entered after " + str(user_timeout) + " seconds, aborting test")
        ret_val = False
    return ret_val


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


def run_display_modetest(label, display_device, fmt, helpers):
    """
    DP Modetest

    Args:
            label: Label for Interface under test
            display_device: DP name of display device
            fmt: Display format value
            helpers: Handle for logging
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Fetch the Plane ID
    plane_id = get_plane_id('id', display_device)
    if plane_id == None:
        logger.error("Plane ID not found")
        return False
    # Function call to Run Modetest Pipeline
    return run_modetest_pipeline(plane_id, fmt, logger)
