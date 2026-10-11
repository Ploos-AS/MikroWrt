# Repository agent guidance

**Hard architectural rule:** PocketBox depends on MikroWrt; MikroWrt must never depend on PocketBox. This repository is an independent firmware distribution, not a PocketBox appliance repository. Do not add PocketBox-specific code, package feeds, build profiles, integration tests or CI dependencies here. Keep any downstream integration in the PocketBox repository or an independent integration repository. Generic extension interfaces are permitted.

Do not import or maintain legacy PirateBox/LibraryBox implementations.

Favor small, reviewable patches. Pin and document upstream sources and toolchain versions. Never imply a built image is flash-safe without real hardware tests and documented recovery. Never commit binary firmware images without provenance, target identity, checksums and release gating. Avoid hardcoded secrets. Preserve upstream licensing and source attribution.
