# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import subprocess

def run_fancontrol_test(label, helpers):
    logger = helpers.logger_init(label)
    logger.start_test()

    logger.info("This test involves stopping the fancontrol service. "
                "If the test fails, the service may need to be restarted manually."
                "\nTo perform this test, use the prompt below to stop fancontrol, "
                "observe that the fan spins at full speed, and restart fancontrol.")

    logger.info("\nType Y to stop fancontrol:")
    while(1):
        var = input().strip().upper()
        if var == 'Y':
            logger.info("Stopping fancontrol")
            logger.info("The fan should now be spinning at full speed")
            subprocess.run("systemctl stop fancontrol.service", shell=True)
            break
        else:
            logger.info("Invalid input, try again")

    logger.info("\nIs the fan spinning at full speed? [Y/N]")
    while(1):
        var = input().strip().upper()
        if var == 'Y':
            logger.info("Restarting fancontrol")
            subprocess.run("systemctl start fancontrol.service", shell=True)
            break
        elif var == 'N':
            logger.test_failed()
            logger.stop_test()
            return False
        else:
            logger.info("Invalid input, try again")

    logger.info("\nIs the fancontrol service running? (The fan should not be spinning at full speed) [Y/N]")
    while(1):
        var = input().strip().upper()
        if var == 'Y':
            logger.test_passed()
            logger.stop_test()
            return True
        elif var == 'N':
            logger.test_failed()
            logger.stop_test()
            return False
        else:
            logger.info("Invalid input, try again")
