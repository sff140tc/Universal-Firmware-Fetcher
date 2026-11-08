from .google_pixel import GooglePixelProvider
from .samsung import SamsungProvider

ALIASES = {
    "samsung": SamsungProvider,
    "google pixel": GooglePixelProvider,
    "pixel": GooglePixelProvider,
}

def get_provider(manufacturer: str):
    key = manufacturer.strip().lower()
    provider = ALIASES.get(key)
    if not provider:
        raise RuntimeError(
            f"No verified downloader is implemented for '{manufacturer}' yet. "
            "See README.md → Provider support before adding an OEM adapter."
        )
    return provider()
