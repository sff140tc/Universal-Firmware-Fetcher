from pathlib import Path

class Provider:
    def download(self, *, device: str, build: str, region: str, output_dir: Path):
        raise NotImplementedError
