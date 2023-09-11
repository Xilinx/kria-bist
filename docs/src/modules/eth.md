# BIST Ethernet Test Module

## Overview

This module tests the ethernet interface(s) on the AMD Kria&trade; starter kits using a
host machine.

## Tests

There are two types of tests in this module: a self-validating functional test,
which uses the ping3 python package, and a self-validating performance test,
which uses the iperf3 utility.

There are two ways in which you can assign an IP Address:
  * DHCP IP Assignment
  * Static IP Assignment

**NOTE**: `BIST_REMOTE_HOST_SFP_IP` can only be assigned a Static IP

Configure the host machine to have a DHCP/Static IP and set the `BIST_REMOTE_HOST_IP` 
environment variable on the Kria board. If the host machine has already assigned 
an IP to the Kria board using DHCP and it is in the same subnet, this IP is used 
for the test. If the host machine has not assigned an IP, user should assign a 
Static IP under the same subnet to the eth interfaces. For Kria boards with 
multiple ethernet  ports, an ethernet switch must be used to connect all ethernet 
ports to a single port on the host machine that has the above IP. Configure the 
IP for the SFP interface on the host machine and set the `BIST_REMOTE_HOST_SFP_IP` 
environment variable on the Kria board.

If Static IP Assignment is used for BIST_REMOTE_HOST_IP and 
BIST_REMOTE_HOST_SFP_IP they have to be on different subnets. For example:
* `BIST_REMOTE_HOST_IP` - `192.168.0.1`
* `BIST_REMOTE_HOST_SFP_IP` - `192.168.1.1`

On the KR260 the interfaces correspond to the following:
* eth0,eth1,eth3,eth4(PS/PL IPs) - Should be under `BIST_REMOTE_HOST_IP` subnet
* eth2(SFP IP) - Should be under `BIST_REMOTE_HOST_SFP_IP` subnet

The config parameters for this test are described below:

* label: The test label
* phy_addr: The PHY address of the ethernet port (Note: For the SFP+ port on
  the KR260, the phy_addr is None since the SFP+ port does not have a PHY)

For each test in this module, the eth_get_interface_speed() and eth_setup()
functions are used to set up the test. The eth_get_interface_speed() returns
the interface name and its speed based on the PHY address. If the PHY address
is None, this function returns the interface for the SFP+ port and a fixed
speed. The assumption is that there is only one ethernet interface without
a PHY, and this interface corresponds to the SFP+ port. The eth_setup()
function checks if a given interface has an IP in the same subnet as the host
machine. 

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

The example commands for this module are provided below (KR260):

```bash
pytest-3 --board kr260 -m eth			// Run all tests in this module
pytest-3 --board kr260 -k ethernet1_ping	// Run ethernet1_ping test
pytest-3 --board kr260 -k ping			// Run all ping tests
pytest-3 --board kr260 -k perf			// Run all perf tests
```
For each interface, the ping test prints out the delay and the test is a
pass if the ping is successful. The perf test prints out the measured
bitrate and the test is a pass if it is above the threshold. The default
threshold is 80% of the max speed for the ethernet ports.

## Test Debug

* Make sure that the host machine is set up as described [here](../run).
* Make sure that the BIST_REMOTE_HOST_IP environment variable is set on the Kria
  board.
* Make sure that the BIST_REMOTE_HOST_SFP_IP environment variable is set on the Kria
  board.
* If static IP assignment is used for host machines, make sure that 
  BIST_REMOTE_HOST_IP and BIST_REMOTE_HOST_SFP_IP are on different subnets.
* For the perf tests, make sure that an iperf3 server is running on the host machine.
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
