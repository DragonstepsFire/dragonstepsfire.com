from pathlib import Path
from typing import Dict
import jinja2

def publish(to_publish: Path, substitutions: Dict) -> Path:
    """Take a template directory and a set of substitutions create a published
    directory with the same structure as the to_publish template directory with
    the requested substitutions.
    """
