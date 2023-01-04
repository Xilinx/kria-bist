# Copyright (C) 2022 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest


def pytest_addoption(parser):
    """
    Addition to command line arguements

    :board  - Command line arguement which takes board name as input (eg --board kv260/kr260/kd240)
    :action - Store the command(will store the board name)
    :help   - Description of the command added to pytest help console

    """
    parser.addoption("--board", action="store", help="Board to use")
