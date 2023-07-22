# BIST EEPROM Test Module

## Overview

The EEPROM module tests the EEPROM on the SOM and the carrier card by reading
its contents and verifying the data that is read.

## Tests

There are two tests for each board, one for the SOM and one for the carrier
card. Both tests are self-validating functional tests. The tests use the
ipmi-fru utility to read FRU data from a given file and print it to the
terminal. The "FRU Board Product Name" field is used to check if the expected
value is read and determine if a test passed or failed.

The config parameters for each test are described below:

* label: The test label
* eeprom_addr: The EEPROM address (used to differentiate SOM vs carrier card)
* field: The FRU field used to validate the read data
* value: The expected value that should be in the FRU field

## Test Execution

Example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m eeprom		// Run all tests in this module
pytest-3 --board kv260 -k som_eeprom		// Run som_eeprom test
pytest-3 --board kv260 -k carrier_card_eeprom	// Run carrier_card_eeprom test
```

These tests will print out all the FRU Data and each test will pass if the
"FRU Board Product Name" contains the value in the test config.

## Test Debug

* If one of the EEPROM tests fail, the FRU data can be verified manually using
  ipmi-fru.

## Known Issues and Limitations

* The EEPROM tests are limited to verifying a value in the "FRU Board Product
  Name" field.
* There is known issue for some EEPROM records which results in a multirecord
  area checksum error. If this is observed, the EEPROM output should be
  verified manually.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
