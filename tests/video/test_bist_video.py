# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_video import *


@pytest.mark.video
def test_video(id, helpers):
    """
    Function to parse Video Test Configurations

    Args:
            id: List of configurations
    """
    # Parse the configurations
    label = (id["label"])
    pipeline = (id["pipeline"])
    width = (id["width"])
    height = (id["height"])
    fps = (id["fps"])
    fmt = (id["fmt"])

    if "filesink" in label:
        # Parse Test pattern generator value from configurations
        tpg_pattern = (id["tpg_pattern"])
        # Funtion call to Video Filesink Test
        test_result = run_video_filesink_test(label, pipeline, width, height, fps, fmt, tpg_pattern, helpers)
    elif "perf" in label:
        # Function call to Video Performance Test
        test_result = run_video_perf_test(label, pipeline, width, height, fps, fmt, helpers)
    elif "ximagesink" in label:
        # Parse Test pattern generator value from configurations
        tpg_pattern = (id["tpg_pattern"])
        # Function call to Video Imagesink test
        test_result = run_video_ximagesink_test(label, pipeline, width, height, fps, fmt, tpg_pattern, helpers)
    else:
        assert False

    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
