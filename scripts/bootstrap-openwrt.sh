#!/bin/sh
# Fetch a pinned upstream OpenWrt checkout for reproducible local development.
set -eu
: "${OPENWRT_REF:=78b23a26c4c98938d549e7ff5876508544e33d4d}"
: "${OPENWRT_URL:=https://github.com/openwrt/openwrt.git}"
: "${OPENWRT_DIR:=upstream/openwrt}"
if [ -e "$OPENWRT_DIR" ]; then
  echo "Refusing to overwrite $OPENWRT_DIR" >&2
  exit 1
fi
mkdir -p "$(dirname "$OPENWRT_DIR")"
git clone --filter=blob:none "$OPENWRT_URL" "$OPENWRT_DIR"
git -C "$OPENWRT_DIR" checkout --detach "$OPENWRT_REF"
actual=$(git -C "$OPENWRT_DIR" rev-parse HEAD)
printf 'OpenWrt commit: %s\n' "$actual"
if [ "$OPENWRT_REF" = "78b23a26c4c98938d549e7ff5876508544e33d4d" ] && [ "$actual" != "$OPENWRT_REF" ]; then
  echo "Pinned upstream commit mismatch" >&2
  exit 1
fi
echo "Source checkout ready. Firmware build and hardware qualification are still required."
