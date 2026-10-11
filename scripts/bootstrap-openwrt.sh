#!/bin/sh
# Fetch a pinned upstream OpenWrt checkout for reproducible local development.
set -eu
: "${OPENWRT_REF:=v24.10.4}"
: "${OPENWRT_URL:=https://github.com/openwrt/openwrt.git}"
: "${OPENWRT_DIR:=upstream/openwrt}"
if [ -e "$OPENWRT_DIR" ]; then
  echo "Refusing to overwrite $OPENWRT_DIR" >&2
  exit 1
fi
mkdir -p upstream
git clone --filter=blob:none "$OPENWRT_URL" "$OPENWRT_DIR"
git -C "$OPENWRT_DIR" checkout --detach "$OPENWRT_REF"
git -C "$OPENWRT_DIR" rev-parse HEAD
echo "Verify upstream ref and commit before treating this as a release build."
