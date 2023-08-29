# BIST Video Test Module

## Overview

This module tests the video interface(s) on the AMD Kria&trade; starter kits.
## Tests

There are three types of tests in this module:

* Self-validating functional tests
   * imx219_filesink
   * ar1335_filesink

   These tests use v4l2-utils to set a test pattern at the sensor and gstreamer
   packages to run a Gstreamer pipleine. The set_test_pattern() function sets
   the test pattern at the sensor, run_filesink_pipeline() runs the Gstreamer
   pipeline, which saves(capture a single frame) the test pattern raw test image.
   The compare_images() compares this test image against a pre-defined golden
   image and declares pass/fail

* Self-validating performance tests:
   * ar1335_ap1302_perf
   * tpg_ap1302_perf
   * imx219_perf
   * ar1335_perf

   These tests use Gstreamer packages to run a gstreamer pipeline on a media
   node. The run_perf_pipeline() runs a Gstreamer pipeline and captures the
   performance output, within_percentage() checks if the 'actual_fps' of the
   pipeline is within accepted range of 'target_fps'.

* User-validating functional tests:
   * ar1335_ap1302_ximagesink
   * tpg_ap1302_ximagesink

   These tests use v4l2-utils to set a test pattern at the ISP, certain debugfs
   commands to set test pattern at the sensor and gstreamer packages to run a
   Gstreamer pipeline, which opens up a new window/display(using ximagesink).
   run_ximagesink_pipeline() opens up this ximagesink display and waits for User
   Input. The user responds with a Y/N if the test pattern was observed.

The config parameters for this test are described below:
   * label: The test label
   * pipeline: Name of video pipeline
   * width: Width in terms of resolution
   * height: Height in terms of resolution
   * fps: Targetted frames per second
   * fmt: Video format of pipeline
   * tpg_pattern: Test pattern generator value(for ximageink and filesink tests)

Pattern to be observed in ximageink tests:

![Color_Bar_Pattern](../media/Color_Bar_Pattern.png)

## Test Execution

The example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m video                       // Run all tests in this module
pytest-3 --board kv260 -k imx219_perf	               // Run imx219_perf test
pytest-3 --board kv260 -k imx219_filesink             // Run imx219_filesink test
pytest-3 --board kv260 -k ar1335_ap1302_ximagesink    // Run ar1335_ap1302_ximagesink test
pytest-3 --board kv260 -k perf -m video               // Run all performance tests in this module
pytest-3 --board kv260 -k filesink -m video           // Run all filesink tests in this module
pytest-3 --board kv260 -k ximagesink -m video         // Run all ximagesink tests in this module
```
For the perf tests, the logs should have a comparison between actual_fps and
target_fps. For a pass, it should be within the accepted percentage range.
Additional debug information with the performance output can be found in the
log file that is generated automatically for each test.
For the filesink tests, expected result is a match between Golden Image and Test
Image. The live log call prints the result of the comparison.
For ximagesink tests, you are asked a question[Y/N] in the live log call, if a
test pattern was seen in the pop-up window. You have 30 seconds to answer it via
command line. Test result is based on your pattern observation.

## Test Debug

* Make sure that the BIST firmware is loaded.
* If the logs consist of the message, "No media node found" or "Gstreamer command
timed out after 15 seconds. Sensor not connected or faulty," these would mean
that either the sensor is not connected to the board or the sensor is faulty.
The solution would be to connect the sensor back and power cycle the board and
run the test again. If the sesnor was already connected, try with a new sensor.
* Make sure that you are in an SSH terminal with X11 forwarding enabled, which is 
mandatory while running ximagesink tests.


## Known Issues and Limitations

* Test pattern at the sensor(ar1335_tpg_ximagesink) does not produce expected
result with a single write to the register. When the pipeline is running, the second
write to register is done. There maybe a delay of around 3 seconds for the test
pattern to be observed.
* The actual_fps in performance tests is currently expected to be within +/- 1
percent relative to the target_fps.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
