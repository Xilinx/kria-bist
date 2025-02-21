# Copyright (C) 2024 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import signal

class TimeoutException(Exception):
    """
    Raised when user does not provide input within the specified timeout period
    """
    pass


def timeout_handler(signum, frame):
    """
    Handles SIGALRM signal(timeout event) by raising a TimeoutException
    """
    raise TimeoutException

def input_timeout(seconds):
    """
    Wait for user input with a timeout

    Args:
            seconds: Timeout in seconds
    Returns:
            str/timeout: Returns user input string/TimeoutException if timeout complete
    """
    # Set signal alarm to trigger timeout_handler if alarm goes off
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

    try:
        # Wait for user input
        user_input = input()
        #If input is received before timeout, cancel the alarm
        signal.alarm(0)
        return user_input
    except TimeoutException:
        # Raise timeout occurred exception if no input entered within "seconds"
        raise TimeoutException
