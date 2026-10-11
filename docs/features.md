# Functionality-first feature selection

MikroWrt should make old routers useful, not artificially cripple them.

## Default policy

- Preserve upstream OpenWrt package selections unless the builder **explicitly** changes them.
- Preserve a usable administration and recovery path for every supported device/profile.
- Preserve the networking function advertised by the profile (AP, router, bridge, etc.).
- Package management is selectable, with upstream default retained unless explicitly overridden.
- Never promise runtime package installation on a full or read-only flash partition.
- An image may be extremely small, but it must be documented as usable for its intended role.
- On limited flash, prefer build-time packages; use extroot or external services only where supported.
- Features can be built in, excluded, or installed later if storage, dependencies, and package feeds permit.
- Legacy unsupported kernels require explicit security and network-exposure warnings.

## Configurable package groups (initial tooling)

`scripts/apply-minimal-profile.py` currently supports `--enable` and `--disable` for `web`, `ppp`, `ssh`, and `dns`. Defaults **do not change any package**. These are candidate OpenWrt config changes, not verified runtime toggles.

Example:

```sh
python3 scripts/apply-minimal-profile.py upstream/openwrt/.config \
  --output build-output/mango-ap.config --disable ppp --enable ssh
```

Copy the candidate to the upstream `.config`, run `make defconfig`, and verify the resolved package list and functional network access. **Do not disable the only management interface.**

## Planned profile UX

Offer a board-aware feature selector, report flash/RAM costs, flag incompatible packages, and refuse builds with no documented management or recovery route. This is future work, not an implemented feature.
