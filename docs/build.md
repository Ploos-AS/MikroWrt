# Development build bootstrap

M1 is not yet a tested firmware release. The repository provides source bootstrap, a guarded build wrapper, and size checks, **not a ready-to-flash image**.

## Prerequisites

Linux development host, Git, Python 3, and upstream OpenWrt build dependencies.

## Bootstrap and configuration

```sh
sh scripts/bootstrap-openwrt.sh
cd upstream/openwrt
make menuconfig
cd ../..
sh scripts/build-firmware.sh
```

Choose the actual hardware target and device profile in menuconfig. See [Mango qualification](hardware/mango.md). The default upstream reference is for exploration only; verify its availability, compatibility and security support, and pin a full immutable commit before a reproducible release.

The build script checks for an explicit device/profile selection, runs `make defconfig`, downloads sources, builds firmware, and writes image SHA-256 checksums to `build-output/image-sha256.txt`. It does not flash devices, qualify images, or automatically enforce partition-size budgets.

## Image budget

```sh
python3 scripts/check-budget.py path/to/image.bin --max-bytes ACTUAL_PARTITION_BYTES
```

Do not substitute total flash capacity for actual writable firmware partition size. Passing a size check is not sufficient to establish flash safety.

## Tests

```sh
python3 -m unittest discover -s tests -v
sh -n scripts/bootstrap-openwrt.sh scripts/build-firmware.sh
```

## Next

Validate the Mango target and partition map in the pinned upstream tree, build an image, and test boot/recovery on physical hardware. Independently evaluate legacy WR703N support.
