# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {'label': 'tpm2_getcap'},
        {'label': 'tpm2_selftest'},
        {'label': 'tpm2_getrandom'},
        {'label': 'tpm2_hash'},
        {'label': 'tpm2_pcrread'},
        {'label': 'tpm2_pcrextend'},
        {'label': 'tpm2_pcrreset'}
    ]
}

supported_boards['kr260'] = supported_boards['kv260']
supported_boards['kd240'] = supported_boards['kv260']
