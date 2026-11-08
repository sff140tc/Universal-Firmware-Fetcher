# Universal Firmware Fetcher

A GitHub Actions project for **downloading original stock firmware**, with an optional
second stage that extracts a `system.img` candidate for GSI research.

This project does **not** port ROMs, flash devices, unlock bootloaders, or modify a phone.

## Run it

1. Fork this repository.
2. Open **Actions → Universal Firmware Fetcher**.
3. Choose the manufacturer.
4. Enter the device model/codename.
5. Enter the exact firmware build number.
6. Enter the region/CSC when the manufacturer requires it.
7. Choose **Convert into GSI? → Y - Yes** or **N - No**.
8. Run the workflow and download the generated artifacts.

## Inputs

| Input | Meaning |
|---|---|
| `manufacturer` | OEM family |
| `device` | Exact model number or device codename |
| `build_number` | Exact firmware build |
| `region` | Region, CSC or channel where applicable |
| `convert_gsi` | `N - No` keeps only original firmware; `Y - Yes` attempts system-image extraction |

## Provider support (initial implementation)

| Manufacturer | Status | Notes |
|---|---|---|
| Samsung | Implemented | Uses Samloader/FUS. Supply exact model, CSC and version/build. |
| Google Pixel | Implemented | Downloads the official Google factory image for device codename + build. |
| Vivo / iQOO | Adapter required | No unsupported endpoint is guessed. |
| OPPO | Adapter required | Add a verified official OTA/Firmware provider. |
| OnePlus | Adapter required | Add a verified official OTA/Firmware provider. |
| Honor | Adapter required | Adapter required. |
| Xiaomi / POCO / Redmi | Adapter required | Adapter required. |
| TECNO / Infinix / itel | Adapter required | Adapter required. |
| Motorola | Adapter required | Adapter required. |
| Meizu / Fairphone / Huawei / Realme / Nothing | Adapter required | Adapter required. |
| ZTE / Nubia / RedMagic | Adapter required | Separate adapters may be needed for different update systems. |
| LG | Adapter required | Availability varies; many official update services are discontinued. |

The manufacturer menu is broad so the interface is ready for expansion, but only
providers marked **Implemented** can currently fetch firmware. Unsupported choices
stop with a clear message rather than returning a fabricated or unrelated package.

## GSI option: important limitation

`Y - Yes` currently means **extract/prepare a system-image candidate**, not magically
convert every vendor ROM into a universally bootable GSI. The workflow:

- checks for `payload.bin` and extracts its partitions when possible;
- otherwise checks for `super.img` and attempts to unpack logical partitions;
- copies a discovered `system.img` into the GSI candidate artifact;
- writes a report explaining what was found.

A portable GSI requires Treble compatibility and often additional work for
architecture, dynamic partitions, AVB, SELinux, framework/vendor compatibility,
and device-specific dependencies. A `system.img` by itself is not proof that it
will boot on another device. The original firmware artifact is always retained.

## Local usage

```bash
python -m pip install -r requirements.txt
python -m uffetch download \
  --manufacturer "Google Pixel" \
  --device "panther" \
  --build "TQ3A.230805.001" \
  --output firmware
```

Samsung example:

```bash
python -m uffetch download \
  --manufacturer "Samsung" \
  --device "SM-S918B" \
  --build "S918BXXU..." \
  --region "EUX" \
  --output firmware
```

## Legal and operational notes

- Use firmware intended for your exact model and region.
- Downloads are large; GitHub Actions storage and runtime limits apply.
- OEM download services can change or rate-limit requests.
- Respect OEM terms, copyright, and regional restrictions.
- Do not publish proprietary firmware packages without checking redistribution rights.
