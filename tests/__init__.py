import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List, Tuple


@contextmanager
def make_test_dir(file_name: str, file_contents: str) -> Path:
    """Create a temporary directory structure to test publishing from a
    directory in an idempotent manner.
    """
    with tempfile.TemporaryDirectory() as temp_path:
        with open(Path(temp_path, file_name), "w") as handle:
            handle.write(file_contents)
        yield Path(temp_path)
