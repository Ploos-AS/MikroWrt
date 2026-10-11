# Roadmap

MikroWrt is independent firmware. PocketBox depends on MikroWrt and maintains its own integration roadmap in its own repository.

## M0 — Foundations

- [x] Record scope, non-goals and architecture.
- [x] Add upstream bootstrap tooling and guarded firmware build entrypoint.
- [x] Add image-size checker, tests and CI for tooling.
- [ ] Select and pin supported OpenWrt baseline(s) to full commits.
- [ ] Add image-size and build-metadata reporting to firmware CI.
- [ ] Record known-safe flashing/recovery paths per hardware revision.

## M1 — Mango reference

- [x] Document hardware acceptance criteria.
- [ ] Select and verify actual Mango OpenWrt target/profile.
- [ ] Minimal bootable image for GL-MT300N-V2.
- [ ] Serial boot log, network test, RAM and flash measurements.
- [ ] Repeatable builds and recovery test.

## M2 — WR703N legacy

- [ ] Document verified WR703N hardware revisions and flash layouts.
- [ ] Reproducible 4/32 image with minimal networking where possible.
- [ ] Factory/sysupgrade formats and recovery qualification.
- [ ] Explore 4/16 target experimentally; report feasibility honestly.

## M3 — Generic firmware profiles

- [ ] Standalone minimal AP, router and serial gateway profiles.
- [ ] Reproducible profile-specific resource budgets.
- [ ] Stable downstream application extension points.

## M4+ — Supported devices and releases

- [ ] Additional purpose-specific networking profiles.
- [ ] Security support matrix and lifecycle documentation.
- [ ] Public hardware-qualified firmware releases.
