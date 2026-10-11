# MikroWrt

**Tiny Linux. Old Hardware. New Possibilities.**

**A small but full-featured Linux distribution for older routers — not a collection of unnecessarily crippled firmware images.**

MikroWrt is an independent, experimental OpenWrt-derived Linux firmware project for resource-constrained routers that contemporary distributions no longer prioritize. It complements OpenWrt; it does not aim to replace it.

## Design principles

- **Usability first:** every released image must provide a useful network role, a tested management path and a documented recovery method.
- **Features are choices:** preserve upstream defaults; add or remove optional features explicitly, rather than permanently removing capabilities.
- **Package management is optional:** use the manager supported by the chosen OpenWrt baseline where feasible; very small images may instead include packages at build time.
- **One distribution, multiple resource tiers:** Nano, Nano+, Micro and Standard are hardware/resource profiles, not incompatible distributions.
- **No artificial limits:** flash, RAM, CPU, driver support and security requirements determine feasibility.

See [feature selection](docs/features.md) and the [usability contract](docs/usability-policy.md).

## Dependency direction

**PocketBox depends on MikroWrt. MikroWrt does not depend on PocketBox.**

MikroWrt is a complete standalone router firmware platform with its own build, tests, releases and hardware support. It must build, boot and work without PocketBox source code, packages, or configuration. PocketBox is developed and released in its own repository as a downstream application.

## Goals

- Restore useful functionality to older routers.
- Target 4 MB flash / 32 MB RAM initially; investigate 4 MB / 16 MB as an ambitious stretch target.
- Produce reproducible, device-specific firmware images measured against real flash and RAM budgets.
- Document installation, administration and recovery before hardware flashing.

## Initial hardware

- GL.iNet GL-MT300N-V2 (Mango): first development target.
- TP-Link TL-WR703N v1: constrained legacy target requiring exact hardware/firmware revision verification.

## Project status

**Experimental build tooling and candidate profiles. No hardware-tested MikroWrt firmware yet.** Do not flash unverified images.

Read the [architecture](docs/architecture.md), [roadmap](docs/roadmap.md), [build guide](docs/build.md), and [WR703N notes](docs/hardware/wr703n.md).

## Security and licensing

Legacy devices may require kernels/drivers without maintained security support. Prefer isolated/offline deployment and do not expose them directly to untrusted networks. OpenWrt/Linux-derived components retain upstream license obligations; project-original materials must declare their licenses.
