# M1.3 — Mango minimal profile and image inventory

This is an **unqualified candidate** OpenWrt-derived Mango build recipe. No hardware validation or firmware release is implied.

## Candidate target

- SoC family: MediaTek MT76x8 / ramips
- Candidate device config: `CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y`
- Verify device definition in the chosen upstream checkout.

## Build a baseline candidate

```sh
sh scripts/bootstrap-openwrt.sh
sh scripts/select-mango.sh
cd upstream/openwrt
make defconfig
cd ../..
sh scripts/build-firmware.sh
```

## Prepare a conservative minimal profile

Start with a fresh, configured OpenWrt tree. The script **writes a separate file** and never edits the original configuration in place.

```sh
python3 scripts/apply-minimal-profile.py upstream/openwrt/.config --output build-output/mango-minimal.config
cp build-output/mango-minimal.config upstream/openwrt/.config
cd upstream/openwrt
make defconfig
cd ../..
sh scripts/build-firmware.sh
```

The overlay disables a small explicit list of optional packages (LuCI, PPP and opkg). Some upstream package selections may be restored by dependency resolution; inspect the resolved `.config` and image manifest. This is a **first pass**, not an optimized Nano image. Do not remove DHCP, Wi-Fi drivers, or essential network tooling without target-specific tests.

## Firmware inventory

```sh
python3 scripts/report-images.py upstream/openwrt/bin/targets --output build-output/images.json
```

Only specify `--budget-bytes N` after confirming the exact writable firmware partition size for the target. The report records image paths, bytes and SHA-256 digests. Its budget result does **not** prove the image is flash-safe.

## Safety

No flashing is performed. Factory and sysupgrade images are not interchangeable. Verify board revision, image metadata, partition map, recovery method and checksums before attempting installation. Record RAM and boot measurements on physical hardware. PocketBox is outside MikroWrt scope.
