from pathlib import Path
from urllib.parse import quote
import requests

from .base import Provider

class GooglePixelProvider(Provider):
    """Official Google factory image URL convention."""

    def download(self, *, device: str, build: str, region: str, output_dir: Path):
        if not device or not build:
            raise ValueError("Pixel device codename and build number are required.")

        filename = f"{device}-{build}-factory.zip"
        url = f"https://dl.google.com/dl/android/aosp/{quote(filename)}"
        destination = output_dir / filename

        with requests.get(url, stream=True, timeout=(30, 180)) as response:
            if response.status_code == 404:
                raise RuntimeError(
                    "Google did not return a factory image for this device/build. "
                    "Check the codename and exact build number."
                )
            response.raise_for_status()
            with destination.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)

        if destination.stat().st_size == 0:
            destination.unlink(missing_ok=True)
            raise RuntimeError("Google returned an empty download.")
        print(f"Downloaded official factory image: {destination}")
