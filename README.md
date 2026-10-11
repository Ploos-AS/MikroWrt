# MikroWrt

**Tiny Linux. Old Hardware. New Possibilities.**

MikroWrt is an experimental, OpenWrt-derived Linux firmware project for resource-constrained routers that contemporary distributions no longer prioritize. It complements OpenWrt; it does not aim to replace it.

## Goals

- Restore useful functionality to older routers.
- Target 4 MB flash / 32 MB RAM initially; investigate 4 MB / 16 MB as an ambitious stretch target.
- Keep PocketBox as a separate application built on top of MikroWrt, not as a fork of PirateBox or LibraryBox.
- Produce reproducible, device-specific firmware images, measured against real flash and RAM budgets.
- Document installation and recovery before hardware flashing.

## Initial hardware

- GL.iNet GL-MT300N-V2 (Mango): first development target.
- TP-Link TL-WR703N v1: constrained legacy target requiring exact hardware/firmware revision verification.

## Project status

**M0: documentation and architecture bootstrap. No hardware-tested firmware yet.** Do not flash unverified images.

Read the [architecture](docs/architecture.md), [roadmap](docs/roadmap.md), and [WR703N notes](docs/hardware/wr703n.md).

## Security and licensing

Legacy devices may require kernels/drivers without maintained security support. Prefer isolated/offline deployment and do not expose them directly to untrusted networks. OpenWrt/Linux-derived components retain upstream license obligations; project-original materials must declare their licenses.
