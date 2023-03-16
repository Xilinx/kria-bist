# Kria Board Interface Test Application

## Setup
Install prerequisites
```
sudo apt install freeipmi-tools libiio python3-libiio tpm2-tools v4l-utils gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad libgstreamer1.0-0 gst-perf libdrm-tests
```
Install pytest, clone this repo, and cd into tests dir
```
sudo apt install python3-pytest
```
## Examples
To collect tests:
```
pytest-3 --board kr260 --collect-only
```

To run tests:
```
pytest-3 --board kr260
```

To run gpio tests only, use the -m option:
```
pytest-3 --board kr260 -m gpio
```

To run an individual test, use the -k option:
```
pytest-3 --board kr260 -k pmod1
```

## License

Copyright (C) 2022, Advanced Micro Devices, Inc.\
SPDX-License-Identifier: MIT
