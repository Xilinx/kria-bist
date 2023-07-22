# BIST Ethernet Test Module

## Overview

This module tests the ethernet interface(s) on the Kria starter kits using a
host machine.

## Tests

There are two types of tests in this module: a self-validating functional test
which uses the ping3 python package, and a self-validating performance test
which uses the iperf3 utility.

By default, the tests in this module expect the host machine's IP to be
192.168.0.1 for the ethernet interface. To change this, the BIST_REMOTE_HOST_IP
environment variable can be set on the Kria board. For Kria boards with
multiple ethernet ports, an ethernet switch must be used to connect all
ethernet ports to a single port on the host machine which has the above IP. The
default IP for the SFP interface on the host machine is 192.168.0.2. To change
this, the BIST_REMOTE_HOST_SFP_IP environment variable can be set.

The config parameters for this test are described below:

* label: The test label
* phy_addr: The PHY address of the ethernet port (Note: For the SFP+ port on
  the KR260, the phy_addr is None since the SFP+ port does not have a PHY)

For each test in this module, the eth_get_interface_speed() and eth_setup()
functions are used to set up the test. The eth_get_interface_speed() returns
the interface name and its speed based on the PHY address. If the PHY address
is None, this function returns the interface for the SFP+ port and a fixed
speed. The assumption is that there will only be one ethernet interface without
a PHY, and this interface corresponds to the SFP+ port. The eth_setup()
function checks if a given interface has an IP in the same subnet as the host
machine. If the host machine has already assigned an IP to the Kria board using
DHCP and it is in the same subnet, this IP is used for the test. If the host
machine has not assigned an IP, a static IP in the same subnet is assigned.

The ping test attempts to ping the host machine via a specific interface and
the test passes if the ping is successful.

The perf test uses iperf3 to test the performance between a specified interface
and the host machine. The bind_address parameter is used to determine which
interface is used for the test.

The mapping for the test labels to the four ethernet ports on KR260 is given
below:

| Test Label  | Ethernet Port |
| :---------: | :-----------: |
| ethernet1_* | Top Left      |
| ethernet2_* | Bottom Left   |
| ethernet3_* | Top Right     |
| ethernet4_* | Bottom Right  |

## Test Execution

Example commands for this module are provided below (KR260):

```bash
pytest-3 --board kr260 -m eth			// Run all tests in this module
pytest-3 --board kr260 -k ethernet1_ping	// Run ethernet1_ping test
pytest-3 --board kr260 -k ping			// Run all ping tests
pytest-3 --board kr260 -k perf			// Run all perf tests
```
For each interface, the ping test will print out the delay and the test will
pass if the ping is successful. The perf test will print out the measured
bitrate and the test will pass if it is above the threshold. The default
threshold is 80% of the max speed for the ethernet ports.

## Test Debug

* Make sure the host machine is set up as described [here](../run).
* Make sure the BIST_REMOTE_HOST_IP environment variable is set on the Kria
  board if the host machine's ethernet interface is not set to the default IP.
* Make sure the BIST_REMOTE_HOST_SFP_IP environment variable is set on the Kria
  board if the host machine's SFP interface is not set to the default SFP IP.
* For the perf tests, make sure an iperf3 server is running on the host machine.
* If a ping test fails, it can be run manually using ping with the -I option.
* If a perf test fails, it can be run manually using iperf3 with the -B option.

## Known Issues and Limitations

* The tests in this module are limited to verifying a ping and a minimum
  performance speed for each interface.
* The max speed for the KR260 SFP+ port is set to 0.5 Gbps based on tests
  performed with the BIST firmware.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
