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

PocketBox owns offline HTTP, Telnet/BBS, its application packages, configuration and optional firmware integration. PocketBox depends on MikroWrt, never the reverse. Do not put PocketBox-specific appliances, build profiles, CI dependencies or source imports into MikroWrt core. Generic extension points are acceptable if they are useful independently of PocketBox.

Historical PirateBox/LibraryBox are reference-only: consult straightforward WR703N installation procedures where useful, but do not port, maintain, or depend on their implementations.

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
