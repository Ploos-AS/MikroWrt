# M1.2 — Mango build candidate

This is a **candidate** OpenWrt-derived Mango build recipe. No hardware validation or firmware release is implied.

## Candidate target

- SoC family: MediaTek MT76x8 / ramips
- Candidate OpenWrt device config: `CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y`
- Validate the exact device definition against the selected upstream checkout.

## Steps

```sh
sh scripts/bootstrap-openwrt.sh
sh scripts/select-mango.sh
cd upstream/openwrt
make defconfig
grep '^CONFIG_TARGET_.*=y' .config
cd ../..
sh scripts/build-firmware.sh
```

The selector refuses to overwrite an existing `.config` and checks for the device token in upstream image definitions. This is only a sanity check, not a full compatibility guarantee.

The build currently uses OpenWrt's default package selection, not a MikroWrt-minimized package set. A dedicated minimal package configuration and verified baseline commit are still required.

## Safety

No flashing is performed. Factory and sysupgrade image formats are not interchangeable. Verify board revision, image metadata, partition map, recovery method and checksums before attempting hardware installation. Record firmware size and runtime measurements from real hardware.
