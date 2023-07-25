# BIST Disk Test Module

## Overview

The disk test module verifies the performance of USB and SD interfaces on the 
Kria starter kits.


## Tests

The module contains self validating performance test. It uses "dd" command-line
utility to check the performance of USB and SD disk interfaces and verifies
if the measured read/write speeds are greater than the specified threshold speeds.
The test provides performance verification for different modes such as read, write
and read_write (optional) suites.

The config parameters for the test are described below:

* label: The test label
* hw_path: The USB/SD hardware path enumeration on the device
* mode: The mode of the performance test (read, write or read_write)

The disk performance test obtains port name and number from the test label
and retrieves the disk partition, USB/SD device path and speed standard of
the device connected to the interface using get_dev_path_speed() function.
The module then verifies if the available space on the device is greater than
128MiB using check_disk_space() function and mounts it for read and write transaction
between the device and the starter kit. 

Depending on the mode of the test, read or write performance of the interfaces
are verified using dd command-line utility by get_read_speed() or get_write_speed()
functions and the result is logged by log_disk_performance(). The device is unmounted
after the test execution.

For KV260 and KR260 starter kits, there are four USB ports and one SD card port. The
mapping for the test labels to the four USB ports is given below:

| Test Label  | USB Port |
| :---------: | :------: |
| usb1_* | Top Left      |
| usb2_* | Bottom Left   |
| usb3_* | Top Right     |
| usb4_* | Bottom Right  |

## Test Execution

Example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m disk  // Run all tests in this module
pytest-3 --board kv260 -k usb1_read_performance  // Run read performance test for USB1 port
pytest-3 --board kv260 -k usb1_write_performance  // Run write performance test for USB1 port
pytest-3 --board kv260 -k sd_read_performance  // Run read performance test for SD port
pytest-3 --board kv260 -k sd_write_performance  // Run write performance test for SD port
```

For each interface, the test prints out the device path, speed standard of the device
connected, along with minimum expected read/write speed and measured speed. The log indicates
whether the performance test is passed or failed based on the measured and threshold speed
comparison.

## Test Debug

* Make sure the USB/SD card media is inserted correctly to the interface under test.
* Verify there is minimum of 128MiB of storage space available for performing read/write
  transaction on the device connected to the interface. 

## Known Issues and Limitations

* The disk test is limited to verifying the read and write performances of USB and SD
  ports only. 
* Read and write performance speeds depend on the actual device under test and varies greatly
  on the manufacturer and model. The obtained performance numbers are to be reviewed by the
  user and not an indication of max achievable performance.
* There is a known issue that for some USB/SD ports read and write performance speeds fall
  slightly below the threshold speeds given in the table below. In this case, the performance
  can be verified manually based on the device manufacturer and model.

| Mode  | SD Speed C-class | SD Speed UHS-class | USB-SD Speed class | USB 2.0 | USB 3.0 |
| :---: | :--------------: | :----------------: | :----------------: | :-----: | :-----: |
| Read  |       6MB/s      |       12MB/s       |        6MB/s       |  9MB/s  |  80MB/s |
| Write |       2MB/s      |       6MB/s        |        2MB/s       |  2MB/s  |  8MB/s  |

* The threshold speeds are established based on experimentation conducted on different devices
  as shown in the tables below. The read and write speeds indicated are an average of multiple
  iterations with a 20% error margin.
  
USB devices:

|                Model                 |   Class   |  Read     |   Write  |
|  :--------------------------------:  |  :-----:  |  :-----:  |  :----:  |
|     SanDisk Cruzer - SDCZ600-016G    |  USB 3.0  |  100MB/s  |  12MB/s  |
|      SanDisk Ultra - SDCZ48-016G     |  USB 3.0  |  102MB/s  |   8MB/s  |
|   SanDisk Ultra fair - SDCZ73-032G   |  USB 3.0  |  120MB/s  |  12MB/s  |
|   SanDisk Ultra Eco - SDCZ96-064G    |  USB 3.2  |  80MB/s   |  12MB/s  |
|      SanDisk Cruzer - SDCZ36-004G    |  USB 2.0  |   9MB/s   |   2MB/s  |
|  SanDisk Cruzer Blade - SDCZ50-016G  |  USB 2.0  |  24MB/s   |   7MB/s  |
|  DataTraveler 101 G2 - DT101G2-016G  |  USB 2.0  |  18MB/s   |   6MB/s  |

MicroSD devices:

For the MicroSD devices, there are two variants in the same model that match both theoretical
speeds of SD Speed C-class and SD Speed UHS-class.

|                      Model                    |        Class       |   Read   |  Write |
| :-------------------------------------------: | :----------------: | :------: | :----: |
| SanDisk Ultra 16GB - HC Class 10 (White/Grey) |  SD Speed C-class  |  6MB/s   |  2MB/s |
| SanDisk Ultra 16GB - HC Class 10 (Red/Grey)   | SD Speed UHS-class |  12MB/s  |  6MB/s |

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>