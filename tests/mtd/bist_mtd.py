# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import subprocess
import os
import filecmp
import tempfile


def get_user_partition_size(logger):
    """
    Get "User" MTD partition

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
            logger.info(f"MTD User partition: {mtd_partition}")            
            mtd_partition_size = round((float(line.split()[4]) / 1024 / 1024), 2)  # To convert to MiB
            logger.info(f"Size of MTD User partition: {mtd_partition_size}MiB")
            return mtd_partition, mtd_partition_size
    logger.error("MTD User partition not available on the board")
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
    Write the test file to User MTD partition

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
        logger.error("Error writing test file to MTD User partition")
        return False
    logger.info("MTD write of test file successful")
    return True


def mtd_debug_read(mtd_user_partition, offset, length, test_file, logger):
    """
    Read the test file from User MTD partition

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
        logger.error("Error reading test file from MTD User partition")
        return False
    logger.info("MTD read of test file successful")
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
       logger.error("Test file written to MTD partition does not exist for file comparison")
       return False
    if not os.path.exists(read_test_file):
       logger.error("Test file read from MTD partition does not exist for file comparison")
       return False
    if not filecmp.cmp(write_test_file, read_test_file, shallow=False):
       logger.error("Test file mismatch between written and read-back data on MTD partition")
       return False
    logger.info("Test file match between written and read-back data on MTD partition")
    return True    


def run_mtd_read_write_test(label, helpers):
    """
    MTD read write test

    Args:
            label: Test label
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    data_size = 1 # To set data size to 1MiB
    offset = 0 # Address offset at the mtd partition
    length = data_size * 1048576 # To convert MiB to bytes
    bist_mtd_write_file = tempfile.NamedTemporaryFile(delete=False)
    bist_mtd_read_file = tempfile.NamedTemporaryFile(delete=False)
    # Obtain MTD user partition and size of the partition
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
        logger.error("MTD read and write test failed")
        os.unlink(bist_mtd_write_file.name)
        os.unlink(bist_mtd_read_file.name)
        return False
    logger.info("MTD read and write test passed")
    os.unlink(bist_mtd_write_file.name)
    os.unlink(bist_mtd_read_file.name)
    return True
