import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List, Tuple


@contextmanager
def make_test_dir(files_to_make: List[Tuple[str, str]]) -> Path:
    """Create a temporary directory structure to test publishing from a
    directory in an idempotent manner.
    """
    with tempfile.TemporaryDirectory() as temp_path:
        for file_name, contents in files_to_make:
            with open(Path(temp_path, file_name), "w") as handle:
                handle.write(contents)
        yield Path(temp_path)
