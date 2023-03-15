# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import subprocess
import os
import re

def run_tpm2_getcap_test(label, helpers):
    """List all capabilities and verify expected capabilities"""
    logger = helpers.logger_init(label)
    logger.start_test()

    cmd = "tpm2_getcap -l"
    logger.info("Running " + cmd)
    expected = [
        "algorithms",
        "commands",
        "pcrs",
        "properties-fixed",
        "properties-variable",
        "ecc-curves",
        "handles-transient",
        "handles-persistent",
        "handles-permanent",
        "handles-pcr",
        "handles-nv-index",
        "handles-loaded-session",
        "handles-saved-session",
    ]
    ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
    if ret.returncode:
        logger.error("Failed to run " + cmd)
        return False
    output = ret.stdout
    if not output:
        logger.error("Failed to read tpm2_getcap list")
        return False
    logger.debug("\n" + output)
    for val in expected:
        if val not in output:
            logger.error("Failed to find " + val + " in tpm2_getcap list")
            return False
    return True

def run_tpm2_selftest_test(label, helpers):
    """Verify that tpm2_selftest passes"""
    logger = helpers.logger_init(label)
    logger.start_test()

    cmd = "tpm2_selftest"
    logger.info("Running " + cmd)
    ret = subprocess.run(cmd, check=True)
    if ret.returncode:
        logger.error(cmd + " failed with return code: " + ret)
        return False
    else:
        return True

def run_tpm2_getrandom_test(label, helpers):
    """Verify that tpm2_getrandom can generate unique hash keys"""
    logger = helpers.logger_init(label)
    logger.start_test()

    # Command to get random hash key with byte length of 30
    cmd = "tpm2_getrandom --hex 30"
    logger.info("Running " + cmd + " test")
    random_data = []
    # Generate 10 hash keys
    for i in range(10):
        ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
        if ret.returncode:
            logger.error(cmd + " failed with return code: " + ret)
            return False
        output = ret.stdout
        if not output:
            logger.error("Failed to get random hash key")
            return False
        logger.debug(output)
        random_data.append(output)
    # Check for duplicates
    if len(random_data) == len(set(random_data)):
        return True
    else:
        logger.error("Randomly generated hash keys are not unique")
        return False

def run_tpm2_hash_test(label, helpers):
    """Verify that tpm2_hash returns expected hash key"""
    logger = helpers.logger_init(label)
    logger.start_test()

    output_dir = helpers.get_output_dir(__file__)
    test_file_name = label + "_test.txt"
    with open(output_dir + '/' + test_file_name, 'w') as f:
        f.write("This is a test file to verify tpm2_hash output.")

    cmd = "tpm2_hash " + output_dir + "/" + test_file_name + " --hex"
    logger.info("Running " + cmd)
    ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
    if ret.returncode:
        logger.error(cmd + " failed with return code: " + ret)
        return False
    output = ret.stdout
    if not output:
        logger.error("Failed to get hash key")
        return False
    expected_hash = "6066cf698b08063a2ee8751236c45954bd477d72"
    logger.debug("Expected hash key: " + expected_hash)
    logger.debug("Hash key returned: " + output)
    if output == expected_hash:
        logger.info("Hash key matches expected hash key")
        return True
    else:
        logger.error("Hash key does not match expected hash key")
        return False

def tpm_pcrread(pcr_banks, sha, logger):
    """Helper function to read PCR registers"""
    cmd = "tpm2_pcrread sha" + sha + ":" + pcr_banks
    logger.info("Running " + cmd)
    ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
    if ret.returncode:
        logger.error(cmd + " failed with return code: " + ret)
        return False
    output = ret.stdout
    if not output:
        logger.error("Failed to read PCR registers")
        return False
    pcr_data = output.splitlines()
    pcr_data = [int(re.sub(".*: ", "", i.strip()), 16) for i in pcr_data if "0x" in i]
    logger.debug("pcr_data: " + str(pcr_data))
    return pcr_data

def run_tpm2_pcrread_test(label, helpers):
    """Verify that tpm2_pcrread can read PCR registers"""
    logger = helpers.logger_init(label)
    logger.start_test()

    # PCRs 0-16 should read 0 for both hash algorithms
    hash_algorithms = ['1', '256']
    pcr_banks = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16'

    for sha in hash_algorithms:
        output = tpm_pcrread(pcr_banks, sha, logger)
        if not output:
            logger.error("Failed to read PCR registers")
            return False
        for val in output:
            if val != 0:
                logger.error("PCR register values are not 0 as expected")
                return False
    return True

def tpm_pcrextend(pcr_register, hash_algorithm, sha_data, logger):
    """Helper function to extend PCR register"""
    cmd = "tpm2_pcrextend " + pcr_register + ":sha" + hash_algorithm + "=" + sha_data
    logger.info("Running " + cmd)
    ret = subprocess.run(cmd.split(' '), check=True, capture_output=True, text=True)
    if ret.returncode:
        logger.error(cmd + " failed with return code: " + ret)
        return False
    output = tpm_pcrread(pcr_register, hash_algorithm, logger)
    if not output:
        logger.error("Failed to read PCR register " + pcr_register)
        return False
    return output

def run_tpm2_pcrextend_test(label, helpers):
    """Verify that tpm2_pcrextend can extend PCR register 23"""
    logger = helpers.logger_init(label)
    logger.start_test()

    # Try to extend PCR register 23 with pre-defined hash for both hash algorithms
    # Pass 20 bytes for hash algorithm 1, 32 bytes for 256
    hash_algorithms = ['1', '256']
    pcr_register = '23'
    sha_data = [
        'ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4',
        'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d'
    ]
    for i in range(len(hash_algorithms)):
        read_data = []
        # Extend PCR register 3 times, hash value should change each time
        for j in range(1, 4):
            output = tpm_pcrextend(pcr_register, hash_algorithms[i], sha_data[i], logger)
            if not output:
                logger.error("Failed to extend PCR register " + pcr_register)
                return False
            read_data.append(output[0])
        logger.debug("read_data for sha" + hash_algorithms[i] + ": " + str(read_data))
        matches = list(set([x for x in read_data if read_data.count(x) > 1]))
        if matches:
            logger.error("Failed to extend data on PCR register " + pcr_register)
            logger.debug("Hash matches found: " + str(matches))
            return False
    return True

def run_tpm2_pcrreset_test(label, helpers):
    """Verify that tpm2_pcrreset can reset PCR register 23"""
    logger = helpers.logger_init(label)
    logger.start_test()

    # Try to extend PCR register 23 with pre-defined hash for both hash algorithms,
    # and verify the value is 0 after tpm2_pcrreset
    # Pass 20 bytes for hash algorithm 1, 32 bytes for 256
    hash_algorithms = ['1', '256']
    pcr_register = '23'
    sha_data = [
        'ac3478d69a3c81fa62e60f5c3696165a4e5e6ac4',
        'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d'
    ]

    for i in range(len(hash_algorithms)):
        output = tpm_pcrextend(pcr_register, hash_algorithms[i], sha_data[i], logger)
        if not output:
            logger.error("Failed to extend PCR register " + pcr_register)
            return False
        cmd = "tpm2_pcrreset " + pcr_register
        logger.info("Running " + cmd)
        ret = subprocess.run(cmd.split(' '), check=True)
        if ret.returncode:
            logger.error(cmd + " failed with return code: " + ret)
            return False
        output = tpm_pcrread(pcr_register, hash_algorithms[i], logger)
        if not output:
            logger.error("Failed to read PCR register " + pcr_register)
            return False
        if output[0] != 0:
            logger.error("Failed to reset PCR register " + pcr_register)
            return False
    return True
