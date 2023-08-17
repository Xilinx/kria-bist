# BIST Motor Test Module

## Overview

The Motor test module verifies the functionality of KD240 starter kit.

## Tests

The module contains seven self-validating functional tests. It uses py_foc_motor_ctrl
library to create motor control instance for calling member functions such as getSpeed(),
setOperationMode(), etc.

1. run_qei_gate_drive_test() - In this test, QEI interface and motor gate drive is
   validated. The motor is spun in 'Speed' mode with rpm set to 1000 and the set speed is
   then compared with average of 10 measured motor speed readings obtained by getSpeed()
   motor control function. The measured motor speed is expected to be within the error
   margin of 20% of the set speed to pass the test.

   The config parameters for the test are described below:

    * label: The test label
    * speed: Motor speed to be set

2. run_motor_vlt_adc_fb_modeoff_test() - In this test, the ADC voltages are validated to
   read back near 0V when the motor is in 'Off' mode. The ADC voltage feedback values of
   channels PhaseA, PhaseB and PhaseC are measured using getVoltage() motor control function
   and verified to be below predefined threshold value of 1V to pass the test.
  
   The config parameter for the test is described below:

    * label: The test label
  
3. run_motor_vlt_adc_fb_modespeed_test() - In this test, the ADC voltages are validated to
   read back the volatge values in the predefined range in 'Speed' mode with rpm set to 1000.
   The ADC voltage feedback values of channels PhaseA, PhaseB and PhaseC are measured using
   getVoltage() motor control function. The measured voltages are averaged out of 100 samples
   of readings and verified to be in the range of 8V - 15V for each channel to pass the test.
   
   The config parameters for the test are described below:

    * label: The test label
    * speed: Motor speed to be set

4. run_motor_curr_adc_fb_modeoff_test() - In this test, the ADC currents are validated to
   read back near 0A when the motor is in 'Off' mode. The ADC current feedback values of
   channels PhaseA, PhaseB and PhaseC are measured using getCurrent() motor control function.
   The measured currents are averaged out of 100 samples of readings for each channel and
   verified to be below predefined threshold value of 0.05A for the test to pass.
   
   The config parameter for the test is described below:

    * label: The test label
    
5. run_motor_curr_adc_fb_modespeed_test() - In this test, the ADC currents are validated to
   read back the current values in the predefined range in 'Speed' mode with rpm set to 1000.
   The ADC current feedback values of channels PhaseA, PhaseB and PhaseC are measured using
   getCurrent() motor control function. The measured currents are averaged out of 100 samples
   of readings for each channel and verified to be in the range of 0.01A - 0.5A for the test
   to pass.
   
   The config parameters for the test are described below:

    * label: The test label
    * speed: Motor speed to be set

6. run_motor_dc_link_volt_adc_fb_test() - In this test, the DC link voltage is validated to be
   near 24V when the power supply is plugged in motor 'Off' mode. The DC link voltage is measured
   using getVoltage() motor control function. The measured voltageis averaged out of 10 samples
   of readings and verified to be in the range of 23.5V - 24.5V for the test to pass.

   The config parameter for the test is described below:

    * label: The test label
    
7. run_motor_dc_link_curr_adc_fb_test() - In this test, the DC link current is validated to be
   near 0A in the 'Off' mode. The DC link voltage is measured using getVoltage() motor control
   function. The measured current is averaged out of 10 samples of readings and verified to be
   below predefined threshold value of 0.05A for the test to pass.

   The config parameter for the test is described below:

    * label: The test label

## Test Execution

Example commands for this module are provided below (KD240):

```bash
pytest-3 --board kd240 -m motor  // Run all tests in this module
pytest-3 --board kd240 -k qei_gate_drive_test  // Run QEI interface test in 'Speed' mode
pytest-3 --board kd240 -k volt_adc_fb_modeoff_test  // Run motor voltage ADC feedback test in 'Off' mode
pytest-3 --board kd240 -k volt_adc_fb_modespeed_test  // Run motor voltage ADC feedback test in 'Speed' mode
pytest-3 --board kd240 -k curr_adc_fb_modeoff_test  // Run motor current ADC feedback test in 'Off' mode
pytest-3 --board kd240 -k curr_adc_fb_modespeed_test  // Run motor current ADC feedback test in 'Speed' mode
pytest-3 --board kd240 -k dc_link_volt_adc_fb_test  // Run DC link voltage ADC feedback test in 'Off' mode
pytest-3 --board kd240 -k dc_link_curr_adc_fb_test  // Run DC link current ADC feedback test in 'Off' mode
```

The test prints out messages indicating motor mode and readings of the motor object for each test.
 
## Test Debug

* Make sure to load the BIST firmware before running the motor tests as motor hls_foc_periodic device
  is not detected otherwise.

## Known Issues and Limitations

* The motor test is limited to verifying the functionalities specified in the configuration file on loading
  the BIST firmware only.
* The established threshold values or ranges are based on the outputs observed during experimentation.
  The values might differ slightly from board to board.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
