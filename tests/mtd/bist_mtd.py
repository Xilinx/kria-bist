# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import os
import filecmp
import tempfile


def get_user_partition_size(logger):
    """
    Get "User" MTD partition on QSPI

    Args:
            logger: Calling function's logger object

    Returns:
            str: MTD User partition
            float: MTD User partition size
    """
    lsmtd_cmd = "lsmtd -b DEVICE, NAME, SIZE"
    mtd_result = subprocess.run(lsmtd_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if mtd_result.returncode:
        logger.error("Error listing MTD partitions on the board")
        return None, None
    for line in mtd_result.stdout.split('\n'):
        if "User" in line:
            mtd_partition = line.split()[0]
            logger.info(f"MTD User partition on QSPI: {mtd_partition}")
            mtd_partition_size = round((float(line.split()[4]) / 1024 / 1024), 2)  # To convert to MiB
            logger.info(f"Size of MTD User partition: {mtd_partition_size}MiB")
            return mtd_partition, mtd_partition_size
    logger.error("MTD User partition not available on the QSPI")
    return None, None
   

def write_random_data(length, write_test_file, logger):
    """
    Write random data into test file used for MTD write

    Args:
            write_test_file: Test file to write the data to
            length: Data length
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    random_data = os.urandom(length)
    bytes_written = write_test_file.write(random_data)
    if bytes_written != length:
        logger.error("Error writing data into test file")
        return False
    logger.debug("Test file write successful")
    return True
    
    
def mtd_debug_erase(mtd_user_partition, offset, length, logger):
    """
    MTD partition data erase

    Args:
            mtd_user_partition: User partition for data erase
            offset: Address offset
            length: Data length
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    erase_cmd = f"mtd_debug erase /dev/{mtd_user_partition} {offset} {length}"
    erase_result = subprocess.run(erase_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    length_mib = length / 1048576  # To convert length to MiB
    if erase_result.returncode:
        logger.error(f"Failed to erase {length_mib}MiB of memory starting at offset of {offset} bytes on MTD User partition")
        return False
    logger.info(f"Memory erase successful. {length_mib}MiB of memory erased at offset {offset} bytes on MTD User partition")
    return True


def mtd_debug_write(mtd_user_partition, offset, length, test_file, logger):
    """
    Write the test file to User MTD partition on QSPI

    Args:
            mtd_user_partition: User partition for writing test file
            offset: Address offset
            length: Data length
            test_file: Test file that is written to the partition
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    write_cmd = f"mtd_debug write /dev/{mtd_user_partition} {offset} {length} {test_file}"
    write_result = subprocess.run(write_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if write_result.returncode:
        logger.error("Error writing test file to QSPI MTD User partition")
        return False
    logger.info("\nQSPI write of test file successful")
    return True


def mtd_debug_read(mtd_user_partition, offset, length, test_file, logger):
    """
    Read the test file from User MTD partition on QSPI

    Args:
            mtd_user_partition: User partition for reading test file
            offset: Address offset
            length: Data length
            test_file: Test file that is read from the partition
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    read_cmd = f'mtd_debug read /dev/{mtd_user_partition} {offset} {length} {test_file}'
    read_result = subprocess.run(read_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if read_result.returncode:
        logger.error("Error reading test file from QSPI MTD User partition")
        return False
    logger.info("QSPI read of test file successful")
    return True


def compare_files(write_test_file, read_test_file, logger):
    """
    Compare Read and Write test files

    Args:
            write_test_file: Test file written to mtd partition
            read_test_file: Test file read from mtd partition
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    if not os.path.exists(write_test_file):
       logger.error("Test file written to QSPI MTD partition does not exist for file comparison")
       return False
    if not os.path.exists(read_test_file):
       logger.error("Test file read from QSPI MTD partition does not exist for file comparison")
       return False
    if not filecmp.cmp(write_test_file, read_test_file, shallow=False):
       logger.error("Test file mismatch between written and read-back data on MTD partition\n")
       return False
    logger.info("Test file match between written and read-back data on MTD partition\n")
    return True


def clear_cache(logger):
    """
    Clear cache for accurate read write performance

    Args:
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    with open('/proc/sys/vm/drop_caches', 'w') as f:
        written_len = f.write('3\n')  # To clear pagecache, dentries and inodes
        f.flush()
    if written_len != len('3\n'):
        logger.error("Failed to clear pagecache, dentries and inodes")
        return False  # Error occurred performing file operations
    logger.debug("Cleared pagecache, dentries and inodes")
    return True  # File operations successful


def get_qspi_write_performance(mtd_user_partition, offset, block_size, length, logger):
    """
    Obtain QSPI write performance

    Args:
            mtd_user_partition: QSPI User partition to write data to
            offset: Address offset
            block_size: Block size of data transfer
            length: Data length
            logger: Calling function's logger object

    Returns:
            float: QSPI write performance in KB/s
    """
    qspi_write_cmd = f'dd if=/dev/urandom of=/dev/{mtd_user_partition} bs={block_size} seek={offset // block_size} count={length // block_size} oflag=dsync iflag=fullblock'
    qspi_write_result = subprocess.run(qspi_write_cmd.split(), capture_output=True, text=True)
    if qspi_write_result.returncode:
        logger.error(f"{qspi_write_cmd} failed with return code: {str(qspi_write_result.returncode)}")
        return None
    qspi_write_output = qspi_write_result.stderr  # Extract performance information message written to 'stderr' by 'dd' command
    # Extract the measured QSPI write performance from the information message
    for line in qspi_write_output.split('\n'):
        if 'bytes' in line and 's, ' in line:
            qspi_write_spd = line.split('s, ')[1].split(' ')[0]
            return float(qspi_write_spd)
    logger.error(f"Failed to parse QSPI Write speed")
    return None


def get_qspi_read_performance(mtd_user_partition, offset, block_size, length, logger):
    """
    Obtain QSPI read performance

    Args:
            mtd_user_partition: QSPI User partition to read data from
            offset: Address offset
            block_size: Block size of data transfer
            length: Data length
            logger: Calling function's logger object

    Returns:
            float: QSPI read performance in MB/s
    """
    qspi_read_cmd = f'dd of=/dev/null if=/dev/{mtd_user_partition} bs={block_size} skip={offset // block_size} count={length // block_size} oflag=dsync iflag=fullblock'
    qspi_read_result = subprocess.run(qspi_read_cmd.split(), capture_output=True, text=True)
    if qspi_read_result.returncode:
        logger.error(f"{qspi_read_cmd} failed with return code: {str(qspi_read_result.returncode)}")
        return None
    qspi_read_output = qspi_read_result.stderr  # Extract performance information message written to 'stderr' by 'dd' command
    # Extract the measured QSPI read performance from the information message
    for line in qspi_read_output.split('\n'):
        if 'bytes' in line and 's, ' in line:
            qspi_read_spd = line.split('s, ')[1].split(' ')[0]
            return float(qspi_read_spd)
    logger.error(f"Failed to parse QSPI Read speed")
    return None


def log_qspi_performance(qspi_measured_speed, mode, qspi_min_speed, logger):
    """
    Log QSPI read/write performance result

    Args:
            qspi_measured_speed: Test label
            mode: mode: Performance mode (Read/Write/ReadWrite)
            qspi_min_speed: Minimum expected read/write speed
            logger: Calling function's logger object

    Returns:
            bool: True/False
    """
    if mode == "Read":
        logger.info(f"\nMinimum expected {mode} speed for QSPI MTD partition: {qspi_min_speed} MB/s")
        logger.info(f"Measured {mode} speed: {str(qspi_measured_speed)} MB/s")
    else:
        logger.info(f"\nMinimum expected {mode} speed for QSPI MTD partition: {qspi_min_speed} KB/s")
        logger.info(f"Measured {mode} speed: {str(qspi_measured_speed)} KB/s")
    # Compare measured speed with expected speed
    if float(qspi_measured_speed) < qspi_min_speed:
        logger.error(f"\nQSPI {mode} performance test failed")
        return False
    logger.info(f"\nQSPI {mode} performance test passed")
    return True


def run_qspi_read_write_test(label, helpers):
    """
    QSPI read write test

    Args:
            label: Test label
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    data_size = 1 # To set data size to 1MiB
    # Address offset set for 3 sectors at mtd User partition until device tree update with correct QSPI partition layout is available
    offset = 196608 # Address offset set for 3 sectors (192KB)
    length = data_size * 1048576 # To convert MiB to bytes
    bist_mtd_write_file = tempfile.NamedTemporaryFile(delete=False)
    bist_mtd_read_file = tempfile.NamedTemporaryFile(delete=False)
    # Obtain MTD User partition and size of the partition
    mtd_user_partition, mtd_partition_size = get_user_partition_size(logger)
    if mtd_user_partition is None:
        return False
    if mtd_partition_size < data_size:
        logger.error(f"Insufficient memory on MTD User partition. Need minimum of {data_size}MiB for test")
        return False
    mtd_test_file_write = write_random_data(length, bist_mtd_write_file, logger)
    if mtd_test_file_write is False:
        return False
    erase_partition = mtd_debug_erase(mtd_user_partition, offset, length, logger)
    if erase_partition is False:
        return False
    mtd_write = mtd_debug_write(mtd_user_partition, offset, length, bist_mtd_write_file.name, logger)
    if mtd_write is False:
        return False
    mtd_read = mtd_debug_read(mtd_user_partition, offset, length, bist_mtd_read_file.name, logger)
    if mtd_read is False:
        return False
    files_match = compare_files(bist_mtd_write_file.name, bist_mtd_read_file.name, logger)
    if files_match is False:
        logger.error("QSPI read and write test failed")
        os.unlink(bist_mtd_write_file.name)
        os.unlink(bist_mtd_read_file.name)
        return False
    logger.info("QSPI read and write test passed")
    os.unlink(bist_mtd_write_file.name)
    os.unlink(bist_mtd_read_file.name)
    return True


def run_qspi_performance_test(label, mode, helpers):
    """
    QSPI performance test

    Args:
            label: Test label
            mode: Performance mode (Read/Write)
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    data_size = 1 # To set data size to 1MiB
    # Address offset set for 3 sectors at mtd User partition until device tree update with correct QSPI partition layout is available
    offset = 196608 # Address offset set for 3 sectors (192KB)
    length = data_size * 1048576 # To convert MiB to bytes
    block_size = 65536 # Block size (in bytes) of mtd partitions on the device
    qspi_min_write_speed = 285 # Minimum expected QSPI write speed in KB/s
    qspi_min_read_speed = 9 # Minimum expected QSPI read speed in MB/s
    # Obtain MTD user partition and size of the partition
    mtd_user_partition, mtd_partition_size = get_user_partition_size(logger)
    if mtd_user_partition is None:
        return False
    if mtd_partition_size < data_size:
        logger.error(f"Insufficient memory on MTD User partition. Need minimum of {data_size}MiB for test")
        return False
    cache_cleared = clear_cache(logger)
    if not cache_cleared:
        return False
    match mode:
        case 'w':
            erase_partition = mtd_debug_erase(mtd_user_partition, offset, length, logger)
            if not erase_partition:
                return False
            qspi_write_speed = get_qspi_write_performance(mtd_user_partition, offset, block_size, length, logger)
            if qspi_write_speed is None:
                return False
            qspi_write_test = log_qspi_performance(qspi_write_speed, 'Write', qspi_min_write_speed, logger)
            if not qspi_write_test:
                return False
        case 'r':
            qspi_read_speed = get_qspi_read_performance(mtd_user_partition, offset, block_size, length, logger)
            if qspi_read_speed is None:
                return False
            qspi_read_test = log_qspi_performance(qspi_read_speed, 'Read', qspi_min_read_speed, logger)
            if not qspi_read_test:
                return False
        case 'rw':
            erase_partition = mtd_debug_erase(mtd_user_partition, offset, length, logger)
            if not erase_partition:
                return False
            qspi_write_speed = get_qspi_write_performance(mtd_user_partition, offset, block_size, length, logger)
            if qspi_write_speed is None:
                return False
            qspi_write_test = log_qspi_performance(qspi_write_speed, 'Write', qspi_min_write_speed, logger)
            if not qspi_write_test:
                return False
            cache_cleared = clear_cache(logger)
            if not cache_cleared:
                return False
            qspi_read_speed = get_qspi_read_performance(mtd_user_partition, offset, block_size, length, logger)
            if qspi_read_speed is None:
                return False
            qspi_read_test = log_qspi_performance(qspi_read_speed, 'Read', qspi_min_read_speed, logger)
            if not qspi_read_test:
                return False
    return True
