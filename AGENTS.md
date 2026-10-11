# Repository agent guidance

Respect the project's distinct layers: MikroWrt firmware platform; PocketBox application in its own repository. Do not import or maintain legacy PirateBox/LibraryBox implementations.

Favor small, reviewable patches. Pin and document upstream sources and toolchain versions. Never imply a built image is flash-safe without real hardware tests and documented recovery. Never commit binary firmware images without provenance, target identity, checksums and release gating. Avoid hardcoded secrets. Preserve upstream licensing and source attribution. Build-time appliance profiles must remain optional.
