#!/bin/sh
# Build configured OpenWrt; fail on missing management before compiling.
set -eu
: "${OPENWRT_DIR:=upstream/openwrt}"
: "${BUILD_JOBS:=2}"
: "${MIKROWRT_REQUIRE_SSH:=0}"
case "$BUILD_JOBS" in *[!0-9]*|'') echo "BUILD_JOBS must be a positive integer" >&2; exit 2;; esac
[ "$BUILD_JOBS" -gt 0 ] || { echo "BUILD_JOBS must be positive" >&2; exit 2; }
[ -f "$OPENWRT_DIR/Makefile" ] || { echo "Missing OpenWrt checkout: $OPENWRT_DIR" >&2; exit 2; }
[ -f "$OPENWRT_DIR/.config" ] || { echo "Configure OpenWrt first (make menuconfig)" >&2; exit 2; }
grep -Eq '^CONFIG_TARGET_[^=]+_DEVICE_[^=]+=y$|^CONFIG_TARGET_PROFILE="[^"]+"' "$OPENWRT_DIR/.config" || {
  echo "No selected device/profile found in .config; refusing generic build" >&2; exit 2;
}
mkdir -p build-output
(
  cd "$OPENWRT_DIR"
  echo "OpenWrt revision: $(git rev-parse HEAD)"
  make defconfig
)
case "$MIKROWRT_REQUIRE_SSH" in
  0) python3 scripts/check-usability.py "$OPENWRT_DIR/.config" --output build-output/usability.json ;;
  1) python3 scripts/check-usability.py "$OPENWRT_DIR/.config" --require-ssh --output build-output/usability.json ;;
  *) echo "MIKROWRT_REQUIRE_SSH must be 0 or 1" >&2; exit 2 ;;
esac
(
  cd "$OPENWRT_DIR"
  make download -j"$BUILD_JOBS"
  make -j"$BUILD_JOBS" V=s
)
printf '%s\n' "Build completed; images are NOT qualified for flashing."
find "$OPENWRT_DIR/bin/targets" -type f \( -name '*.bin' -o -name '*.img' \) -exec sha256sum {} \; > build-output/image-sha256.txt
python3 scripts/report-images.py "$OPENWRT_DIR/bin/targets" --output build-output/images.json
python3 scripts/report-packages.py "$OPENWRT_DIR/.config" --output build-output/packages.json
printf '%s\\n' "Build artifacts found; images remain UNTESTED — DO NOT FLASH."\n