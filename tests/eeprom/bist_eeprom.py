# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import glob
import subprocess

def run_eeprom_test(label, eeprom_addr, field, value, helpers):
    logger = helpers.logger_init(label)
    logger.start_test()
    eeprom_file = glob.glob('/sys/devices/platform/axi/*.i2c/*/*' + eeprom_addr + '/eeprom')[0]
    ret, fru = subprocess.getstatusoutput('/usr/sbin/ipmi-fru' + ' --fru-file=' + eeprom_file  + ' --interpret-oem-data')
    data_from_eeprom = fru.split(field+": ",1)[1].split("\n",1)[0].strip()

    if field == "FRU Board Product Name":
        data_from_eeprom = data_from_eeprom.split("-")[1]

    logger.info(fru + "\n")
    logger.info("Expected " + field + " is: " + str(value))
    logger.info(field + " from EEPROM: " + data_from_eeprom)

    # Check if ipmi-fru returns an error code
    if (ret != 0):
        # This if condition is an exception for a known EEPROM issue
        if "ipmi_fru_next: multirecord area checksum invalid" in fru:
            logger.warning("A multirecord area checksum is invalid. This is likely a known issue. Please double check the EEPROM output.")
        else:
            logger.error("Error reading EEPROM")
            logger.test_failed()
            logger.stop_test()
            return False

    if data_from_eeprom == value:
        logger.test_passed()
        logger.stop_test()
        return True
    else:
        logger.test_failed()
        logger.stop_test()
        return False
