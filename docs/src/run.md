# Setting up the Board and Application Deployment

## Introduction

This document shows how to set up the board and run the Built-In Self Test
(BIST) application.

This guide and its prebuilts are targeted for Ubuntu 22.04 and Xilinx 2023.1
toolchain.

## Set up the Host Machine

***Note***: Setting up the host machine is only required to test the ethernet
and SFP+ interfaces. If this is skipped, the tests for these interfaces
fail.

* Install the NIC card into the host machine.

* The host machine can be assigned an IP in two ways:
  * DHCP IP Assignment
  * Static IP Assignment

* Configure the host machine to have a DHCP/Static IP and set the 
  `BIST_REMOTE_HOST_IP` environment variable on the AMD Kria &trade; board.

  Example:
  ```
    export BIST_REMOTE_HOST_IP=<IP_Address>
  ```

* Install iperf3.

  * For Ubuntu, use the following command:

    ```
    sudo apt install iperf3
    ```

  * For Windows, use the appropriate download link from
    [this page](https://iperf.fr/iperf-download.php).

* Start an iperf3 server on the host machine using the following command:

   ```
   iperf3 -s -p 5201
   ```


## Set up the Board

Supported Starter Kits

The BIST application requires the following hardware setup to run
the full suite of hardware tests. See the board specific pages:

1. [KV260 Board Setup](setup_kv260.md)
2. [KR260 Board Setup](setup_kr260.md)
2. [KD240 Board Setup](setup_kd240.md)


## Tested Artifacts

Testing was performed with the following artifacts:

### KD240 platform artifacts

| Component                | Version              |
|--------------------------|----------------------|
| Boot Fiwmare             | K24-BootFW-01.00.bin |
| Linux Kernel             | 5.15.0-9002          |
| xlnx-firmware-kd240-bist | 0.10.1-0xlnx1        |

### KR260 platform artifacts

| Component                | Version                                                 |
|--------------------------|---------------------------------------------------------| 
| Boot Firmware            | BOOT_xilinx-k26-starterkit-v2022.1-09152304_update3.BIN |
| Linux Kernel             | 5.15.0-1023                                             |
| xlnx-firmware-kr260-bist | 0.10.1-0xlnx1                                           |

### KV260 platform artifacts

| Component                | Version                                                 |
|--------------------------|---------------------------------------------------------| 
| Boot Firmware            | BOOT_xilinx-k26-starterkit-v2022.1-09152304_update3.BIN |
| Linux Kernel             | 5.15.0-1023                                             |
| xlnx-firmware-kv260-bist | 0.10.1-0xlnx1                                           |

Please refer to the [Kria Wiki](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/1641152513/Kria+K26+SOM#Boot-Firmware-Updates)
to obtain latest linux image and boot firmware.

### Application docker image

| Docker Image              | Version     |
|---------------------------|------------ |
| xilinx/kria-bist          | 2023.1      |

## Boot Linux

Before continuing with the BIST application specific instructions, if not yet
done so, boot Linux with instructions from:

  1. [Kria Starter Kit Linux Boot on KV260](https://xilinx.github.io/kria-apps-docs/kv260/2022.1/build/html/docs/kria_starterkit_linux_boot.html)
  2. [Kria Starter Kit Linux Boot on KR260](https://xilinx.github.io/kria-apps-docs/kr260/build/html/docs/kria_starterkit_linux_boot.html)
  3. [Kria Starter Kit Linux Boot on KD240](https://xilinx.github.io/kria-apps-docs/kd240/linux_boot.html)

## Download and Load the BIST PL Firmware

* Search the package feed for available bist firmware packages.

  ```bash
  apt search bist

  Sorting... Done
  Full Text Search... Done

  xlnx-firmware-kr260-bist/jammy 0.10-0xlnx1 arm64
  FPGA firmware for Xilinx boards - kr260 bist application
  xlnx-firmware-kv260-bist/jammy 0.10-0xlnx1 arm64
  FPGA firmware for Xilinx boards - kv260 bist application
  xlnx-firmware-kd240-bist/jammy 0.10-0xlnx1 arm64
  FPGA firmware for Xilinx boards - kd240 bist application
  ```

* Install firmware binaries.

  ```bash
  sudo apt install xlnx-firmware-kv260-bist     // For kv260-bist
  sudo apt install xlnx-firmware-kr260-bist     // For kr260-bist
  sudo apt install xlnx-firmware-kd240-bist     // For kd240-bist
  ```

* List installed the application firmware binaries.

  The firmware consists of bitstream, device tree overlay (dtbo) file. The
  firmware is loaded dynamically on user request once Linux is fully booted.
  The xmutil utility can be used for that purpose.

  After installing the FW, execute xmutil listapps to verify that it is
  captured under the listapps function, and to have dfx-mgrd, re-scan and
  register all accelerators in the firmware directory tree.

  ```bash
  sudo xmutil listapps
  ```

* Load a new application firmware binary.

  When there is already an another accelerator/firmware being activated, unload it
  first, then load the desired BIST firmware.

  ```bash
  sudo xmutil unloadapp
  sudo xmutil loadapp kv260-bist      // For kv260-bist
  sudo xmutil loadapp kr260-bist      // For kr260-bist
  sudo xmutil loadapp kd240-bist      // For kd240-bist
  ```
  **NOTE**: KD240 Firmware load `xmutil loadapp kd240-bist` will print following 
  messages. These are safe to ignore.
  ```bash
    [  112.802574] net eth1: Speed other than 10, 100
    [  112.807227] net eth1: or 1Gbps is not supported
    [  112.866305] net eth2: Speed other than 10, 100
    [  112.871168] net eth2: or 1Gbps is not supported
  ```

## Setup SSH with X-forwarding

**NOTE**: Setting up an SSH connection is only required to test the ximagesink
tests of the video module on KV260 board. If this is skipped, those tests will 
fail

* To run the bist test suite, the test instructions should run over an SSH
  connection with X-forwarding enabled.

  Examples:

  * On Host, run:

    ```bash
    ssh -X ubuntu@<Kria Starter Kit IP address>
    ```
    **NOTE**: If all ethernet cables are plugged in, feel free to use any IP.

  * On Windows, download [Mobaxterm](https://mobaxterm.mobatek.net/download.html),
    which automatically enables X-forwarding when creating a new ssh connection.

## Miscellaneous Preparation

* Verify if the SSH terminal is using the correct authority file.
  * The output should look something like this.
   ```bash
   xauth -v list
   Using authority file /home/ubuntu/.Xauthority
   kria/unix:10  MIT-MAGIC-COOKIE-1  f5212118305f75678a69daa4a6eda703
   ```
   * If incorrect or no authority file is present, do the following steps:
   ```bash
   rm -rf ~/.Xaut*
   ```
   * Reboot the target board.
   ```bash
   sudo reboot
   ```
   * Check the `xauth -v list` after reboot(in SSH terminal), it should display 
   the correct authority file on the output console.

* The BIST application tests the fan. Therefore, if a fan is present stop the 
  fancontrol service before running the docker for the testing to function as 
  intended.

  ```bash
  sudo systemctl stop fancontrol
  ```

* On KV260/KR260 disable desktop environment before running the docker 
  for the display testing to function as intended. On KD240 this step can be 
  skipped as we are using a headless Ubuntu Server image.

  ```bash
  sudo xmutil desktop_disable
  ```

  ***NOTE***: Executing “xmutil desktop_disable” causes the monitor to go
  blank.

* Remember to start the fancontrol service after exiting the docker container.

  ```bash
  sudo systemctl start fancontrol
  ```

* After running the application and exiting the docker container, the desktop
  environment can be enabled again.

  ```bash
  sudo xmutil desktop_enable
  ```

## Download and Run the BIST Docker Image

* Pull the docker image from dockerhub.

  ```bash
  docker pull xilinx/kria-bist:2023.1
  ```

* The storage volume on the SD card can be limited with multiple docker
  images inbstalled. If there are space issues, use the following command
  to remove existing docker images.

  ```bash
  docker rmi --force <image>
  ```

* You can find the images installed with the following command:

  ```bash
  docker images
  ```

* Launch the docker container using the following command:

  ```bash
  docker run \
      --env=DISPLAY \
      --env=XDG_SESSION_TYPE \
      --net=host \
      --privileged \
      --volume=/home/ubuntu/.Xauthority:/root/.Xauthority:rw \
      -v /tmp:/tmp \
      -v /dev:/dev \
      -v /sys:/sys \
      -v /etc/vart.conf:/etc/vart.conf \
      -v /lib/firmware/xilinx:/lib/firmware/xilinx \
      -v /run:/run \
      -it xilinx/kria-bist:2023.1 bash
  ```

* It launches the bist image in a new container and drops the user into a bash
  shell.

  ```
  root@xlnx-docker/#
  ```

## Setup IP addresses on the Kria board

* Set the `BIST_REMOTE_HOST_IP` environment variable on Kria board
  
  Example:
  ```
    export BIST_REMOTE_HOST_IP=<IP_Address>
  ```

* You can assign IP addresses in two ways:
  * DHCP IP Assignment - IP addresses are auto-assigned.
  * Static IP Assignment - You need to set a Static IP for the eth interfaces 
    under test. Make sure that the Static IPs are in the same subnet as the 
    remote host machine.

## Run the BIST Application

The application is installed under `/opt/xilinx/kria-bist`. Navigate to the
"tests" directory from where the BIST tests are to be run.

```bash
cd /opt/xilinx/kria-bist/tests
```

### Usage

Commonly used command line switches for BIST.

```bash
pytest-3 [OPTIONS]

OPTIONS:
  --collect-only                Collect the tests
  --board <target_board>        Specify target board
  -k <test_name>                Run an individual test
  -m <module_name>              Specify module name
```

### Output and Logs

The pytest command line output has two separate sessions as follows:

* Test session

  It displays the number of collected, deselected, and selected tests. Current
  running test is also shown.

  For example:

  ```bash
  ============================= test session starts ==============================
  platform linux -- Python 3.10.6, pytest-6.2.5, py-1.10.0, pluggy-0.13.0
  rootdir: /opt/xilinx/kria-bist/tests, configfile: pytest.ini
  plugins: anyio-3.6.1
  collected 34 items / 33 deselected / 1 selected

  gpio/test_bist_gpio.py::test_gpio[pmod0]
  ```

* Live Log call

  This displays the current status of the test.

  1. Start of test: Indicates that the test has started.

  2. Test observations: Prints the test observation on the command line.

  3. Test passed/failed: Declares the test result, that is, pass/fail.

  4. End of Test: Indicates that the test has ended.

  For example:

  ```bash
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Write pattern: 0001, Read pattern 0001 : Match
  Write pattern: 0010, Read pattern 0010 : Match
  Write pattern: 0100, Read pattern 0100 : Match
  Write pattern: 1000, Read pattern 1000 : Match
  Test passed
  End of test
  PASSED                                                                   [100%]

  ======================= 1 passed, 33 deselected in 1.02s =======================
  ```

* A log file (`kria_bist_pytest.log`) is created in the current directory.

### Examples

* Run the entire BIST test suite for a target board.

  ```bash
  pytest-3 --board kv260     // For KV260
  pytest-3 --board kr260     // For KR260
  pytest-3 --board kd240     // For KD240
  ```

* Run individual tests.

  The following example runs the pmod0 test on the KV260 as target board.

  ```bash
  pytest-3 -k pmod0 --board kv260

  ============================= test session starts ==============================
  platform linux -- Python 3.10.6, pytest-6.2.5, py-1.10.0, pluggy-0.13.0
  rootdir: /opt/xilinx/kria-bist/tests, configfile: pytest.ini
  plugins: anyio-3.6.1
  collected 34 items / 33 deselected / 1 selected

  gpio/test_bist_gpio.py::test_gpio[pmod0]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Write pattern: 0001, Read pattern 0001 : Match
  Write pattern: 0010, Read pattern 0010 : Match
  Write pattern: 0100, Read pattern 0100 : Match
  Write pattern: 1000, Read pattern 1000 : Match
  Test passed
  End of test
  PASSED                                                                   [100%]

  ======================= 1 passed, 33 deselected in 1.01s =======================
  ```

* Collect test cases.

  Collect all the tests for a target board.

  ```bash
  pytest-3 --collect-only --board kv260

  ========================== test session starts ===============================
  platform linux -- Python 3.10.6, pytest-6.2.5, py-1.10.0, pluggy-0.13.0
  rootdir: /opt/xilinx/kria-bist/tests, configfile: pytest.ini
  plugins: anyio-3.6.1
  collected 40 items

  <Module disk/test_bist_disk.py>
    <Function test_disk[usb1_read_performance]>
    <Function test_disk[usb1_write_performance]>
    <Function test_disk[usb2_read_performance]>
    <Function test_disk[usb2_write_performance]>
    <Function test_disk[usb3_read_performance]>
    <Function test_disk[usb3_write_performance]>
    <Function test_disk[usb4_read_performance]>
    <Function test_disk[usb4_write_performance]>
    <Function test_disk[sd_read_performance]>
    <Function test_disk[sd_write_performance]>
  <Module display/test_bist_display.py>
    <Function test_display[display_connectivity]>
    <Function test_display[display_modetest]>
  <Module eeprom/test_bist_eeprom.py>
    <Function test_eeprom[som_eeprom]>
    <Function test_eeprom[carrier_card_eeprom]>
  <Module eth/test_bist_eth.py>
    <Function test_eth[ethernet1_ping]>
    <Function test_eth[ethernet1_perf]>
  <Module gpio/test_bist_gpio.py>
    <Function test_gpio[pmod0]>
  <Module i2c/test_bist_i2c.py>
    <Function test_i2c[ps_i2c_bus_main]>
    <Function test_i2c[axi_i2c_bus_main]>
    <Function test_i2c[axi_i2c_bus_ch0]>
  <Module iio/test_bist_iio.py>
    <Function test_iio[ina260_current]>
  <Module mtd/test_bist_mtd.py>
    <Function test_mtd[qspi_read_write]>
    <Function test_mtd[qspi_read_performance]>
    <Function test_mtd[qspi_write_performance]>
  <Module pwm/test_bist_pwm.py>
    <Function test_pwm[fan]>
  <Module tpm/test_bist_tpm.py>
    <Function test_tpm[tpm2_getcap]>
    <Function test_tpm[tpm2_selftest]>
    <Function test_tpm[tpm2_getrandom]>
    <Function test_tpm[tpm2_hash]>
    <Function test_tpm[tpm2_pcrread]>
    <Function test_tpm[tpm2_pcrextend]>
    <Function test_tpm[tpm2_pcrreset]>
  <Module video/test_bist_video.py>
    <Function test_video[ar1335_ap1302_ximagesink]>
    <Function test_video[ar1335_ap1302_perf]>
    <Function test_video[tpg_ap1302_ximagesink]>
    <Function test_video[tpg_ap1302_perf]>
    <Function test_video[imx219_filesink]>
    <Function test_video[imx219_perf]>
    <Function test_video[ar1335_filesink]>
    <Function test_video[ar1335_perf]>

  ====================== 40 tests collected in 1.02s ===========================
  ```

* Collect all tests for a specific testmodule for a target board.

  ```bash
  pytest-3 --collect-only --board kv260 -m video

  ============================= test session starts ==============================
  platform linux -- Python 3.10.6, pytest-6.2.5, py-1.10.0, pluggy-0.13.0
  rootdir: /opt/xilinx/kria-bist/tests, configfile: pytest.ini
  plugins: anyio-3.6.1
  collected 34 items / 26 deselected / 8 selected

  <Module video/test_bist_video.py>
    <Function test_video[ar1335_ap1302_ximagesink]>
    <Function test_video[ar1335_ap1302_perf]>
    <Function test_video[tpg_ap1302_ximagesink]>
    <Function test_video[tpg_ap1302_perf]>
    <Function test_video[imx219_filesink]>
    <Function test_video[imx219_perf]>
    <Function test_video[ar1335_filesink]>
    <Function test_video[ar1335_perf]>

  ================ 8/34 tests collected (26 deselected) in 0.99s =================
  ```

* Run all tests for a target board and the module.

  ```bash
  pytest-3 --board kv260 -m video

  ============================= test session starts ==============================
  platform linux -- Python 3.10.6, pytest-6.2.5, py-1.10.0, pluggy-0.13.0
  rootdir: /opt/xilinx/kria-bist/tests, configfile: pytest.ini
  plugins: anyio-3.6.1
  collected 34 items / 26 deselected / 8 selected

  video/test_bist_video.py::test_video[ar1335_ap1302_ximagesink]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Please observe the pop-up window
  Do you see color bar test pattern in the window [Y/N]?
  y
  User reports that pattern was observed in the window
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[ar1335_ap1302_perf]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Actual fps: 30.0, Target fps:30 - Actual fps within accepted range
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[tpg_ap1302_ximagesink]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Please observe the pop-up window
  Do you see color bar test pattern in the window [Y/N]?
  y
  User reports that pattern was observed in the window
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[tpg_ap1302_perf]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Actual fps: 30.003, Target fps:30 - Actual fps within accepted range
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[imx219_filesink]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test

  (gst-launch-1.0:89): GStreamer-CRITICAL **: 21:29:17.009: gst_structure_fixate_field_nearest_int: assertion 'IS_MUTABLE (structure)' failed

  (gst-launch-1.0:89): GStreamer-CRITICAL **: 21:29:17.009: gst_structure_fixate_field_nearest_int: assertion 'IS_MUTABLE (structure)' failed

  (gst-launch-1.0:89): GStreamer-CRITICAL **: 21:29:17.010: gst_structure_fixate_field_nearest_fraction: assertion 'IS_MUTABLE (structure)' failed
  Test Image and Golden Image match
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[imx219_perf]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Actual fps: 30.004, Target fps:30 - Actual fps within accepted range
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[ar1335_filesink]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  (gst-launch-1.0:89): GStreamer-CRITICAL **: 21:29:17.009: gst_structure_fixate_field_nearest_int: assertion 'IS_MUTABLE (structure)' failed

  (gst-launch-1.0:89): GStreamer-CRITICAL **: 21:29:17.009: gst_structure_fixate_field_nearest_int: assertion 'IS_MUTABLE (structure)' failed

  (gst-launch-1.0:89): GStreamer-CRITICAL **: 21:29:17.010: gst_structure_fixate_field_nearest_fraction: assertion 'IS_MUTABLE (structure)' failed
  Test Image and Golden Image match
  Test passed
  End of test
  PASSED
  video/test_bist_video.py::test_video[ar1335_perf]
  -------------------------------- live log call ---------------------------------
  ------------------------------------------
  Start of test
  Actual fps: 30.004, Target fps:30 - Actual fps within accepted range
  Test passed
  End of test
  PASSED                                                                   [100%]

  ==================== 8 passed, 26 deselected in 42.11s =======================
  ```

## Next Steps

* [BIST Overview](./overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
