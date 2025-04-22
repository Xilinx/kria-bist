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


* On KV260 **Rev2** boards, the I2C test fails to detect the USB hub device `usb5744` at address `0x2d` on the `ps_i2c_bus_main` bus. This leads to a test failure in the I2C BIST test:

  ```
  i2c/test_bist_i2c.py::test_i2c[ps_i2c_bus_main]
  ---------------------------------------------------------------------------------- live log call -------------------------------------------------------------------
  ------------------------------------------
  Start of test
  Device 'usb5744' could not be detected on i2c-1 bus at expected device address 0x2d
  Test failed
  End of test
  FAILED
  i2c/test_bist_i2c.py::test_i2c[axi_i2c_bus_main]
  ============================================================================= short test summary info ==============================================================
  FAILED i2c/test_bist_i2c.py::test_i2c[ps_i2c_bus_main] - assert False
  ```

* For `kr260-bist` firmware a synchronous abort kernel trace is observed sometimes(not always) which is a known issue because of the XXV IP error.
Workaround is to reboot/power cycle the target KR260 to get rid of it and start fresh.

  ```
  ubuntu@kria:~$ [  282.930884] Internal error: synchronous external abort: 0000000096000210 [#1] SMP
  [  282.938396] Modules linked in: xt_conntrack xt_MASQUERADE bridge xt_set ip_set nft_chain_nat nf_nat nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 xt_addrtype nft_compat nf_tables qrtr binfmt_misc tee zynqmp_edac ina260_adc mali sch_fq_codel dm_multipath efi_pstore nfnetlink ip_tables x_tables autofs4 raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx raid1 raid0 i2c_mux_pca954x da9121_regulator crct10dif_ce polyval_ce polyval_generic rtc_zynqmp spi_zynqmp_gqspi i2c_cadence uio_pdrv_genirq aes_neon_bs aes_neon_blk aes_ce_blk aes_ce_cipher
  [  282.987940] CPU: 0 PID: 541 Comm: kworker/u8:5 Not tainted 6.8.0-1013-xilinx #14-Ubuntu
  [  282.995949] Hardware name: ZynqMP KR260 revA (DT)
  [  283.000646] Workqueue: events_power_efficient phylink_resolve
  [  283.006409] pstate: 60400005 (nZCv daif +PAN -UAO -TCO -DIT -SSBS BTYPE=--)
  [  283.013370] pc : axienet_pcs_get_state+0x454/0x518
  [  283.018161] lr : axienet_pcs_get_state+0x454/0x518
  [  283.022952] sp : ffff8000846fbcb0
  [  283.026259] x29: ffff8000846fbcb0 x28: 0000000000000000 x27: 00000041dedfbe6f
  [  283.033403] x26: ffff80008123434c x25: ffff80008123434c x24: 0000000000000000
  [  283.040547] x23: ffff8000811c69a4 x22: ffff800084bc040c x21: ffff8000811c69a4
  [  283.047690] x20: ffff8000846fbd30 x19: ffff000800fe79e0 x18: ffff800084395030
  [  283.054834] x17: 0000000000000000 x16: 0000000000000000 x15: 0000000000000000
  [  283.061978] x14: ffffffffffffffff x13: 0000000000000000 x12: 0101010101010101
  [  283.069122] x11: 0000000000000000 x10: 0000000000001b80 x9 : ffff800081ae1a3c
  [  283.076265] x8 : ffff0008095d9be0 x7 : 0000000000000000 x6 : 0000000000000000
  [  283.083409] x5 : 0000000000000000 x4 : 0000000000000000 x3 : 0000000000000000
  [  283.090553] x2 : 0000000000000000 x1 : 0000000000000000 x0 : 0000000000000000
  [  283.097697] Call trace:
  [  283.100137]  axienet_pcs_get_state+0x454/0x518
  [  283.104580]  phylink_mac_pcs_get_state+0x84/0x118
  [  283.109285]  phylink_resolve+0x290/0x370
  [  283.113208]  process_one_work+0x170/0x3f8
  [  283.117218]  worker_thread+0x354/0x478
  [  283.120968]  kthread+0xf8/0x110
  [  283.124110]  ret_from_fork+0x10/0x20
  [  283.127690] Code: aa1e03e3 aa1603e1 52800400 97e57332 (b94002d8)
  [  283.133784] ---[ end trace 0000000000000000 ]---
  ```
