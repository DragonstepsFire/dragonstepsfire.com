"""The publisher package is a light wrapper around jinja2 that's focused on
produce the Fire Light Circus static media website.
"""
import logging
from pathlib import Path

def load_version() -> str:
    """Load the package version from the VERSION file so that all other python
    files can use `import crs_normalizer; crs_normalizer.__version__`.
    """
    with open(Path(__file__).parent / "VERSION") as handle:
        return handle.read().strip()

__version__ = load_version()

logging.basicConfig()
logger = logging.getLogger(__name__) # pylint: disable=invalid-name

__all__ = ["__version__"]
