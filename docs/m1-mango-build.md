# M1.5 — Mango candidate build

No hardware-tested firmware or release is available yet.

## Verified upstream source

OpenWrt v24.10.4 resolves to commit `78b23a26c4c98938d549e7ff5876508544e33d4d` (checked using GitHub commit API). The tag's `target/linux/ramips/image/mt76x8.mk` includes `Device/glinet_gl-mt300n-v2` and `TARGET_DEVICES += glinet_gl-mt300n-v2`.

Candidate device config: `CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y`. Kconfig resolution and the firmware build passed in [CI run 38356171732](https://github.com/Ploos-AS/MikroWrt/actions/runs/38356171732) (13 October 2026). This is build-only evidence, not a hardware qualification.

## Build on a supported Linux host

```sh
sh scripts/bootstrap-openwrt.sh
sh scripts/select-mango.sh
cd upstream/openwrt
make defconfig
cd ../..
MIKROWRT_REQUIRE_SSH=1 sh scripts/build-firmware.sh
```

The wrapper runs `make defconfig`, checks recognized management packages, downloads dependencies, compiles firmware and writes reports if successful. If static usability preflight fails, inspect the resolved config and fix the selected packages. No automated flashing.

## Feature choices

**Default: preserve upstream packages.** The optional configuration helper no longer removes LuCI, PPP or package management implicitly.

```sh
python3 scripts/apply-minimal-profile.py upstream/openwrt/.config \
  --output build-output/mango-custom.config --disable ppp --enable ssh
cp build-output/mango-custom.config upstream/openwrt/.config
```

Then run `make defconfig`, inspect the resolved config, and build. The `--package-manager` option accepts `keep` (default), `opkg`, `apk` and `none`; availability depends on the selected upstream release.

## Required validation

- Confirm device-specific flash partition limits and factory/sysupgrade image formats.
- Confirm actual management access, Wi-Fi AP, Ethernet, DHCP/DNS, boot RAM and free flash.
- Record serial boot logs and verified recovery procedure.
- Compare unmodified OpenWrt and custom MikroWrt build outputs.
- Treat all generated images as **UNTESTED — DO NOT FLASH** until qualification.

PocketBox remains a separate downstream project.

## GitHub Actions candidate build (M1.6)

The **Mango firmware candidate** workflow runs automatically on pushes to `main` that change scripts, tests, or the relevant CI workflows. It can also be started manually using **Actions → Mango firmware candidate → Run workflow**. Documentation-only commits do not trigger the full build.

The workflow installs build dependencies on Ubuntu 24.04, checks out the pinned upstream revision, installs OpenWrt feeds, selects the Mango device and runs the guarded build wrapper. Candidate outputs and diagnostic reports are uploaded as the `mango-candidate-unqualified` artifact when available. The first confirmed successful candidate build is [run 38356171732](https://github.com/Ploos-AS/MikroWrt/actions/runs/38356171732); subsequent changes must pass their own CI runs.

**Do not flash CI artifacts.** A successful workflow run is evidence of compilation only, not device safety, runtime administration, correct partition sizes, or recovery.

## Package manifest (M1.7)

A successful build now writes `build-output/packages.json` with the selected OpenWrt packages from the **resolved** `.config`. It is included in the GitHub Actions artifact, whether the workflow was started automatically or manually.

To compare a candidate against a saved stock configuration:

```sh
python3 scripts/report-packages.py upstream/openwrt/.config \
  --baseline build-output/stock-openwrt.config \
  --output build-output/package-diff.json
```

The manifest compares package selections only. It does not prove packages were included in a specific final image, that runtime installation works, or that a firmware build succeeded. Use device-specific image manifests and hardware tests to confirm those properties.

## Candidate image manifest (M1.8)

The build inventories binary candidate images, calculates SHA-256, records sizes and classifies filename-indicated image kinds (`factory`, `sysupgrade`, or `unknown`). The classification is **not** a validation of the image header or flash layout. Optional `--budget-bytes` and `--reserve-bytes` values only become meaningful after the board-specific firmware partition has been verified; no generic 4 MiB budget is assumed.

The Mango workflow requires a filename containing `gl-mt300n-v2` and publishes `build-output/mango-images.json`. It does **not** yet enforce a verified partition budget, validate headers, or confirm boot/recovery. Every image remains **UNTESTED — DO NOT FLASH**.
