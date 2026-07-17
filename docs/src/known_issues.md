 # Known Issues

* For EDF 26.06 release, ethernet_performance for DHCP address assignment and SFP+ test suite yields performance lower than
80% of the maximum bitrate. Due to this, Ethernet Performance tests for DHCP address assignment case and SFP+ are expected
to fail.

* For `kr260-bist` firmware a synchronous abort kernel trace is observed which is a known issue because of the XXV IP.

  ```
  amd-edf:~$ [  933.318691] Internal error: synchronous external abort: 0000000096000210 [#1]  SMP
  [  933.326284] Modules linked in: xt_conntrack xt_MASQUERADE iptable_nat nf_nat xt_addrtype iptable_filter ip_tables cfg80211 mali(O) dmaproxy(O)
  [  933.339102] CPU: 2 UID: 0 PID: 72 Comm: kworker/2:2 Tainted: G   M       O        6.18.10-xilinx-gfb979987d554 #1 NONE
  [  933.349888] Tainted: [M]=MACHINE_CHECK, [O]=OOT_MODULE
  [  933.355022] Hardware name: xlnx ZynqMP KR260 revB/ZynqMP KR260 revB, BIOS 2026.01 01/01/2026
  [  933.363453] Workqueue: events_power_efficient phylink_resolve
  [  933.369206] pstate: 60000005 (nZCv daif -PAN -UAO -TCO -DIT -SSBS BTYPE=--)
  [  933.376167] pc : axienet_pcs_get_state+0x2b8/0x3ac
  [  933.380958] lr : axienet_pcs_get_state+0x2b0/0x3ac
  [  933.385749] sp : ffff80008094bcb0
  [  933.389055] x29: ffff80008094bcb0 x28: ffff000801457d80 x27: ffff00087f6fce98
  [  933.396193] x26: ffff000801457dc0 x25: 0000000000000000 x24: ffff00080548e8e0
  [  933.403327] x23: ffff00080548e900 x22: 0000000000000000 x21: 000000d94d9cde33
  [  933.410462] x20: ffff80008094bd00 x19: ffff000805b81a00 x18: 0000000000000000
  [  933.417597] x17: ffff800080c03c48 x16: 0000000000000000 x15: 0000000000000000
  [  933.424732] x14: ffff00080034c380 x13: 000026b9ef14f45c x12: 0000000000000307
  [  933.431868] x11: 00000000000000c0 x10: 00000000000009e0 x9 : ffff80008094bb10
  [  933.439004] x8 : ffff00080034cd40 x7 : 0000000000000001 x6 : 00000002f9ae6994
  [  933.446147] x5 : ffff00087f6fd540 x4 : 0000000000000002 x3 : 000000000006317a
  [  933.453282] x2 : 0028496afad1c6f9 x1 : ffff8000819d040c x0 : 000000d94d956ff4
  [  933.460417] Call trace:
  [  933.462855]  axienet_pcs_get_state+0x2b8/0x3ac (P)
  [  933.467647]  phylink_mac_pcs_get_state+0x7c/0xb0
  [  933.472264]  phylink_resolve+0x53c/0x608
  [  933.476188]  process_one_work+0x144/0x380
  [  933.480198]  worker_thread+0x27c/0x464
  [  933.483947]  kthread+0x114/0x1cc
  [  933.487176]  ret_from_fork+0x10/0x20
  [  933.490756] Code: d503203f 97d43fab f9407261 91103021 (b9400021)
  [  933.496851] ---[ end trace 0000000000000000 ]---

  Message from syslogd@amd-edf at Fri May 15 19:02:21 2026 ...
  kernel: Internal error: synchronous external abort: 0000000096000210 [#1]  SMP

  Message from syslogd@amd-edf at Fri May 15 19:02:21 2026 ...
  kernel: Code: d503203f 97d43fab f9407261 91103021 (b9400021)
  ```

  The reason being, when the link is not connected, the clock becomes unstable, and the block lock register of the XXV IP becomes inaccessible and results in a crash. [Solution/Workaround](https://adaptivesupport.amd.com/s/article/000037700?language=en_US)

* On 26.1 EDF images, a kernel call trace related to the AXI Ethernet driver is observed in dmesg when the BIST overlay is unloaded (dfx-mgr-client -unload <id>). This has been observed on KV260, KR260, and KD240 boards. Although the call trace is reported, it does not impact the execution or functionality of the BIST application.

* During Kria BIST execution, a DeprecationWarning related to the deprecated pkg_resources API may be displayed in the test output. This warning does not affect test execution or the validity of the test results and can be safely ignored.

 ```
 ================================================================================================ warnings summary =================================================================================================
 ../../../../usr/lib/python3.12/site-packages/can/io/logger.py:13
  /usr/lib/python3.12/site-packages/can/io/logger.py:13: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
    from pkg_resources import iter_entry_points

 -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
 ```
