# Architecture and boundaries

MikroWrt = firmware/build system, board support, basic networking, recovery, resource budgets.

PocketBox = separate project/application offering offline HTTP and Telnet/BBS experiences. PocketBox may be included during image composition or installed on compatible systems; no dependency on PirateBox or LibraryBox source trees.

Historical PirateBox/LibraryBox are reference-only: consult their straightforward WR703N installation procedures where useful, but do not port, maintain, or depend on their implementations.

## Build strategy

Start from reproducibly pinned OpenWrt sources and board definitions; keep downstream changes minimal and auditable. Target-specific kernel/driver selection must be recorded. Appliance profiles are build-time selections, not a promise of a runtime package manager.

## Target tiers

- Nano: 4 MB flash / 16 MB RAM (research/stretch target, not yet demonstrated).
- Nano+: 4 MB flash / 32 MB RAM (practical constrained target).
- Micro: 8 MB flash / 32 MB RAM.
- Standard: 16 MB flash / 64–128 MB RAM.

Measure compressed kernel, rootfs, flash partition overhead, boot RAM, free memory, CPU and networking functionality per board.

## Delivery gates

Never publish a flashable image before verifying device identity, partition layout, bootloader constraints, exact factory/sysupgrade format, checksum, installation path and recovery path. Hardware test reports are mandatory.
