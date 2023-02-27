# Copyright (C) 2022 - 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
import logging


class Helpers:
    def logger_init(label):
        logger = logging.getLogger(__name__)
        extra = {'label':label}
        logger = logging.LoggerAdapter(logger, extra)

        def start_test():
            logger.info("------------------------------------------")
            logger.info("Start of test")
        logger.start_test = start_test

        def test_passed():
            logger.info("Test passed")
        logger.test_passed = test_passed

        def test_failed():
            logger.info("Test failed")
        logger.test_failed = test_failed

        def stop_test():
            logger.info("End of test")
        logger.stop_test = stop_test

        return logger

@pytest.fixture
def helpers():
    return Helpers

def pytest_addoption(parser):
    """
    Addition to command line arguements

    :board  - Command line arguement which takes board name as input (eg --board kv260/kr260/kd240)
    :action - Store the command(will store the board name)
    :help   - Description of the command added to pytest help console

    """
    parser.addoption("--board", action="store", help="Board to use")
