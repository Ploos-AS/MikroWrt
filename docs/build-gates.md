# Firmware build gates

The build wrapper now runs the static usability preflight **after** `make defconfig` resolves the OpenWrt configuration and **before** downloading or compiling packages.

1. An explicit board profile must be selected.
2. The resolved config must include a recognized management package, otherwise compilation stops.
3. DHCP and package management are advisory, not mandatory; valid bridges and 4 MB devices may omit them.
4. `MIKROWRT_REQUIRE_SSH=1 sh scripts/build-firmware.sh` enforces SSH selection.
5. After a successful build, the wrapper writes `build-output/usability.json`, `build-output/image-sha256.txt`, and `build-output/images.json`.

**Important limitation:** The current management check is package-name-based, not board-aware. OpenWrt may have built-in services or alternative management arrangements that this check does not recognize. Such cases require improving the validator, not bypassing safety checks without a documented tested path.

The wrapper does not automatically enforce image size: firmware partition budgets vary by board and image type. It also does not prove that a selected service actually works, that package feeds are compatible, or that firmware is safe to flash. Those require board-specific hardware qualification.
