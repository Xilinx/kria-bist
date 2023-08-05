# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import can
import glob
import time
import re
import os
import subprocess


def get_can_node(can_controller, logger):
    """
    Get CAN node of the device under test

    Args:
        can_controller: CAN controller
        logger: Calling function's logger object

    Returns:
        str: CAN node
    """
    can_base_path = f"/sys/class/net/can*/device/modalias"
    can_modalias_files = glob.glob(can_base_path)
    if not can_modalias_files:
        logger.error(f"Error finding CAN node for '{can_controller}' device")
        return None
    for can_modalias_file in can_modalias_files:
        with open(can_modalias_file, 'r') as f:
            controller_contents = f.read()
            if can_controller in controller_contents:
                # Extract the can node of the form canX from the modalias file path
                can_interface = os.path.basename(os.path.dirname(os.path.dirname(can_modalias_file)))
                logger.info(f"CAN node for '{can_controller}': {can_interface} ")
                return can_interface
    logger.error(f"Error finding CAN node for '{can_controller}' device")
    return None


def can_node_initialize(can_channel, buffer_length, baudrate, logger):
    """
    Initialize CAN node/ channel for communication

    Args:
        can_channel: CAN node/ channel
        buffer_length: Transmit buffer length
        baudrate: Baudrate for communication
        logger: Calling function's logger object

    Returns:
        can_bus: CAN device bus object
    """
    # Set baudrate for the can interface
    can_baudrate_cmd = ["ip", "link", "set", can_channel, "type", "can", "bitrate", str(baudrate)]
    set_baudrate_result = subprocess.run(can_baudrate_cmd, capture_output=True, text=True)
    if set_baudrate_result.returncode:
        logger.error(f"Error setting baudrate for node: {can_channel}")
        return None  
    logger.debug(f"Baudrate of {can_channel} set to {baudrate}")
    # Set transmit buffer length
    set_txbuffer_result = subprocess.run(["ifconfig", can_channel, "txqueuelen",  str(buffer_length)], capture_output=True, text=True)
    if set_txbuffer_result.returncode:
        logger.error(f"Error setting {can_channel} transmit buffer length: {buffer_length}")
        return None
    logger.debug(f"Transmit queue length of {can_channel} set to {buffer_length}")
    # Set CAN node to state 'up'
    set_can_result = subprocess.run(["ip", "link", "set", can_channel, "up"], capture_output=True, text=True)
    if set_can_result.returncode:
        logger.error(f"Error setting {can_channel} interface state: up")
        return None
    logger.debug(f"CAN interface {can_channel} is set to state: up")
    try:
        bus = can.interface.Bus(channel=can_channel, bustype='socketcan', bitrate=baudrate)
        logger.debug(f"Initialized node {can_channel}")
        return bus
    except can.CanError as e:
        logger.error(f"Error initializing CAN node: {can_channel} - {e}")
        return None


def send_can_message(can_transmit_bus, can_transmitter_node, can_transmit_message, logger):
    """
    Send CAN message from transmitter node

    Args:
        can_transmit_bus: CAN transmitter bus instance
        can_transmitter_node: CAN message transmitter node
        can_transmit_message: CAN message to be transmitted
        logger: Calling function's logger object

    Returns:
        bool: True/False
    """
    try:
        msg = can.Message(arbitration_id=0x123, data=can_transmit_message, is_extended_id=False)
    except Exception as e:
        logger.error(f"Error creating CAN message object - {e}")
        return False
    try:
        can_transmit_bus.send(msg)
        can_transmit_bus.send(msg) # Send CAN message twice to avoid any transaction errors
        logger.info(f"Message sent from node {can_transmitter_node}: {can_transmit_message}")
        return True
    except can.CanError as e:
        logger.error(f"Error sending CAN message from node {can_transmitter_node}: {can_transmit_message} - {e}")
        return False


def read_can_message(can_receive_bus, can_receiver_node, logger):
    """
    Read CAN message from receiver node

    Args:
        can_receive_bus: CAN receiver bus instance
        can_receiver_node: CAN message receiver node
        logger: Calling function's logger object

    Returns:
        str: CAN message received
    """
    try:
        can_received_msg = can_receive_bus.recv(1)  # Timeout in seconds
        logger.info(f"Message received at node {can_receiver_node}: {can_received_msg.data}")
        return can_received_msg.data
    except can.CanError as e:
        logger.error(f"Error reading CAN message from node {can_receiver_node} - {e}")
        return None


def can_node_shutdown(can_bus, can_channel, logger):
    """
    Shutdown CAN node

    Args:
        can_bus: CAN bus instance
        can_channel: CAN node for shutting down
        logger: Calling function's logger object
    """
    try:
        can_bus.shutdown()
        logger.debug(f"CAN node {can_channel} shutdown")
    except can.CanError as e:
        logger.error(f"Error shutting down CAN node {can_channel} - {e}")
    # Set CAN node to state 'down'
    set_can_result = subprocess.run(["ip", "link", "set", can_channel, "down"], capture_output=True, text=True)
    if set_can_result.returncode:
        logger.error(f"Error setting {can_channel} interface state: down")
    logger.debug(f"CAN interface {can_channel} is set to state: down")


def run_can_transmission_test(label, can_transmitter, can_receiver, helpers):
    """
    CAN message transmission test

    Args:
        label: Test label
        can_transmitter: CAN message transmitter
        can_receiver: CAN message receiver
        helpers: Fixture for helper functions

    Returns:
        bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    baudrate = 100000  # Choose baudrate of 100Kbps for communication between CAN nodes
    buffer_length = 1000  # To set transmit buffer length
    can_transmit_message = bytes([1, 2, 3, 4, 5])
    can_transmitter_node = get_can_node(can_transmitter, logger)
    if can_transmitter_node is None:
        return False
    can_receiver_node = get_can_node(can_receiver, logger)
    if can_receiver_node is None:
        return False
    can_transmit_bus = can_node_initialize(can_transmitter_node, buffer_length, baudrate, logger)
    if can_transmit_bus is None:
        return False
    can_receive_bus = can_node_initialize(can_receiver_node, buffer_length, baudrate, logger)
    if can_receive_bus is None:
        can_node_shutdown(can_transmit_bus, can_transmitter_node, logger)
        return False
    can_message_transmit = send_can_message(can_transmit_bus, can_transmitter_node, can_transmit_message, logger)
    if can_message_transmit is False:
        can_node_shutdown(can_transmit_bus, can_transmitter_node, logger)
        can_node_shutdown(can_receive_bus, can_receiver_node, logger)
        return False
    # Allow sufficient time for the CAN message detection at the receiver node
    time.sleep(1)
    can_receive_message = read_can_message(can_receive_bus, can_receiver_node, logger)
    if can_receive_message is None:
        can_node_shutdown(can_transmit_bus, can_transmitter_node, logger)
        can_node_shutdown(can_receive_bus, can_receiver_node, logger)
        return False
    if can_transmit_message != can_receive_message:
        logger.error("CAN message received does not match with transmitted message")
        logger.error("CAN communication failed")
        can_node_shutdown(can_transmit_bus, can_transmitter_node, logger)
        can_node_shutdown(can_receive_bus, can_receiver_node, logger)
        return False
    logger.info("CAN message received matches with transmitted message")
    logger.info("CAN communication successful")
    can_node_shutdown(can_transmit_bus, can_transmitter_node, logger)
    can_node_shutdown(can_receive_bus, can_receiver_node, logger)
    return True
