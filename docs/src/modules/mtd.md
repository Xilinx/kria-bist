# BIST MTD Test Module

## Overview

The MTD test module verifies read and write functionality of the QSPI MTD User
partition along with the performance measure on the AMD Kria&trade; starter kits.

## Tests

The module contains self-validating funcational and performance tests. For the
functional test, it uses mtd-utils package to write random data to MTD User partition
and reads it back to ensure that the data is same. For the performance test, it uses
"dd" command-line utility to check the read and write performances of QSPI MTD user
partition and verifies if the measured read/write speeds are greater than the specified
threshold speeds. The test provides performance verification for different modes such
as read, write, and read_write (optional) suites.

The config parameter for the functional test is described below:

* label: The test label

The QSPI read/write functional test obtains the MTD user partition and size of the partition
using get_user_partition_size() function and verifies if the available space on the device
is greater than 1MiB. The test writes random data to the partition and reads it back using
mtd_debug_write() and mtd_debug_read() functions. The written data file and read data files
are compared using compare_files() to verify the read and write functionality of the QSPI
MTD User partition.

The config parameters for the performance test are described below:

* label: The test label
* mode: The mode of the performance test (read, write or read_write)

The QSPI performance test obtains the MTD user partition and size of the partition using
get_user_partition_size() function. It then verifies if the available space on the device
is greater than 1MiB. Depending on the mode of the test, read or write performance of the
interfaces are verified using dd command-line utility by get_qspi_write_performance() or
get_qspi_read_performance() functions and the result is logged by log_disk_performance().

## Test Execution

The example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m mtd  // Run all tests in this module
pytest-3 --board kv260 -k qspi_read_write  // Run QSPI read and write functional test
pytest-3 --board kv260 -k qspi_read_performance  // Run QSPI read performance test
pytest-3 --board kv260 -k qspi_write_performance  // Run QSPI write performance test
```

The QSPI read and write functional test prints the MTD User partition and its size along
with the status of test file write and read from the partition. The test is passed based
on data match between the written and read-back test data.

The QSPI read/write performance test prints the MTD User partition and its size along with
minimum expected read/write speed and measured speed. The test is passed based on the
measured and threshold speed comparison.

## Test Debug

* Verify that there is minimum of 1MiB of storage space available on the QSPI MTD user partition
  before performing read/write transaction.

## Known Issues and Limitations

* The MTD module is limited to verifying the functionality and performance on QSPI User
  partition only.
* MTD read and write from the User partition is done with offset of 196608 bytes due to
  sector lock.
* The QSPI read and write performance speeds are expected to be above the threshold speed
  values given in the following table. 

| Mode  |QSPI MTD partition|
| :---: | :--------------: |
| Read  |       9MBps      |
| Write |     285KBps      |

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>