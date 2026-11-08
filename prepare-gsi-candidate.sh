#!/usr/bin/env bash
set -euo pipefail

INPUT_DIR="${1:-firmware}"
OUTPUT_DIR="${2:-gsi-candidate}"
mkdir -p "$OUTPUT_DIR"
REPORT="$OUTPUT_DIR/conversion-info.txt"

{
  echo "Universal Firmware Fetcher - system image candidate report"
  echo "This is extraction/preparation, not a guarantee of a bootable universal GSI."
  echo
} > "$REPORT"

# Find payload.bin in downloaded ZIP packages and extract partitions.
PAYLOAD="$(find "$INPUT_DIR" -type f -name payload.bin -print -quit || true)"
if [[ -n "$PAYLOAD" ]]; then
  echo "Found payload.bin: $PAYLOAD" | tee -a "$REPORT"
  python -m pip install --quiet payload-dumper
  mkdir -p "$OUTPUT_DIR/payload-partitions"
  payload_dumper --out "$OUTPUT_DIR/payload-partitions" "$PAYLOAD" || {
    echo "payload-dumper invocation failed; inspect logs and tool version." | tee -a "$REPORT"
    exit 1
  }
fi

# Unpack super.img when present. This is useful for logical partition extraction.
SUPER="$(find "$INPUT_DIR" "$OUTPUT_DIR/payload-partitions" -type f -name super.img -print -quit 2>/dev/null || true)"
if [[ -n "$SUPER" ]]; then
  echo "Found super.img: $SUPER" | tee -a "$REPORT"
  sudo apt-get update -qq
  sudo apt-get install -y android-sdk-libsparse-utils
  mkdir -p "$OUTPUT_DIR/super-partitions"
  lpunpack "$SUPER" "$OUTPUT_DIR/super-partitions" || {
    echo "lpunpack could not unpack super.img." | tee -a "$REPORT"
  }
fi

SYSTEM="$(find "$INPUT_DIR" "$OUTPUT_DIR" -type f -name system.img -print -quit 2>/dev/null || true)"
if [[ -z "$SYSTEM" ]]; then
  echo "No system.img was found. This firmware may use another format or require OEM-specific extraction." | tee -a "$REPORT"
  exit 1
fi

cp "$SYSTEM" "$OUTPUT_DIR/system.img"
{
  echo
  echo "Candidate system image: system.img"
  echo "Source: $SYSTEM"
  echo "Next checks required: image format, architecture, Treble support, dynamic partition layout,"
  echo "AVB/vbmeta requirements, framework/vendor compatibility, SELinux policy and bootability."
  echo "No vendor, boot, vbmeta or device partitions were modified."
} >> "$REPORT"

echo "Prepared system.img candidate at $OUTPUT_DIR/system.img"
