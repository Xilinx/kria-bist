# BIST CAN Test Module

## Overview

The CAN test module verifies the functionality of CAN transceiver on the KD240 starter kit.

## Tests

The module contains self-validating functional test. It uses python3-can package for
transmitting and receiving CAN messages through the CAN port (CAN_L, CAN_H and GND pins).
The verification is done by performing transactions between MCP25625 PMOD CAN controller
(connected via SPI to KD240) and zynq_can controller on the kit. For the 'can_bus_send'
test, CAN message is sent from the CAN port on the kit and received on the PMOD CAN port.
Based on the comparison of sent and received messages, CAN transmit functionality is
verified on the board. Similarly, for 'can_bus_receive' test, the PMOD CAN port sends the
CAN messages and zynq_can CAN port on the kit receives the messages. Based on the comparison
of sent and received messages, CAN receive functionality is verified. 

The config parameters for the test are described below:

* label: Test label
* can_transmitter: CAN message transmitter
* can_receiver: CAN message receiver

The run_can_transmission_test() functional test obtains CAN node for transmitter and
receiver through get_can_node() function based on the controller information. CAN nodes
are then initialized by setting baudrate, buffer length, etc for communication through
can_node_initialize(). CAN messages are sent and received through send_can_message() and
read_can_message() functions via can_bus.send() and can_bus.recv() instances provided by
python3-can module. After the comparison of sent and received messages, the can nodes are
shutdown using can_node_shutdown().

## Test Execution

The example commands for this module are provided below:

```bash
pytest-3 --board kd240 -m can  // Run all tests in this module
pytest-3 --board kd240 -k can_bus_send  // Run CAN message transmitter functional test
pytest-3 --board kd240 -k can_bus_receive  // Run CAN message receiver functional test
```

The CAN functional test prints the CAN node enumeration of the form canX for transmitter
and receiver nodes along with the message transmitted and received. The test is passed based
on message match between the sent and received CAN messages.

## Test Debug

* Verify the hardware connection between CAN port on the starter kit and PMOD CAN device
  (Connected externally to the starter kit) before performing the CAN transactions.

## Known Issues and Limitations

* The CAN module is limited to verifying the functionality of CAN transceiver hardware ports only.
* Make sure that the BIST firmware is loaded before performing the CAN transaction. The PMOD CAN port
  is not recognized otherwise.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>