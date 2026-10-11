# Architecture and boundaries

## Strict one-way dependency

```text
OpenWrt upstream
      |
      v
  MikroWrt        (independent firmware; no PocketBox dependency)
      |
      v
  PocketBox       (separate downstream application/repository)
```

MikroWrt owns firmware/build system, board support, basic networking, recovery, resource budgets, standalone firmware releases and tests. It must remain functional without PocketBox.

PocketBox owns offline HTTP, Telnet/BBS, its application packages, configuration and optional firmware integration. PocketBox depends on MikroWrt, never the reverse.

## Functionality first

MikroWrt is not a stripped-down demo. Retain essential network functions and expose optional features through build-time profiles. Package management must be selectable, **not unconditionally removed**. Default to the package manager of the pinned upstream OpenWrt baseline (opkg on older releases, apk on newer releases); never assume a manager exists without checking the selected baseline. Nano builds may omit a package manager to meet strict flash budgets, but must still provide a useful, documented set of built-in services. USB/extroot is optional where supported.

Historical PirateBox/LibraryBox are reference-only; do not import or maintain their implementations.

## Build strategy

Start from reproducibly pinned OpenWrt sources and board definitions; keep downstream changes minimal and auditable. Target-specific kernel/driver selection must be recorded. MikroWrt firmware must build and boot standalone.

## Target tiers

- Nano: 4 MB flash / 16 MB RAM (research/stretch target, not yet demonstrated).
- Nano+: 4 MB flash / 32 MB RAM (practical constrained target).
- Micro: 8 MB flash / 32 MB RAM.
- Standard: 16 MB flash / 64–128 MB RAM.

Measure compressed kernel, rootfs, flash partition overhead, boot RAM, free memory, CPU and networking functionality per board.

## Delivery gates

Never publish a flashable image before verifying device identity, partition layout, bootloader constraints, exact factory/sysupgrade format, checksum, installation path and recovery path. Hardware test reports are mandatory.
