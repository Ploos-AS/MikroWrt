#!/bin/sh
# Select GL-MT300N-V2 on an already-bootstrapped OpenWrt tree.
set -eu
: "${OPENWRT_DIR:=upstream/openwrt}"
[ -f "$OPENWRT_DIR/Makefile" ] || { echo "Missing OpenWrt checkout" >&2; exit 2; }
[ ! -e "$OPENWRT_DIR/.config" ] || { echo "Existing .config: refusing to overwrite" >&2; exit 2; }
device='CONFIG_TARGET_ramips_mt76x8_DEVICE_glinet_gl-mt300n-v2'
# Refuse to apply config if the upstream tree does not contain the requested device.
grep -R -F -q 'glinet_gl-mt300n-v2' "$OPENWRT_DIR/target/linux/ramips/image" || {
  echo "Mango profile not found in upstream tree; verify target naming" >&2; exit 2;
}
cat > "$OPENWRT_DIR/.config" <<EOF
CONFIG_TARGET_ramips=y
CONFIG_TARGET_ramips_mt76x8=y
${device}=y
EOF
echo "Selected Mango candidate profile. Run make defconfig and inspect final .config before building."
