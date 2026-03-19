import yaml
from pathlib import Path


def load_yaml(path: str):
    with open(Path(path), "r") as f:
        return yaml.safe_load(f)
