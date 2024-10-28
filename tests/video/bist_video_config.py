# Copyright (C) 2023 Advanced Micro Devices, Inc.
# SPDX-License-Identifier: MIT

supported_boards = {
    'kv260': [
        {'label': 'ar1335_ap1302_ximagesink', 'pipeline': 'isp_vcap_csi', 'width': 640, 'height': 480, 'fps': 30, 'fmt': 'NV12', 'tpg_pattern': 'Color Bars'},
        {'label': 'ar1335_ap1302_perf', 'pipeline': 'isp_vcap_csi', 'width': 3840, 'height': 2160, 'fps': 30, 'fmt': 'NV12'},
        {'label': 'tpg_ap1302_ximagesink', 'pipeline': 'isp_vcap_csi', 'width': 640, 'height': 480, 'fps': 30, 'fmt': 'NV12', 'tpg_pattern': '100% Color Bars'},
        {'label': 'tpg_ap1302_perf', 'pipeline': 'isp_vcap_csi', 'width': 3840, 'height': 2160, 'fps': 30, 'fmt': 'NV12'},
        {'label': 'imx219_filesink', 'pipeline': 'imx_vcap_csi', 'width': 1920, 'height': 1080, 'fps': 30, 'fmt': 'NV12', 'tpg_pattern': 'Color Bars'},
        {'label': 'imx219_perf', 'pipeline': 'imx_vcap_csi', 'width': 1920, 'height': 1080, 'fps': 30, 'fmt': 'NV12'},
        {'label': 'ar1335_filesink', 'pipeline': 'ias_vcap_csi', 'width': 3840, 'height': 2160, 'fps': 30, 'fmt': 'NV12', 'tpg_pattern': '100% Color Bar'},
        {'label': 'ar1335_perf', 'pipeline': 'ias_vcap_csi', 'width': 3840, 'height': 2160, 'fps': 30, 'fmt': 'NV12'},
    ],
    'kr260' : [
        {'label': 'imx547_filesink', 'pipeline': 'isp_v_proc', 'width': 1920, 'height': 1080, 'fps': 60, 'fmt': 'GRAY8', 'tpg_pattern': 'Gradiation Pattern'},
        {'label': 'imx547_perf', 'pipeline': 'isp_v_proc', 'width': 1920, 'height': 1080, 'fps': 60, 'fmt': 'GRAY8'},
    ],
}
