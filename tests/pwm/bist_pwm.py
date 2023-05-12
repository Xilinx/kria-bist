# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import glob

def run_fancontrol_test(label, helpers):
    logger = helpers.logger_init(label)
    logger.start_test()

    pwm_file = ""
    fan_speed_max = 255
    fan_speed_slow = 26

    # Get pwm file based on hwmon name
    hwmon_devices = glob.glob("/sys/class/hwmon/*/name")
    for file in hwmon_devices:
        with open(file) as f:
            device_name = f.read().rstrip()
        if device_name == 'pwmfan':
            pwm_file = glob.glob(file.split('name')[0] + "pwm*")[0]
            logger.debug("pwm_file: " + pwm_file)

    if pwm_file == "":
        logger.error("Failed to get pwm file")
        return False

    logger.info("Please stop the fancontrol service before running this test "
                "and remember to restart the service after the test is complete."
                "\nTo perform this test, use the prompt below to reduce the fan speed, "
                "observe that the fan has slowed down, and then increase the fan speed.")

    logger.info("\nType Y to reduce fan speed:")
    while(1):
        var = input().strip().upper()
        if var == 'Y':
            logger.info("Reducing fan speed to " + str(int(fan_speed_slow/fan_speed_max*100)) + "%")
            logger.debug("Writing " + str(fan_speed_slow) + " to " + str(pwm_file))
            logger.info("The fan should now be spinning at a slower speed")
            with open(pwm_file, "w") as pf:
                pf.write(str(fan_speed_slow))
            break
        else:
            logger.info("Invalid input, try again")

    logger.info("\nIs the fan spinning at a slower speed? [Y/N]")
    while(1):
        var = input().strip().upper()
        if var == 'Y':
            logger.info("Setting fan back to max speed")
            logger.debug("Writing " + str(fan_speed_max) + " to " + str(pwm_file))
            with open(pwm_file, "w") as pf:
                pf.write(str(fan_speed_max))
            break
        elif var == 'N':
            with open(pwm_file, "w") as pf:
                pf.write(str(fan_speed_max))
            return False
        else:
            logger.info("Invalid input, try again")

    logger.info("\nIs the fan spinning at full speed? [Y/N]")
    while(1):
        var = input().strip().upper()
        if var == 'Y':
            return True
        elif var == 'N':
            return False
        else:
            logger.info("Invalid input, try again")
