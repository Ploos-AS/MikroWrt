# GL.iNet GL-MT300N-V2 (Mango) — M1 qualification

Mango is the initial hardware build target, not yet a verified MikroWrt release.

## Required identification

- [ ] Read label and board revision from physical device.
- [ ] Verify flash/RAM and partition layout against the selected OpenWrt source tree.
- [ ] Confirm the OpenWrt device target and profile via `make menuconfig` and build output.
- [ ] Confirm correct factory versus sysupgrade image format.
- [ ] Document serial access, failsafe and recovery before flashing.

## Build process

Use the upstream bootstrap script and configure the **actual Mango device profile** in the OpenWrt menu. Then use `sh scripts/build-firmware.sh` from the MikroWrt repository root. This intentionally does not hard-code an unverified profile name.

Do not use generated images on hardware until checksums, image headers, exact board identity and recovery procedures have been independently verified.

## Runtime acceptance criteria

- [ ] Boot log captured over serial.
- [ ] Ethernet operational.
- [ ] Wi-Fi AP and DHCP operational.
- [ ] DNS functional.
- [ ] Boot RAM/free memory and flash footprint measured.
- [ ] Repeat boot and recovery tests performed.

PocketBox is out of scope for MikroWrt acceptance.
