# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

# Import the 'modules' that are required for test cases execution
import pytest
from bist_motor import *


@pytest.mark.motor
def test_motor(id, helpers):
    """
    Function to parse File System test configurations

    Args:
            id: List of configurations
            helpers: Handle for logging
    """
    # Parse the configurations
    label = id['label']
    
           
    if 'volt_adc_fb_modeoff_test' in label:
        test_result = run_motor_vlt_adc_fb_modeoff_test(label, helpers)
        
    elif 'curr_adc_fb_modeoff_test' in label:       
        test_result = run_motor_curr_adc_fb_modeoff_test(label, helpers)
        
    elif 'dc_link_volt_adc_fb_test' in label:
        test_result = run_motor_dc_link_volt_adc_fb_test(label, helpers)

    elif 'dc_link_curr_adc_fb_test' in label:
        test_result = run_motor_dc_link_curr_adc_fb_test(label, helpers)
    
    elif 'qei_gate_drive_test' in label: 
        speed = id['speed']       
        test_result = run_qei_gate_drive_test(label, speed, helpers)  
        
    elif 'volt_adc_fb_modespeed_test' in label: 
        speed = id['speed']       
        test_result = run_motor_vlt_adc_fb_modespeed_test(label, speed, helpers)
        
    elif 'curr_adc_fb_modespeed_test' in label: 
        speed = id['speed']       
        test_result = run_motor_curr_adc_fb_modespeed_test(label, speed, helpers)
        
    else:
        assert False
    
    logger = helpers.logger_init(label)
    if test_result:
        logger.test_passed()
        logger.stop_test()
    else:
        logger.test_failed()
        logger.stop_test()

    assert test_result
