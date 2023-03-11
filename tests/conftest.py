# Copyright (C) 2022 - 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
import logging
import os


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

    def get_output_dir(module_file):
        curr_module = os.path.abspath(module_file).split('/')[-2]
        curr_wd = os.getcwd()
        curr_dir = curr_wd.split('/')[-1]

        # Case where pytest is run from module dir
        if curr_dir == curr_module:
            if not os.path.isdir('output'):
                os.makedirs('output')
            output_dir = curr_wd + "/output"
        # Case where pytest is run from top level dir
        else:
            os.chdir(curr_module)
            if not os.path.isdir('output'):
                os.makedirs('output')
            os.chdir(curr_wd)
            output_dir = curr_wd + "/" + curr_module + "/output"

        return output_dir

    def get_data_dir(module_file):
        curr_module = os.path.abspath(module_file).split('/')[-2]
        curr_wd = os.getcwd()
        curr_dir = curr_wd.split('/')[-1]

        # Case where pytest is run from module dir
        if curr_dir == curr_module:
            if os.path.isdir('data'):
                data_dir = curr_wd + "/data"
            else:
                data_dir = None
        # Case where pytest is run from top level dir
        else:
            os.chdir(curr_module)
            if os.path.isdir('data'):
                data_dir = curr_wd + "/" + curr_module + "/data"
            else:
                data_dir = None
            os.chdir(curr_wd)

        return data_dir

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
