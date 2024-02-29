 # Known Issues

* RS485 over PS uart on KD240 does not function in Ubuntu 22.04 kd05 release as the driver is in the process of being upstreamed. Thus, TTY test is expected to fail in Ubuntu 22.04 kd05 image on KD240. (It expect to pass in the Ubuntu 22.04 kd03 version on KD240, and does not impact RS485 over AXI lite uart on KR260)

* Currently, the AR1335 module does not auto-load after loading kv260-bist firmware
binaries. A near term solution is to dynamically modprobe module with an additional
command.

* Kernel traces are seen while dynamically loading `kv260-bist` firmware binaries
on the second attempt after unloading the app after the first load.

***Note***: To get the BIST app working, press the on board 'SW2,'button which is 'RESET.'
```bash
ubuntu@kria:~$ sudo xmutil unloadapp
[sudo] password for ubuntu:
remove from slot 0 returns: 0 (Ok)
ubuntu@kria:~$ sudo xmutil loadapp kv260-bist
[   76.917224] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/firmware-name
[   76.927666] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/resets
kv260-bist: loaded to slot 0
ubuntu@kria:~$ [   77.996752] debugfs: Directory '4-003c' with parent 'regmap' already present!
ubuntu@kria:~$ sudo modprobe ar1335
ubuntu@kria:~$ sudo xmutil unloadapp
[   88.101605] OF: ERROR: memory leak, expected refcount 1 instead of 2, of_node_get()/of_node_put() unbalanced - destroy cset entry: attach overlay node /axi/scaler@b0040000/ports
[   88.119985] OF: ERROR: memory leak, expected refcount 1 instead of 2, of_node_get()/of_node_put() unbalanced - destroy cset entry: attach overlay node /axi/v_demosaic@b0000000/ports
[   88.136745] OF: ERROR: memory leak, expected refcount 1 instead of 2, of_node_get()/of_node_put() unbalanced - destroy cset entry: attach overlay node /axi/scaler@b0080000/ports
[   88.157751] OF: ERROR: memory leak, expected refcount 1 instead of 2, of_node_get()/of_node_put() unbalanced - destroy cset entry: attach overlay node /axi/v_demosaic@b0030000/ports
[   88.174264] OF: ERROR: memory leak, expected refcount 1 instead of 2, of_node_get()/of_node_put() unbalanced - destroy cset entry: attach overlay node /axi/i2c@80030000/i2c-mux@74/i2c@0/isp@3c/ports/port@0/endpoint
[   88.193558] OF: ERROR: memory leak, expected refcount 1 instead of 2, of_node_get()/of_node_put() unbalanced - destroy cset entry: attach overlay node /axi/i2c@80030000/i2c-mux@74/i2c@0/isp@3c/sensors/sensor@0
remove from slot 0 returns: 0 (Ok)
ubuntu@kria:~$ sudo xmutil loadapp kv260-bist
[   94.308089] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/firmware-name
[   94.318211] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/resets
[   94.497236] debugfs: Directory '4-003c' with parent 'regmap' already present!
[   94.601130] Unable to handle kernel access to user memory outside uaccess routines at virtual address 0000000000000000
[   94.611930] Mem abort info:
[   94.614773]   ESR = 0x0000000096000004
[   94.618555]   EC = 0x25: DABT (current EL), IL = 32 bits
[   94.623923]   SET = 0, FnV = 0
[   94.627004]   EA = 0, S1PTW = 0
[   94.630200]   FSC = 0x04: level 0 translation fault
[   94.635134] Data abort info:
[   94.638111]   ISV = 0, ISS = 0x00000004
[   94.642015]   CM = 0, WnR = 0
[   94.645000] user pgtable: 4k pages, 48-bit VAs, pgdp=0000000802953000
[   94.651509] [0000000000000000] pgd=0000000000000000, p4d=0000000000000000
[   94.658389] Internal error: Oops: 96000004 [#1] SMP
[   94.663269] Modules linked in: ar1335 al5e al5d ap1302 allegro i2c_mux_pca954x xlnx_vcu xt_conntrack nft_chain_nat xt_MASQUERADE nf_nat nf_conntrack_netlink nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nft_counter xt_addrtype nft_compat nf_tables nfnetlink br_netfilter bridge binfmt_misc joydev input_leds ina260_adc tpm_tis_spi mali uio_pdrv_genirq dm_multipath sch_fq_codel scsi_dh_rdac scsi_dh_emc scsi_dh_alua usb5744 dmaproxy ramoops reed_solomon pstore_blk pstore_zone efi_pstore ip_tables x_tables autofs4 raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx raid1 raid0 multipath linear hid_logitech_hidpp da9121_regulator hid_logitech_dj rtc_zynqmp spi_zynqmp_gqspi i2c_cadence zynqmp_dpsub crct10dif_ce usbhid aes_neon_bs aes_neon_blk crypto_simd cryptd
[   94.731858] CPU: 0 PID: 2561 Comm: sh Not tainted 5.15.0-1022-xilinx-zynqmp #26-Ubuntu
[   94.739764] Hardware name: ZynqMP SMK-K26 Rev1/B/A (DT)
[   94.744973] pstate: 00400005 (nzcv daif +PAN -UAO -TCO -DIT -SSBS BTYPE=--)
[   94.751924] pc : match_fwnode+0x38/0x14c
[   94.755848] lr : v4l2_async_find_match+0x98/0xc4
[   94.760457] sp : ffff8000146535a0
[   94.763755] x29: ffff8000146535a0 x28: ffff000802843f00 x27: 0000000000000000
[   94.770882] x26: ffff80000b522db0 x25: ffff00080c1c8bb8 x24: ffff80000905a640
[   94.778008] x23: ffff00080ebef080 x22: ffff00080c1c8b98 x21: ffff00080c1c8bc8
[   94.785134] x20: ffff00080ebef080 x19: ffff00080481ce00 x18: ffffffffffffffff
[   94.792260] x17: 0000000000000000 x16: 0000000000000000 x15: ffffffffffffffff
[   94.799387] x14: ffffff0000000000 x13: ffffffffffffffff x12: ffff800009cd6dc8
[   94.806513] x11: ffff80000b1adad0 x10: 0000000000000b60 x9 : ffff80000905a3c8
[   94.813639] x8 : ffff000802d91c10 x7 : ffff80000b509c10 x6 : 0000000000000001
[   94.820766] x5 : 0000000000000001 x4 : ffff00080481c880 x3 : ffff80000905a4f4
[   94.827892] x2 : ffff000809b35418 x1 : ffff00080ebef080 x0 : 0000000000000000
[   94.835019] Call trace:
[   94.837450]  match_fwnode+0x38/0x14c
[   94.841017]  v4l2_async_find_match+0x98/0xc4
[   94.845279]  v4l2_async_notifier_try_all_subdevs+0x80/0xd0
[   94.850756]  __v4l2_async_notifier_register+0xdc/0x150
[   94.855886]  v4l2_async_notifier_register+0x4c/0x74
[   94.860755]  xvip_composite_probe+0x19c/0x334
[   94.865104]  platform_probe+0x70/0xec
[   94.868758]  really_probe+0xc4/0x470
[   94.872326]  __driver_probe_device+0x11c/0x190
[   94.876761]  driver_probe_device+0x48/0x130
[   94.880936]  __device_attach_driver+0xc4/0x160
[   94.885372]  bus_for_each_drv+0x80/0xe0
[   94.889200]  __device_attach+0xb0/0x1ec
[   94.893028]  device_initial_probe+0x1c/0x30
[   94.897203]  bus_probe_device+0xa4/0xb0
[   94.901030]  device_add+0x40c/0x7a0
[   94.904511]  of_device_add+0x4c/0x70
[   94.908079]  of_platform_device_create_pdata+0xa0/0x130
[   94.913296]  of_platform_notify+0xe8/0x17c
[   94.917384]  blocking_notifier_call_chain+0x74/0xac
[   94.922253]  __of_changeset_entry_notify+0xf0/0x170
[   94.927123]  __of_changeset_apply_notify+0x50/0xdc
[   94.931906]  of_overlay_apply+0x1ac/0x2c0
[   94.935907]  of_overlay_fdt_apply+0xac/0x124
[   94.940169]  cfs_overlay_item_path_store+0xd4/0x1a0
[   94.945039]  configfs_write_iter+0xcc/0x130
[   94.949214]  new_sync_write+0xf0/0x18c
[   94.952955]  vfs_write+0x22c/0x2cc
[   94.956349]  ksys_write+0x70/0x100
[   94.959743]  __arm64_sys_write+0x24/0x30
[   94.963657]  invoke_syscall+0x78/0x100
[   94.967398]  el0_svc_common.constprop.0+0x54/0x184
[   94.972181]  do_el0_svc+0x30/0xac
[   94.975488]  el0_svc+0x28/0xb0
[   94.978535]  el0t_64_sync_handler+0xa4/0x130
[   94.982797]  el0t_64_sync+0x1a4/0x1a8
[   94.986457] Code: f9408420 eb02001f 54000560 aa0103f4 (f9400001)
[   94.992538] ---[ end trace ef36477bd2b0a936 ]---
kv260-bist: loaded to slot 0
ubuntu@kria:~$
```
