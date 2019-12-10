import tempfile
from pathlib import Path
from publisher import publish, create_environment

import pytest

from tests import make_test_dir


@pytest.mark.parametrize(
    "test_template_paths,substitutions,expected",
    (
        (
            [("filename_no_substitution", "")],
            {},
            [("filename_no_substitution", "")]),
        (
            [("{{test}}", "")],
            {"test": "translation"},
            [("translation", "")]),
        (
            [("{{test}}_{{test_2}}", "")],
            {"test": "translation", "test_2": "other"},
            [("translation_other", "")]),
        (
            [("test", "test")],
            {},
            [("test", "test")]),
        (
            [("test", "{{test}}_{{test_2}}")],
            {"test": "translation", "test_2": "other"},
            [("test", "translation_other")]),
    ),
    ids=[
        "test_file_name_with_no_substitution",
        "test_file_name_with_single_substitution",
        "test_file_name_with_two_substitutions",
        "test_file_with_no_substitution",
        "test_file_with_substitution",
        ])
def test_substitution(test_template_paths, substitutions, expected):
    with make_test_dir(test_template_paths) as test_dir:
        with tempfile.TemporaryDirectory() as dest_path:
            test_environment = create_environment(test_template_paths)
            published_dir = publish(test_environment, Path(test_dir))
            for file_name, contents in expected:
                to_test = Path(published_dir, file_name)
                assert to_test.is_file()
                with open(to_test) as test_handle:
                    assert test_handle.read() == contents
