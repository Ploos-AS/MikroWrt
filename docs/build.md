# Development build bootstrap

M1 is not yet a tested firmware release. The repository currently provides bootstrap tooling and image-budget checks, **not a ready-to-flash image**.

## Prerequisites

Linux development host, Git, Python 3. Follow upstream OpenWrt build dependency guidance for the selected release.

## Bootstrap

```sh
sh scripts/bootstrap-openwrt.sh
```

This clones an upstream OpenWrt checkout into `upstream/openwrt` at a default reference for **exploration only**. The reference must be reviewed for support and pinned to a full immutable commit before a reproducible release build. No board config is selected and no firmware is built by this script.

## Image budget

```sh
python3 scripts/check-budget.py path/to/image.bin --max-bytes ACTUAL_PARTITION_BYTES
```

Do not substitute total flash capacity for actual writable firmware partition size. Passing a size check is not sufficient to establish flash safety.

## Test

```sh
python3 -m unittest discover -s tests -v
```

## Next

Identify a maintained OpenWrt baseline for Mango and separately evaluate legacy ath79/WR703N support. Record each board's exact partition layout, image format, serial recovery method and build commit before generating device-specific images.
