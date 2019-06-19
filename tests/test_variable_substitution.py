from publisher import publish

import pytest

from tests import make_test_dir


@pytest.mark.parametrize(
    "test_template_path,substitutions,expected",
    (
        (
            make_test_dir([("filename_no_substitution", "")]),
            {},
            make_test_dir([("filename_no_substitution", "")])),
        (
            make_test_dir([("{{test}}", "")]),
            {"test": "translation"},
            make_test_dir([("translation", "")])),
        (
            make_test_dir([("{{test}}_{{test_2}}", "")]),
            {"test": "translation", "test_2": "other"},
            make_test_dir([("translation_other", "")])),
        (
            make_test_dir([("test", "test")]),
            {},
            make_test_dir([("test", "test")])),
        (
            make_test_dir([("test", "{{test}}_{{test_2}}")]),
            {"test": "translation", "test_2": "other"},
            make_test_dir([("test", "translation_other")])),
    ),
    ids=[
        "test_file_name_with_no_substitution",
        "test_file_name_with_single_substitution",
        "test_file_name_with_two_substitutions",
        "test_file_with_no_substitution",
        "test_file_with_substitution",
        ])
def test_substitution(test_template_path, substitutions, expected):
    assert False
