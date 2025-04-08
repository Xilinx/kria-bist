 # Known Issues

* For 24.04 release, ethernet_performance for DHCP address assignment and SFP+ test suite yields performance lower than
80% of the maximum bitrate. Due to this, Ethernet Performance tests for DHCP address assignment case and SFP+ are expected
to fail.

* An abrupt hang/system freeze is seen when dynamically loading `kr260-bist` firmware on the second attempt of loading.

  **NOTE** : Workaround is to reboot/power cycle and try loading it again on next boot.

  ```
  ubuntu@kria:~$ sudo xmutil loadapp kr260-bist
  [  173.585162] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-region/firmware-name
  [  173.595491] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-region/resets
  ```

* There is a known issue of system hang during the reload of the kd240-bist application. While the initial load and unload
process works correctly, subsequent attempts to load the application result in a system hang. To prevent this, it is
recommended to remove ADC_HUB and all the HLS modules before unloading the application firmware. This ensures that the next
reload of the application does not cause a hang.

  To remove the ADC_HUB and HLS modules before unloading the firmware, use the following commands:

  ```
  sudo rmmod $(lsmod | grep hls_ | awk '{print $1}') # Unloads all HLS modules
  sudo rmmod xilinx_adc_hub # Unloads ADC_HUB module
  sudo lsmod # Verify that HLS modules have been removed
  ```
  **NOTE** : Ensure that HLS and ADC_HUB modules are removed before `xmutil unloadapp` command.


* On KV260 Rev2 boards, the I2C test fails to detect the USB hub device `usb5477` at address `0x2d` on the `ps_i2c_bus_main` bus. This leads to a test failure in the I2C BIST test:

  ```
  i2c/test_bist_i2c.py::test_i2c[ps_i2c_bus_main]
  ---------------------------------------------------------------------------------- live log call -------------------------------------------------------------------
  ------------------------------------------
  Start of test
  Device 'usb5477' could not be detected on i2c-1 bus at expected device address 0x2d
  Test failed
  End of test
  FAILED
  i2c/test_bist_i2c.py::test_i2c[axi_i2c_bus_main]
  ============================================================================= short test summary info ==============================================================
  FAILED i2c/test_bist_i2c.py::test_i2c[ps_i2c_bus_main] - assert False
  ```
