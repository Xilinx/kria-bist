# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution

import py_foc_motor_ctrl as mcontrol
import time


def get_average(mc, iterations, motor_object, logger, iio_channel=None):
    """
    Get average of measured motor object

    Args:
            mc: MotorControl instance
            iterations: Number of iterations for the object measurement
            motor_object: Motor object (Speed, Voltage, Current)

            logger: Calling function's logger object
            iio_channel: IIO channel

    Returns:
            float: Average of measured readings
    """
    # Take average of the iterations of measured motor object
    motor_object_sum = 0
    for iteration in range(iterations):
        if motor_object == "Voltage":
            motor_measurement = mc.getVoltage(iio_channel)
        elif motor_object == "Current":
            motor_measurement = mc.getCurrent(iio_channel)
        elif motor_object == "Speed":
            motor_measurement = mc.getSpeed()
        motor_object_sum = motor_object_sum + abs(motor_measurement)
        logger.debug(f"Measured motor object at iteration {iteration}: {round(motor_measurement, 2)}")
        time.sleep(0.001)  # Allow 1ms delay to observe changes in motor readings
        iteration += 1
    average = motor_object_sum / iterations
    return float(average)


def run_qei_gate_drive_test(label, speed, helpers):
    """
    QEI and gate drive test for motor control and performance evaluation

    Args:
            label: Test label
            speed: Motor speed to be set
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)

    # Run dependency test
    test_result = run_motor_dc_link_volt_adc_fb_test(label, helpers)
    if test_result:
        logger.info("DC Link Voltage Test Passed")
    else:
        logger.error("DC Link Voltage Test Failed")
        return False

    logger.start_test()
    # Initialize speed parameters
    speed_lower_limit = speed * 0.80
    logger.debug(f"Motor speed lower limit: {speed_lower_limit}")
    speed_upper_limit = speed * 1.20
    logger.debug(f"Motor speed upper limit: {speed_upper_limit}")
    # Iterations for taking average of motor speed measurement
    iterations = 10
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    # Set motor speed
    mc.setSpeed(speed)
    logger.info(f"Motor speed: {speed}")
    # Set the mode = Speed to spin the motor
    mc.setOperationMode(mcontrol.MotorOpMode.kModeSpeed)
    time.sleep(2)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeSpeed':
        logger.error("Error setting the motor mode: Speed")
        mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
        motor_offmode = mc.getOperationMode()
        logger.info(f"Operation Mode: {motor_offmode}")
        return False
    logger.info(f"Operation Mode: {op_mode}")

    logger.info(f"Measuring motor speed...")
    motor_speed_avg = get_average(mc, iterations, "Speed", logger)
    logger.info(f"Average measured motor speed: {round(motor_speed_avg, 2)}")
    if (motor_speed_avg < speed_lower_limit) or (motor_speed_avg > speed_upper_limit):
        logger.error("Measured motor speed is not within the error margin of set speed")
        mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
        motor_offmode = mc.getOperationMode()
        logger.info(f"Operation Mode: {motor_offmode}")
        return False
    logger.info("Motor control QEI gate drive test successful")
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    motor_offmode = mc.getOperationMode()
    logger.info(f"Operation Mode: {motor_offmode}")
    return True


def run_motor_vlt_adc_fb_modeoff_test(label, helpers):
    """
    Motor Voltage ADC feedback test on IIO channels for mode: Off

    Args:
            label: Test label
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Initialize voltage parameters
    voltage_fb_upper_limit = 1
    logger.debug(f"Motor voltage ADC feedback upper limit: {voltage_fb_upper_limit}V")
    voltage_fb_in_range = True
    # Iterations for taking average of adc motor voltage feedback measurement
    iterations = 10
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    iio_voltage_channel = [mcontrol.ElectricalData.kPhaseA, mcontrol.ElectricalData.kPhaseB,
                           mcontrol.ElectricalData.kPhaseC]
    time.sleep(1)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeOff':
        logger.error("Error setting the motor mode: Off")
        return False
    logger.info(f"Operation Mode: {op_mode}")

    for channel in iio_voltage_channel:
        logger.info(f"Measuring motor ADC voltage feedback for {channel}...")
        voltage_adc_fb_avg = get_average(mc, iterations, "Voltage" , logger, channel)
        logger.info(f"Average measured motor voltage: {round(voltage_adc_fb_avg, 2)}V")
        if voltage_adc_fb_avg > voltage_fb_upper_limit:
            logger.error(f"Measured motor voltage feedback for {channel} is not within the expected range")
            voltage_fb_in_range = False
    if not voltage_fb_in_range:
        return False
    logger.info("Motor voltage ADC feedback test successful in 'OFF' mode")
    return True


def run_motor_vlt_adc_fb_modeopenloop_test(label, speed, helpers):
    """
    Motor Voltage ADC feedback test on IIO channels for mode: Speed

    Args:
            label: Test label
            speed: Motor speed to be set
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)

    # Run dependency test
    test_result = run_qei_gate_drive_test(label, speed, helpers)
    if test_result:
        logger.info("QEI Gate Drive Test Passed")
    else:
        logger.error("QEI Gate Drive Test Failed")
        return False

    logger.start_test()
    # Initialize parameters
    voltage_fb_lower_limit = 8
    logger.debug(f"Motor voltage ADC feedback lower limit: {voltage_fb_lower_limit}V")
    voltage_fb_upper_limit = 15
    logger.debug(f"Motor voltage ADC feedback upper limit: {voltage_fb_upper_limit}V")
    voltage_fb_in_range = True
    # Iterations for taking average of motor voltage measurement
    iterations = 100
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    # Set the mode = Open loop
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOpenLoop)
    time.sleep(1)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeOpenLoop':
        logger.error("Error setting the motor mode: Open Loop")
        return False
    logger.info(f"Operation Mode: {op_mode}")
    iio_voltage_channel = [mcontrol.ElectricalData.kPhaseA, mcontrol.ElectricalData.kPhaseB,
                           mcontrol.ElectricalData.kPhaseC]

    for channel in iio_voltage_channel:
        logger.info(f"Measuring motor ADC voltage feedback for {channel}...")
        voltage_adc_fb_avg = get_average(mc, iterations, "Voltage" , logger, channel)
        logger.info(f"Average measured motor voltage: {round(voltage_adc_fb_avg, 2)}V")
        if (voltage_adc_fb_avg < voltage_fb_lower_limit) or (voltage_adc_fb_avg > voltage_fb_upper_limit):
            logger.error(f"Measured motor voltage feedback for {channel} is not within the expected range")
            voltage_fb_in_range = False
    if not voltage_fb_in_range:
        mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
        motor_offmode = mc.getOperationMode()
        logger.info(f"Operation Mode: {motor_offmode}")
        return False
    logger.info("Motor voltage ADC feedback test successful in 'Open Loop' mode")
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    motor_offmode = mc.getOperationMode()
    logger.info(f"Operation Mode: {motor_offmode}")
    return True


def run_motor_curr_adc_fb_modeoff_test(label, helpers):
    """
    Motor Current ADC feedback test on IIO channels for mode: Off

    Args:
            label: Test label
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Iterations for taking average of adc motor Current feedback measurement
    iterations = 10
    # Initialize parameters
    current_fb_lower_limit = 0.05
    logger.debug(f"Motor current ADC feedback lower limit: {current_fb_lower_limit}A")
    current_fb_in_range = True
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    iio_current_channel = [mcontrol.ElectricalData.kPhaseA, mcontrol.ElectricalData.kPhaseB,
                           mcontrol.ElectricalData.kPhaseC]
    time.sleep(1)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeOff':
        logger.error("Error setting the motor mode: Off")
        return False
    logger.info(f"Operation Mode: {op_mode}")

    for channel in iio_current_channel:
        logger.info(f"Measuring motor ADC current feedback for {channel}...")
        current_adc_fb_avg = get_average(mc, iterations, "Current" , logger, channel)
        logger.info(f"Average measured motor current: {round(current_adc_fb_avg, 2)}A")
        if current_adc_fb_avg > current_fb_lower_limit:
            logger.error(f"Measured motor current feedback for {channel} is not within the expected range")
            current_fb_in_range = False
    if not current_fb_in_range:
        return False
    logger.info("Motor current ADC feedback test successful in 'OFF' mode")
    return True


def run_motor_curr_adc_fb_modeopenloop_test(label, speed, helpers):
    """
    Motor Current ADC feedback test on IIO channels for mode: Speed

    Args:
            label: Test label
            speed: Motor speed to be set
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)

    # Run dependency test
    test_result = run_qei_gate_drive_test(label, speed, helpers)
    if test_result:
        logger.info("QEI Gate Drive Test Passed")
    else:
        logger.error("QEI Gate Drive Test Failed")
        return False

    logger.start_test()
    # Initialize parameters
    current_fb_lower_limit = 0.01
    logger.debug(f"Motor current ADC feedback lower limit: {current_fb_lower_limit}A")
    current_fb_upper_limit = 0.5
    logger.debug(f"Motor current ADC feedback upper limit: {current_fb_upper_limit}A")
    current_fb_in_range = True
    # Iterations for taking average of motor current measurement
    iterations = 100
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    # Set the mode = Open loop
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOpenLoop)
    time.sleep(1)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeOpenLoop':
        logger.error("Error setting the motor mode: Open Loop")
        return False
    logger.info(f"Operation Mode: {op_mode}")
    iio_current_channel = [mcontrol.ElectricalData.kPhaseA, mcontrol.ElectricalData.kPhaseB,
                           mcontrol.ElectricalData.kPhaseC]

    for channel in iio_current_channel:
        logger.info(f"Measuring motor ADC current feedback for {channel}...")
        current_adc_fb_avg = get_average(mc, iterations, "Current" , logger, channel)
        logger.info(f"Average measured motor current: {round(current_adc_fb_avg, 2)}A")
        if (current_adc_fb_avg < current_fb_lower_limit) or (current_adc_fb_avg > current_fb_upper_limit):
            logger.error(f"Measured motor current feedback for {channel} is not within the expected range")
            current_fb_in_range = False
    if not current_fb_in_range:
        mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
        motor_offmode = mc.getOperationMode()
        logger.info(f"Operation Mode: {motor_offmode}")
        return False
    logger.info("Motor current ADC feedback test successful in 'Open Loop' mode")
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    motor_offmode = mc.getOperationMode()
    logger.info(f"Operation Mode: {motor_offmode}")
    return True


def run_motor_dc_link_volt_adc_fb_test(label, helpers):
    """
    Motor Voltage DC link ADC feedback test for mode: Off

    Args:
            label: Test label
            helpers: Fixture for helper functions

    Returns:
            bool: True/False
    """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Iterations for taking average of adc motor Voltage feedback measurement
    iterations = 10
    # Initialize parameters
    voltage_fb_lower_limit = 22.8
    logger.debug(f"Motor voltage ADC feedback lower limit: {voltage_fb_lower_limit}V")
    voltage_fb_upper_limit = 25.2
    logger.debug(f"Motor voltage ADC feedback upper limit: {voltage_fb_upper_limit}V")
    dc_channel = mcontrol.ElectricalData.kDCLink
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    time.sleep(1)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeOff':
        logger.error("Error setting the motor mode: Off")
        return False
    logger.info(f"Operation Mode: {op_mode}")

    logger.info(f"Measuring motor ADC voltage feedback for {dc_channel}...")
    voltage_adc_fb_avg = get_average(mc, iterations, "Voltage" , logger, dc_channel)
    logger.info(f"Average measured motor voltage: {round(voltage_adc_fb_avg, 2)}V")
    if (voltage_adc_fb_avg < voltage_fb_lower_limit) or (voltage_adc_fb_avg > voltage_fb_upper_limit):
        logger.error(f"Measured motor voltage feedback for {dc_channel} is not within the expected range")
        return False
    logger.info("Motor voltage ADC feedback test successful in 'OFF' mode")
    return True


def run_motor_dc_link_curr_adc_fb_test(label, helpers):
    """
        Motor Current DC link ADC feedback test for mode: Off

        Args:
                label: Test label
                helpers: Fixture for helper functions

        Returns:
                bool: True/False
        """
    logger = helpers.logger_init(label)
    logger.start_test()
    # Iterations for taking average of adc motor Current feedback measurement
    iterations = 10
    # Initialize parameters
    current_fb_lower_limit = 0.6
    logger.debug(f"Motor current DC link ADC feedback lower limit: {current_fb_lower_limit}A")
    dc_channel = mcontrol.ElectricalData.kDCLink
    # Get a MotorControl instance with session ID 1 and default config path
    mc = mcontrol.MotorControl.getMotorControlInstance(1)
    if mc is None:
        logger.error("Unable to get MotorControl instance")
        return False
    # Use the MotorControl instance to call its member functions
    # Initialize the motor by setting mode = OFF
    mc.setOperationMode(mcontrol.MotorOpMode.kModeOff)
    time.sleep(1)  # Wait for the motor to stabilize
    op_mode = mc.getOperationMode()
    if str(op_mode) != 'MotorOpMode.kModeOff':
        logger.error("Error setting the motor mode: Off")
        return False
    logger.info(f"Operation Mode: {op_mode}")

    logger.info(f"Measuring motor ADC current feedback for {dc_channel}...")
    current_adc_fb_avg = get_average(mc, iterations, "Current" , logger, dc_channel)
    logger.info(f"Average measured motor current: {round(current_adc_fb_avg, 2)}A")
    if current_adc_fb_avg > current_fb_lower_limit:
        logger.error(f"Measured motor current feedback for {dc_channel} is not within the expected range")
        return False
    logger.info("Motor current ADC feedback test successful in 'OFF' mode")
    return True
