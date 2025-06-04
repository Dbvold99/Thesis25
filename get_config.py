"""
This module let you access the CONFIG file wherever in the project.
"""

from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent

_CONFIG_PATH = PROJECT_ROOT / "config.yaml"

with _CONFIG_PATH.open("r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

def get(key, default=None):
    """Convenience accessor with optional default."""
    return CONFIG.get(key, default)