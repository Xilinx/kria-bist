# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import os
import shutil
from pathlib import Path
import re


def get_dev_path_speed(port_name, hw_path, logger):
    # Iterate over hw_path to check for device enumeration
    last_index = None
    for index, path in enumerate(hw_path):
        if 'mmc' in path: # MMC-SD enumeration
            bus = 'mmc'
            if path == hw_path[0]:
                speed = 'SD Speed C-class'
            else:
                speed = 'SD Speed UHS-class'
        else:
            bus = 'usb'
            if 'SD' in port_name: # USB-SD enumeration
                speed = 'SD Speed class'
            elif path == hw_path[0]:
                speed = 'USB 2.0'
            else:
                speed = 'USB 3.0'
        # Obtain /dev/{sdx} device path
        disk_part = find_block(bus, path)
        if disk_part is not None:
            last_index = index
            break
        elif index == (len(hw_path) - 1):
            logger.error(f"No media detected at {port_name} port")
            return None, None, None
    device_path = f"/dev/{disk_part}"
    if 'SD' in port_name:
        # To select ext4 partition on the disk
        if 'mmc' in hw_path[last_index]:
            partition_device = f"{device_path}p2"  # MMC-SD adapter enumeration: /dev/{mmcblkxp2}
        else:
            partition_device = f"{device_path}2"  # USB-SD adapter enumeration: /dev/{sdx2}
    else:
        partition_device = f"{device_path}1"  # Consider first device path partition /dev/{sdx1} if exists
    if os.path.exists(partition_device):  # Check if partitions exist to update device path - /dev/{mmcblkxp2/sdx/sdx2/sdx1}
        device_path = partition_device
    logger.info(f"Device path of {port_name} port: {device_path} ")
    logger.info(f"Device data transfer standard: {speed}")
    return disk_part, device_path, speed


def find_block(bus, path, max_depth=3):
    # Create path object for searching the device block directory
    if bus == 'usb':
        search_path = Path(f"/sys/bus/usb/devices/{path}/")
    elif bus == 'mmc':
        search_path = Path("/sys/bus/mmc/devices/")
        mmc_path = re.compile(f"{path}.*")
        for sub_dir in search_path.iterdir():
            if mmc_path.match(sub_dir.name):
                search_path = sub_dir
                break
        else:
            return None
    # Check if the device block exists
    if not search_path.exists():
        return None
    block_path = re.compile(r"(?:.*/){0," + str(max_depth) + r"}block$")
    # Traverse and check for "block" directory till maximum depth
    for block_sub_dir in search_path.glob("**/*"):
        if block_path.match(str(block_sub_dir)):
            for dev_path in block_sub_dir.iterdir():
                return dev_path.name


def check_disk_space(device_path, data_size, logger):
    # Check available space on the disk to proceed with the test
    space_result = subprocess.run(["df", device_path], capture_output=True, text=True)
    if space_result.returncode:
        logger.error(f"Error retrieving available storage space on the disk")
        return False
    # Extract size in 1K blocks
    line = space_result.stdout.split('\n')[1]
    size_blocks = int(line.split()[1])
    # Convert size in 1K blocks to MiB
    size = round((size_blocks / 1024), 2)
    logger.info(f"Available disk space: {size}MiB")
    if size < data_size:
        logger.error(f"Insufficient memory on the disk. Minimum free space of {data_size}MiB is required to execute the test.")
        return False
    else:
        return True


def mount_device(dev_path, port_name, mount_path, logger):
    try:
        os.makedirs(mount_path, exist_ok=True)
    except OSError:
        logger.error(f"Error creating directory {mount_path} to mount {dev_path} for {port_name} port")
        return False
    mount_result = subprocess.run(["mount", dev_path, mount_path], check=True)
    if mount_result.returncode:
        logger.error(f"Error mounting {dev_path} device at {mount_path} for {port_name} port")
        return False
    logger.info(f"Device mounted. Mountpoint: {dev_path} on {mount_path}\n")
    return True


def unmount_device(mount_point, port_name, logger):
    flag = "-l" # Lazy unmount to safely unmount the volume and reuse the mount_point if needed.
    # Through lazy unmount, the volume is still mounted but not accessible through the filesystem and unmounted only after finishing the task performed on the files.
    unmount_result = subprocess.run(["umount", flag, mount_point], check=True)
    if unmount_result.returncode:
        logger.warning(f"Device could not be unmounted at {mount_point} for {port_name} port")
    else:
        logger.info(f"Device unmounted")


def get_write_speed(write_path, data_size, logger):
    # Check write performance of the disk
    count = str(data_size // 32) # Equate block size * count to required data size
    write_cmd = f'dd if=/dev/urandom of={write_path} bs=32M count={count} oflag=dsync iflag=fullblock'
    write_result = subprocess.run(write_cmd.split(), capture_output=True, text=True)
    if write_result.returncode:
        logger.error(f"{write_cmd} failed with return code: {str(write_result.returncode)}")
        return None
    write_output = write_result.stderr # Extract performance information message written to 'stderr' by 'dd' command
    # Extract the measured write performance from the information message
    for line in write_output.split('\n'):
        if 'bytes' in line and 's, ' in line:
            write_spd = line.split('s, ')[1].split(' ')[0]
            return write_spd
    return None


def clear_cache(logger):
    with open('/proc/sys/vm/drop_caches', 'w') as f:
        written_len = f.write('3\n')  # To clear pagecache, dentries and inodes
        f.flush()
    if written_len != len('3\n'):
        logger.error("Failed to clear pagecache, dentries and inodes")
        return False  # Error occurred performing file operations
    return True  # File operations successful


def get_read_speed(read_path, data_size, logger):
    # Check read performance of the disk
    count = str(data_size // 32) # Equate block size * count to required data size
    read_cmd = f'dd of=/dev/null if={read_path} bs=32M count={count} oflag=dsync iflag=fullblock'
    read_result = subprocess.run(read_cmd.split(), capture_output=True, text=True)
    if read_result.returncode:
        logger.error(f"{read_cmd} failed with return code: {str(read_result.returncode)}")
        return None
    read_output = read_result.stderr  # Extract performance information message written to 'stderr' by 'dd' command
    # Extract the measured read performance from the information message
    for line in read_output.split('\n'):
        if 'bytes' in line and 's, ' in line:
            read_spd = line.split('s, ')[1].split(' ')[0]
            return read_spd
    return None


def log_disk_performance(measured_speed, mode, port_name, port_speed, logger):
    if measured_speed is None:
        logger.error(f"Failed to parse {mode} speed")
        return False
    speed_dict = {
        'SD Speed C-class': {'Read': 6, 'Write': 2},
        'SD Speed UHS-class': {'Read': 12, 'Write': 6},
        'SD Speed class': {'Read': 6, 'Write': 2},
        'USB 2.0': {'Read': 9, 'Write': 2},
        'USB 3.0': {'Read': 80, 'Write': 8}
    }
    # Minimum read speed expectation for the port
    min_speed = speed_dict[port_speed][mode]
    logger.info(f"Minimum expected {mode} speed for {port_speed} devices: {min_speed} MB/s")
    logger.info("The indicated threshold values may not be accurate for your specific device. Please verify correct values with the device manufacturer"
    logger.info(f"Measured {mode} speed: {str(measured_speed)} MB/s")
    # Compare measured speed with expected speed
    if float(measured_speed) < min_speed:
        logger.error(f"{mode} performance test failed for {port_name} port\n")
        return False
    logger.info(f"{mode} performance test passed for {port_name} port\n")
    return True


def remove_test_dir(test_file, mount_directory, port_name, logger):
    os.remove(test_file)  # Remove test file
    unmount_device(mount_directory, port_name, logger)  # Unmount test directory
    test_directory = os.path.dirname(mount_directory)
    shutil.rmtree(test_directory, ignore_errors=True)  # Remove test directory


def run_disk_performance(label, hw_path, mode, helpers):
    logger = helpers.logger_init(label)
    logger.start_test()
    port_name = label.split('_')[0].upper()  # Strip the port name
    data_size = 128  # To set data size to 128MiB
    # Obtain /dev/{sdx/mmcblxpx} device path and data transfer standard/ speed of the port
    disk_part, device_path, port_speed = get_dev_path_speed(port_name, hw_path, logger)
    if disk_part is None:
        return False
    # Check for available storage on the disk
    disk_space = check_disk_space(device_path, data_size, logger)
    if not disk_space:
        return False
    # Mount the disk under test
    mount_path = f"/media/disk/{disk_part}"
    mounted = mount_device(device_path, port_name, mount_path, logger)
    if not mounted:
        return False
    test_file = f'{mount_path}/test'
    mount_directory = os.path.dirname(test_file)
    # Performance test based on write, read and read_write modes
    match mode:
        case 'w':
            wr_speed = get_write_speed(test_file, data_size, logger)
            write_test = log_disk_performance(wr_speed, 'Write', port_name, port_speed, logger)
            if not write_test:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
        case 'r':
            # Write to test file for measuring the read performance
            wr_speed = get_write_speed(test_file, data_size, logger)
            if wr_speed is None:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
            cache_cleared = clear_cache(logger)
            if not cache_cleared:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
            rd_speed = get_read_speed(test_file, data_size, logger)
            read_test = log_disk_performance(rd_speed, 'Read', port_name, port_speed, logger)
            if not read_test:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
        case 'rw':
            wr_speed = get_write_speed(test_file, data_size, logger)
            write_test = log_disk_performance(wr_speed, 'Write', port_name, port_speed, logger)
            if not write_test:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
            cache_cleared = clear_cache(logger)
            if not cache_cleared:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
            rd_speed = get_read_speed(test_file, data_size, logger)
            read_test = log_disk_performance(rd_speed, 'Read', port_name, port_speed, logger)
            if not read_test:
                 remove_test_dir(test_file, mount_directory, port_name, logger)
                 return False
    remove_test_dir(test_file, mount_directory, port_name, logger)
    return True
