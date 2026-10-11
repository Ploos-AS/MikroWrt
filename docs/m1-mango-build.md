# M1.5 — Mango candidate build

No hardware-tested firmware or release is available yet.

## Verified upstream source

OpenWrt v24.10.4 resolves to commit `78b23a26c4c98938d549e7ff5876508544e33d4` (checked using GitHub commit API). The tag's `target/linux/ramips/image/mt76x8.mk` includes `Device/glinet_gl-mt300n-v2` and `TARGET_DEVICES += glinet_gl-mt300n-v2`.

Candidate device config: `CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2=y`. Final Kconfig resolution and build remain unverified.

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

Open **Actions → Mango firmware candidate (manual) → Run workflow** on the main branch. This is intentionally not triggered by every push.

The workflow installs build dependencies on Ubuntu 24.04, checks out the pinned upstream revision, installs OpenWrt feeds, selects the Mango device and runs the guarded build wrapper. Candidate outputs and diagnostic reports are uploaded as the `mango-candidate-unqualified` artifact when available. The workflow has not yet been confirmed to compile successfully.

**Do not flash CI artifacts.** A successful workflow run is evidence of compilation only, not device safety, runtime administration, correct partition sizes, or recovery.
