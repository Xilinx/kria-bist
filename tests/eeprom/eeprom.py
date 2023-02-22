# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import glob
import subprocess

def run_eeprom_test(eeprom_addr, field, value, logger):
    eeprom_file = glob.glob('/sys/devices/platform/axi/*.i2c/*/*' + eeprom_addr + '/eeprom')[0]
    ret, fru = subprocess.getstatusoutput('/usr/sbin/ipmi-fru' + ' --fru-file=' + eeprom_file  + ' --interpret-oem-data')
    data_from_eeprom = fru.split(field+": ",1)[1].split("\n",1)[0].strip()

    if field == "FRU Board Product Name":
        data_from_eeprom = data_from_eeprom.split("-")[1]

    logger.info(fru)
    logger.info("\nExpected " + field + " is: " + str(value))
    logger.info(field + " from EEPROM: " + data_from_eeprom)

    # Check if ipmi-fru returns an error code
    # There is a known issue for the KV EEPROM and an error is expected.
    # The second if condition below is a workaround for this issue.
    product_name = fru.split("FRU Board Product Name: ",1)[1].split("\n",1)[0].strip()
    if (ret != 0) and (product_name.split("-")[1] != "KV"):
        assert False

    assert data_from_eeprom == value
