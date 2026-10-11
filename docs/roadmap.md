# Roadmap

## M0 — Foundations

- [x] Record scope, non-goals and architecture.
- [ ] Select pinned OpenWrt baseline(s) using build and support evidence.
- [ ] Add source/bootstrap tooling and containerized build environment.
- [ ] Add image-size and build-metadata reporting to CI.
- [ ] Record known-safe flashing/recovery paths per hardware revision.

## M1 — Mango reference

- [ ] Minimal bootable image for GL-MT300N-V2.
- [ ] Serial boot log, network test, RAM and flash measurements.
- [ ] Repeatable builds and recovery test.

## M2 — WR703N legacy

- [ ] Document verified WR703N hardware revisions and flash layouts.
- [ ] Reproducible 4/32 image with minimal networking where possible.
- [ ] Factory/sysupgrade formats and recovery qualification.
- [ ] Explore 4/16 target experimentally; report feasibility honestly.

## M3 — PocketBox integration

- [ ] Create build-time PocketBox package/profile.
- [ ] Validate offline Wi-Fi AP, HTTP, Telnet/BBS and Ethernet access to an attached host.
- [ ] Keep PocketBox application independent of MikroWrt firmware.

## M4+ — Profiles, supported devices, releases

- [ ] Additional purpose-specific networking profiles.
- [ ] Security support matrix and lifecycle documentation.
- [ ] Public hardware-qualified firmware releases.
