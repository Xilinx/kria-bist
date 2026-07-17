# Kria Board Interface Test Application

## Setup

The recommended way to run the BIST application is from the prebuilt Docker
image for your platform. Pull the image that matches your OS release and
follow its documentation:

| Platform      | Docker image                   | Release tag | Documentation |
|---------------|--------------------------------|-------------|---------------|
| Ubuntu 24.04  | `xilinx/kria-bist:1.2-noble-24.04` | v1.2        | [BIST v1.2 docs](https://xilinx.github.io/kria-apps-docs/kr260/bist/1_2/build/html/docs/overview.html) |
| AMD EDF 26.06 | `xilinx/kria-bist:1.3-edf-26.06` | v1.3      | [BIST v1.3 docs](https://xilinx.github.io/kria-apps-docs/kr260/bist/1_3/build/html/docs/overview.html) |

## Building the Container

The BIST container for the AMD EDF image is built with Yocto/BitBake:

1. Set up an AMD EDF build environment by following the
   [Yocto Project build setup instructions for EDF](https://edf.docs.amd.com/en/latest/osdev/operating-system-integration-and-development.html#yocto-project-build-setup-instructions-for-edf).

2. Add the
   [meta-kria-apps](https://github.com/AMD-AECG-SSW-PUBLIC/meta-kria-apps)
   layer, which provides the BIST container recipe
   ([recipes-containers/container-kria-bist/container-kria-bist.bb](https://github.com/AMD-AECG-SSW-PUBLIC/meta-kria-apps/blob/main/recipes-containers/container-kria-bist/container-kria-bist.bb)):
   ```
   bitbake-layers add-layer /path/to/meta-kria-apps
   ```

3. Build the container image:
   ```
   MACHINE=amd-cortexa53-mali-common bitbake container-kria-bist
   ```

   The resulting OCI image is written under
   `tmp/deploy/images/${MACHINE}/`.

## How to Run

See [Setting up the Board and Application Deployment](docs/src/run.md) for
the full container setup, firmware install, and run instructions.

## Examples

The following are example pytest commands, run from inside the BIST
container.

To collect tests:
```
pytest --board kr260 --collect-only
```

To run tests:
```
pytest --board kr260
```

To run gpio tests only, use the -m option:
```
pytest --board kr260 -m gpio
```

To run an individual test, use the -k option:
```
pytest --board kr260 -k pmod1
```

## License

Copyright (C) 2022, Advanced Micro Devices, Inc.\
SPDX-License-Identifier: MIT
