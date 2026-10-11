# Usability contract

MikroWrt is a small but full-featured Linux distribution for older routers. Device limitations must be measured, not imposed arbitrarily.

## Invariants

1. A released image must perform its declared network role (AP, router, bridge or another explicit role).
2. It must have a **tested** administration path. SSH is preferred when feasible; serial console or another interface may be appropriate, but cannot be assumed present on consumer hardware.
3. It must have a documented and tested recovery procedure before release.
4. Package management must be optional and selected according to available space and the upstream baseline. If omitted, document how users add features via rebuilding, or external storage where supported.
5. Feature choices must remain reversible in source configuration; no permanent fork for each profile.
6. No firmware release based solely on static config checks.

## Initial static preflight

```sh
python3 scripts/check-usability.py upstream/openwrt/.config --require-ssh
```

This checks a small set of known package names and reports possible omissions. It is **not** a substitute for inspecting OpenWrt's resolved configuration, built-in BusyBox applets, board recovery facilities, or physical boot/network tests. A false negative is possible if administration is supplied by a different package. A false positive is possible if a package is selected but nonfunctional.

The current tool treats missing recognized management as an error and missing DHCP or package management as warnings. A bridge need not run DHCP; a 4 MB device need not include a package manager. Build tooling should eventually support explicit, board-specific exemptions backed by documented recovery and administration tests.

## Feature selection

Keep upstream packages by default. Use `scripts/apply-minimal-profile.py` with explicit `--enable` and `--disable` only. Follow with `make defconfig`, static preflight, firmware build, and hardware qualification.
