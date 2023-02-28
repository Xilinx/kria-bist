# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

import iio

def iio_get_channel(device_name, channel_name, logger):
    local_context = iio.Context("local:")
    for dev in local_context.devices:
        # Find device
        if dev.name == device_name:
            for channel in dev.channels:
                # Find channel
                if channel.id == channel_name:
                    return channel
            logger.error(channel_name + " channel not found")
            return None
    logger.error(device_name + " device not found")
    return None

def run_ina260_current_test(label, device_name, channel_name, min_current, max_current, helpers):
    logger = helpers.logger_init(label)
    logger.start_test()

    channel = iio_get_channel(device_name, channel_name, logger)
    if channel is None:
        logger.test_failed()
        logger.stop_test()
        return False
    raw = float(channel.attrs["raw"].value)
    scale = float(channel.attrs["scale"].value)
    current = raw * scale

    # Check if current is within range
    if current >= min_current and current <= max_current:
        logger.info("The current is " + str(current) + " mA, which is within the range of " + str(min_current) + " to " + str(max_current) + ".")
        logger.test_passed()
        logger.stop_test()
        return True
    else:
        logger.info("The current is " + str(current) + " mA, which is outside the range of " + str(min_current) + " to " + str(max_current) + ".")
        logger.test_failed()
        logger.stop_test()
        return False
