# M0 build acceptance and hardware gates

M0 tooling exists, but **M0 firmware is not yet qualified**. The initial build target is the GL.iNet Mango; TL-WR703N v1 is the later constrained target. Do not promote a successful static test to a successful firmware build or boot.

## CI/static checks (available now)

- Python unit tests: `python3 -m unittest discover -s tests -v`.
- Shell syntax: `sh -n scripts/bootstrap-openwrt.sh scripts/select-mango.sh scripts/build-firmware.sh`.
- Build wrapper resolves `make defconfig`, checks management package selections, inventories selected packages, requires firmware artifacts, and hashes resulting images.
- Size tool checks explicit firmware-partition limits; it can require additional reserved bytes.

Example **only after the actual firmware partition budget has been verified**:

```sh
python3 scripts/check-budget.py path/to/firmware.bin --max-bytes ACTUAL_PARTITION_BYTES --reserve-bytes REQUIRED_MARGIN_BYTES
```

The placeholders are intentional; never use nominal 4 MiB flash as the automatic WR703N firmware budget.

## M0 exit criteria

- [ ] Reproducible OpenWrt checkout at the pinned commit with recorded toolchain.
- [ ] Resolve Mango device Kconfig and selected package list in that checkout.
- [ ] Complete a full build with archived logs, package report, image inventory and SHA-256.
- [ ] Measure each relevant image against its **device-specific** firmware partition budget.
- [ ] Document a board-specific recovery procedure before flashing.
- [ ] Verify boot, administrative access and basic network functionality on hardware.
- [ ] Mark all untested images **UNTESTED — DO NOT FLASH**.

## Resource tiers

- **Nano (4/16)** is experimental; never promise a functional image before measurement.
- **Nano+ (4/32)** is the WR703N-class research target.
- Higher tiers retain optional package management and richer services when feasible.
- No artificial removal of administrative or networking functionality just to meet an arbitrary size goal.

## Boundaries

MikroWrt is standalone. PocketBox is a downstream consumer and does not belong in MikroWrt's build dependencies. PirateBox/LibraryBox are historical research, not active firmware dependencies.
