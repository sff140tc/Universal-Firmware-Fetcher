import argparse
import sys
from pathlib import Path

from .providers import get_provider

def main():
    parser = argparse.ArgumentParser(description="Download original stock firmware.")
    sub = parser.add_subparsers(dest="command", required=True)
    dl = sub.add_parser("download")
    dl.add_argument("--manufacturer", required=True)
    dl.add_argument("--device", required=True)
    dl.add_argument("--build", required=True)
    dl.add_argument("--region", default="")
    dl.add_argument("--output", default="firmware")
    args = parser.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    try:
        provider = get_provider(args.manufacturer)
        provider.download(
            device=args.device.strip(),
            build=args.build.strip(),
            region=args.region.strip(),
            output_dir=out,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
