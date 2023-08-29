# BIST TPM Test Module

## Overview

This test module verifies the features provided by the TPM hardware.

## Tests

The tests in this module use tpm2-tools to verify the output of various
functions. All tests are self-validating functional tests. Each entry in the
config contains the name of the command that is used for the test, and each
one has a separate function. The tests are described below.

* tpm2_getcap: Gets the list of capabilities and verifies that the list
  matches the expected list.
* tpm2_selftest: Runs a self test and verifies expected return code.
* tpm2_getrandom: Gets 10 random hash keys and checks if they are unique.
* tpm2_hash: Gets the hash of a fixed file and verifies it matches the
  expected hash.
* tpm2_pcrread: Reads PCR registers 0-16 and verifies that a value of 0 is
  read for both hash algorithms.
* tpm2_pcrextend: Extends PCR register 23 three times and verifies the has
  value changes each time.
* tpm2_pcrreset: Extends PCR register 23 then resets it and verifies the value
  is 0.

## Test Execution

The example commands for this module are provided below (KV260):

```bash
pytest-3 --board kv260 -m tpm			// Run all tests in this module
pytest-3 --board kv260 -k tpm2_getcap		// Run tpm2_getcap test
pytest-3 --board kv260 -k tpm2_hash		// Run tpm2_hash test
```

Each test prints out the log messages that include the command that is run by
the test function and the final test result. Some tests also log debug
level messages with additional information, which can be found in the automatically
generated log file.

## Test Debug

* If one of the tpm tests fails, the commands from the log prints can be run
  manually to verify the expected output.

## Known Issues and Limitations

* The tests in this module are limited to the predefined verification steps
  described above.

## Next Steps

1. [BIST Overview](../overview)


<p class="sphinxhide" align="center"><sub>Copyright © 2023 Advanced Micro Devices, Inc</sub></p>

<p class="sphinxhide" align="center"><sup><a href="https://www.amd.com/en/corporate/copyright">Terms and Conditions</a></sup></p>
