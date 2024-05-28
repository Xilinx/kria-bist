# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import os
import signal
import subprocess
import netifaces
import ipaddress
from ping3 import ping
import glob
from time import sleep
import re


def eth_get_interface_speed(phy_addr, logger):
    """
    Get the eth interface and speed based on PHY address.

    Args:
            phy_addr: PHY address
            logger: Calling function's logger object

    Returns:
            string: eth interface
            float: Max speed in Gb/s
    """
    # Get list of eth interfaces
    interface_list = [interface for interface in netifaces.interfaces() if "eth" in interface]

    # Check for SFP case where PHY address is None
    if phy_addr is None:
        # Find eth interface without a PHY
        for interface in interface_list:
            if glob.glob("/sys/class/net/" + interface + "/phydev") == []:
                logger.debug("The SFP interface is: " + interface)
                # Default speed for SFP
                sfp_max_speed = 0.5 # Gbps
                return interface, sfp_max_speed

    # Check for matching PHY address
    for interface in interface_list:
        cmd = "ethtool " + interface
        ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
        if ret.returncode:
            logger.error("Failed to run " + cmd)
            return None, None
        output = ret.stdout
        if not output:
            logger.error("Failed to read ethtool output")
            return None, None
        phy_addr_string = "PHYAD: " + str(phy_addr)
        if phy_addr_string in output:
            speed = eth_get_speed(interface, logger)
            return interface, speed
    return None, None

def eth_get_speed(eth_interface, logger):
    """
    Get the max speed for the eth interface.

    Args:
            eth_interface: Name of eth interface
            logger: Calling function's logger object

    Returns:
            float: Max speed in Gb/s
    """
    cmd = "ethtool " + eth_interface
    ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
    if ret.returncode:
        logger.error("Failed to run " + cmd)
        return None
    output = ret.stdout
    if not output:
        logger.error("Failed to read ethtool output")
        return None
    # Get speed and convert to Gb/s
    try:
        speed_gbps = int(output.split('Speed: ')[1].split('Mb/s')[0])/1000
        logger.debug("The max speed for " + eth_interface + " is " + str(speed_gbps) + " Gb/s")
    except:
        logger.error("Unable to get max speed for " + eth_interface)
        return None
    return speed_gbps

def eth_setup(label, eth_interface, logger):
    """
    Verify that remote host IP and board IP are in the same subnet.
    If they aren't, add a static IP.

    Args:
            label: Test label
            eth_interface: Name of eth interface
            logger: Calling function's logger object

    Returns:
            interface_ip: Interface IP which is in the same subnet as remote host
            host_ip: Host IP of the appropriate interface
    """

    if "sfp" in label:
        # Check if BIST_REMOTE_HOST_SFP_IP env var is defined
        host_ip = os.getenv('BIST_REMOTE_HOST_SFP_IP', default=None)
        if host_ip == None:
            logger.error("Please set the BIST_REMOTE_HOST_SFP_IP environment variable.")
            return False, False
        logger.info("The remote host SFP IP is currently set to " + host_ip)
    else:
        # Check if BIST_REMOTE_HOST_IP env var is defined
        host_ip = os.getenv('BIST_REMOTE_HOST_IP', default=None)
        if host_ip == None:
            logger.error("Please set the BIST_REMOTE_HOST_IP environment variable.")
            return False, False
        logger.info("The remote host IP is currently set to " + host_ip)

    # Check if interface already has an IP in the same subnet as remote host
    try:
        interface_ips = [data['addr'] for data in netifaces.ifaddresses(eth_interface)[netifaces.AF_INET]]
    except:
        logger.error("No interface IP found for " + str(eth_interface) + ". Please set a Static IP or use DHCP")
        return False, False

    logger.debug(str(eth_interface) + " IPs: " + str(interface_ips))
    # Remove Host ID from interface ip and add /24 subnet mask
    ip_networks = [".".join(interface_ip.split('.')[:-1]) + '.0/24' for interface_ip in interface_ips]
    logger.debug("IP networks: " + str(ip_networks))
    for i in range(len(ip_networks)):
        if (ipaddress.ip_address(host_ip) in ipaddress.ip_network(ip_networks[i])):
            logger.debug("Remote host IP " + host_ip + " is in IP network " + ip_networks[i])
            return interface_ips[i], host_ip
        else:
            logger.error("Remote host IP " + host_ip + " is not in IP network " + ip_networks[i])
            return False, False

def run_eth_ping_test(label, phy_addr, helpers):
    """
    Attempt to ping remote host

    Args:
            label: Test label
            phy_addr: PHY address
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()

    eth_interface, _ = eth_get_interface_speed(phy_addr, logger)
    if eth_interface is None:
        logger.error("Failed to get eth interface")
        return False

    _, host_ip = eth_setup(label, eth_interface, logger)
    if not host_ip:
        return False

    logger.info("Pinging remote host " + host_ip)
    ping_result = ping(host_ip, interface=eth_interface)
    logger.info("Delay: " + str(ping_result))

    # ping returns delay if successful, False otherwise
    if ping_result:
        return True
    else:
        return False


def get_bitrate(iperf3_output, logger):
    """
    Get the average bitrate from iperf3 output

    Args:
            iperf3_output: iperf3 command line output
            logger: Handle for logging

    Returns:
            float: Average value of bitrate
    """
    bitrate_list = re.findall(r"(\d+(?:\.\d+)?)\s+Mbits/sec", iperf3_output)
    if len(bitrate_list) > 0:
        # Get the last value from list of values which is the average
        average_bitrate = bitrate_list[-1]
        return float(average_bitrate)
    else:
        logger.error("Bitrate was not recorded")
        return False


def run_eth_perf_test(label, phy_addr, helpers):
    """
    Perf test with remote host as the server

    Args:
            label: Test label
            phy_addr: PHY address
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()

    eth_interface, max_speed_gbps = eth_get_interface_speed(phy_addr, logger)
    if eth_interface is None or max_speed_gbps is None:
        logger.error("Failed to get eth interface and speed")
        return False

    interface_ip, host_ip = eth_setup(label, eth_interface, logger)
    if not interface_ip or not host_ip:
        return False

    # iperf3 command,run it for 5 seconds,display rate in Mbits/sec,use zerocopy flag
    iperf3_cmd = f"iperf3 -c {host_ip} -B {interface_ip} -f m -t 5 -Z"
    # Run the iperf3 command
    try:
        process = subprocess.Popen(iperf3_cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout, stderr = process.communicate(timeout=10)
    except subprocess.TimeoutExpired as e:
        logger.error("iperf3 command timed out after " + str(e.timeout) + " seconds.")
        os.kill(process.pid, signal.SIGKILL)
        return False
    if process.returncode:
        logger.error("iperf3 failed to measure bitrate. "
            "Please ensure the remote host IP is correct and an iperf3 server is running on the remote host.")
        os.kill(process.pid, signal.SIGKILL)
        return False
    iperf3_output = stdout.decode('utf8')
    logger.debug(iperf3_output)

    # Check if measured bitrate is above threshold
    iperf3_result = get_bitrate(iperf3_output, logger)
    if not iperf3_result:
        return False

    perf_speed_threshold = 800
    if iperf3_result >= perf_speed_threshold:
        return True
    else:
        logger.error("The measured bitrate is lower than " + str(int(perf_speed_threshold/10)) + "% of the "
            "max bitrate of " + str(max_speed_gbps) + " Gbits/sec")
        return False
