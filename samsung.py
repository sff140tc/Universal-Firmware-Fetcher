from pathlib import Path
import shutil
import subprocess

from .base import Provider

class SamsungProvider(Provider):
    """Samsung FUS downloader through the open-source samloader CLI."""

    def download(self, *, device: str, build: str, region: str, output_dir: Path):
        if not region:
            raise ValueError("Samsung requires a CSC/region, e.g. INS, BTU or EUX.")
        if not shutil.which("samloader"):
            raise RuntimeError("samloader is not installed. Install requirements plus samloader.")

        encrypted = output_dir / "firmware.enc4"
        decrypted = output_dir / "firmware.zip"

        subprocess.run([
            "samloader", "-m", device, "-r", region,
            "download", "-v", build, "-O", str(encrypted)
        ], check=True)

        subprocess.run([
            "samloader", "-m", device, "-r", region,
            "decrypt", "-v", build, "-i", str(encrypted), "-o", str(decrypted)
        ], check=True)

        if not decrypted.exists() or decrypted.stat().st_size == 0:
            raise RuntimeError("Samsung download/decryption did not produce a firmware ZIP.")
        encrypted.unlink(missing_ok=True)
        print(f"Downloaded and decrypted Samsung firmware: {decrypted}")
