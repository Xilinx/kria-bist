# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import glob
import re
import filecmp
import os
import signal


def get_video_node(pipeline):
    """
    Find correct video node for video pipeline

    Args:
            pipeline: Name of video pipeline

    Returns:
            string: Video node devpath
    """
    video_cmd = f"v4l2-ctl --list-devices"
    video_devices = subprocess.run(video_cmd.split(' '),check=True, capture_output=True, text=True)
    video_devices = video_devices.stdout.splitlines()
    for i in range(len(video_devices)):
        if pipeline in video_devices[i] and i < len(video_devices) - 1:
            video_node = video_devices[i + 1].replace('\t', '')
            return video_node
    return None


def get_media_node(pipeline):
    """
    Find correct media node for video pipeline

    Args:
            pipeline: Name of video pipeline

    Returns:
            string: Media node devpath
    """
    medias = glob.glob('/dev/media*')

    for media_node in medias:
        media_cmd = f"media-ctl -d {media_node} -p"
        media_devices = subprocess.run(media_cmd.split(' '),capture_output=True, check=True, text=True)
        media_devices = media_devices.stdout.splitlines()
        for i in range(len(media_devices)):
            if pipeline in media_devices[i] and i < len(media_devices) - 1:
                return media_node
    return None


def set_test_pattern(video_node):
    """
    Set a specific Test pattern on a sensor mapped to a video node

    Args:
            video_node: Video node devpath
    """
    # Test Pattern Generator control
    tpg_pattern = "1"
    # Set test pattern on given video node
    video_cmd = f"v4l2-ctl -d {video_node} -c test_pattern={tpg_pattern}"
    subprocess.run(video_cmd.split(' '),check=True, text=True)


def within_percentage(actual_fps, fps):
    """
    Calculate if captured actual fps is within +/- percentage range of target fps

    Args:
            actual_fps: Value of captured video framerate
            fps: Targetted frame rate

    Returns:
            bool: True/False
    """
    # Check whether actual_fps is within a +/- percentage relative to targetted fps
    percentage = 1
    difference = abs(actual_fps - fps)
    threshold = (percentage / 100) * fps
    return difference <= threshold


def get_framerate(perf_output):
    """
    Fetch framerate based on performance output

    Args:
            perf_output: Performace output of media pipeline

    Returns:
            float: Value of captured video framerate
    """
    # Extract and return the framerate of the last captured buffer from perf_output
    actual_fps = float((re.findall(r'\bfps: \d+\.\d+\b',perf_output)[-1]).split(':')[-1])
    return actual_fps


def run_perf_pipeline(media_node, width, height, fps, fmt, logger):
    """
    Get output of "perf" performance of media pipeline

    Args:
            media_node: Media node devpath
            width: Width in terms of resolution
            height: Height in terms of resolution
            fps: Targetted frames per second
            fmt: Video format of pipeline

    Returns:
            bool/string: False if Pipeline Times out/String of performance output if Pipeline succeeds
    """
    # Run the pipeline for 10 seconds
    buffers = (int(fps) * 10)
    # Run the pipeline
    gst_cmd = f"gst-launch-1.0 mediasrcbin media-device={media_node} v4l2src0::num-buffers={buffers} ! video/x-raw," \
              f"width={width},height={height},framerate={fps}/1,format={fmt} ! perf ! fakevideosink"
    try:
        process = subprocess.Popen(gst_cmd.split(' '), stdout=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=15)
    except subprocess.TimeoutExpired as e:
        logger.error("Gstreamer command timed out after " + str(e.timeout) + " seconds. Sensor not connected or faulty")
        os.kill(process.pid, signal.SIGKILL)
        return False
    if process.returncode:
        logger.error("Failed to run Gstreamer command")
        return False
    perf_output = stdout.decode('utf8')
    return perf_output


def compare_images(test_image_path, golden_image_path, logger):
    """
    Function to compare golden image with test image

    Args:
            test_image_path: Path to test_image
            golden_image_path: Path to golden_image
            logger: Handle for logging

    Returns:
            bool: True if match, False if images do not match or if image path does not exist
    """
    if not os.path.exists(test_image_path):
        logger.error("Test image not found")
        return False
    if not os.path.exists(golden_image_path):
        logger.error("Golden image not found")
        return False
    result = filecmp.cmp(test_image_path,golden_image_path, shallow=True)
    return result


def run_filesink_pipeline(label, media_node, width, height, fps, fmt, test_image_path, logger):
    """
    Generate a test image with test pattern

    Args:
            label: Label for interface under test
            media_node: Media node devpath
            width: Width in terms of resolution
            height: Height in terms of resolution
            fps: Targetted frames per second
            fmt: Format for video pipeline
            test_image_path: Path to test_image

    Returns:
            bool: True/False if Pipeline execution success/failure
    """
    # Run the pipeline
    gst_cmd = f"gst-launch-1.0 mediasrcbin media-device={media_node} v4l2src0::num-buffers=1 ! video/x-raw,width={width}" \
              f",height={height},framerate={fps}/1,format={fmt} ! filesink location={test_image_path}"
    try:
        process = subprocess.Popen(gst_cmd.split(' '), stdout=subprocess.PIPE)
        stdout,stderr = process.communicate(timeout=3)
    except subprocess.TimeoutExpired as e:
        logger.error("Gstreamer command timed out after " + str(e.timeout) + " seconds. Sensor not connected or faulty")
        os.kill(process.pid, signal.SIGKILL)
        return False
    if process.returncode:
        logger.error("Failed to run Gstreamer command")
        return False
    return True


def run_video_filesink_test(label, pipeline, width, height, fps, fmt, helpers):
    """
    Video Filesink Test

    Args:
            label: Label for interface under test
            pipeline: Name of video pipeline
            width: Width in terms of resolution
            height: Height in terms of resolution
            fps: Targetted frames per second
            fmt: Video format of pipeline
            helpers: Handle for logging
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Function call to fetch video node
    video_node = get_video_node(pipeline)
    if video_node == None:
        logger.error("No video node found for " + pipeline)
        return False

    # Function call to fetch media node
    media_node = get_media_node(pipeline)
    if media_node == None:
        logger.error("No media node found for " + pipeline)
        return False

    # Function call to set Test pattern
    set_test_pattern(video_node)

    # Function call to get paths for output/data directories
    output_dir = helpers.get_output_dir(__file__)
    data_dir = helpers.get_data_dir(__file__)

    # Set paths to golden/test images
    test_image_path = output_dir + "/" + label + "_test.raw"
    golden_image_path = data_dir + "/" + label + "_golden.raw"

    # Function call to generate test image
    output = run_filesink_pipeline(label, media_node, width, height, fps, fmt, test_image_path, logger)
    if not output:
        return False
    # Function call to compare golden and test image
    result = compare_images(test_image_path, golden_image_path, logger)
    if result:
        logger.info("Test Image and Golden Image match")
        return True
    else:
        logger.error("Test Image and Golden Image do not match")
        return False


def run_video_perf_test(label, pipeline, width, height, fps, fmt, helpers):
    """
    Video Performance Test

    Args:
            label: Label for Interface under test
            pipeline: Name of video pipeline
            width: Width in terms of resolution
            height: Height in terms of resolution
            fps: Targetted frames per second
            fmt: Video format of pipeline
            helpers: Handle for logging
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Function call to fetch media node
    media_node = get_media_node(pipeline)
    if media_node == None:
        logger.error("No media node found for " + pipeline)
        return False

    # Function call to fetch perf output
    perf_output = run_perf_pipeline(media_node, width, height, fps, fmt, logger)
    if not perf_output:
        return False
    logger.debug(perf_output)

    # Function call to get actual video framerate for captured buffers
    actual_fps = get_framerate(perf_output)

    # Function call to check if actual_fps is within accepted range of targetted fps
    result = within_percentage(actual_fps, int(fps))

    # Check result and declare pass/fail
    if result:
        logger.info("Actual fps: " + str(actual_fps) + ", Target fps:" + fps + " - Actual fps within accepted range")
        return True
    else:
        logger.error("Actual fps: " + str(actual_fps) + ", Target fps:" + fps + " - Actual fps not within accepted range")
        return False
