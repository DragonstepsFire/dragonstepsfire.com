#pytest: disable=missing-module-docstring,missing-function-docstring
import tempfile
from typing import Dict
from pathlib import Path
from publisher.publisher import publish, load_template_variables, create_env

import pytest

from tests import make_test_dir

@pytest.fixture(scope="function")
def site_config() -> Dict:
    return {}

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
def test_substitution(
        test_template_paths,
        substitutions,
        expected,
        site_config):
    with make_test_dir(test_template_paths) as test_dir:
        with tempfile.TemporaryDirectory() as dest_path:
            test_env = create_env(test_template_paths)
            template_variables = load_template_variables(site_config)
            published_dir = publish(
                test_env,
                Path(test_dir),
                template_variables)
            for file_name, contents in expected:
                to_test = Path(published_dir, file_name)
                assert to_test.is_file()
                with open(to_test) as test_handle:
                    assert test_handle.read() == contents
