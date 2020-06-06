#pytest: disable=missing-module-docstring,missing-function-docstring
import tempfile
from typing import Dict
from pathlib import Path
from publisher.publisher import publish, load_template_variables, create_env
from publisher.__main__ import site_config

import pytest

from tests import make_test_dir


@pytest.mark.parametrize(
    "file_contents,substitutions,expected",
    (
        (
            "",
            {},
            ""),
        (
            "No substitutions",
            {},
            "No substitutions"),
        (
            "This file has {{one}} substitution.",
            {"one": "sub_sub"},
            "This file has sub_sub substitution."),
    ),
    ids=[
        "test_empty_file",
        "test_no_substitution",
        "test_with_substitution",
        ])
def end_to_end_test(
        file_contents,
        substitutions,
        expected):
    with tempfile.TemporaryDirectory(prefix="output_dir") as output_dir:
        input_template = "test_file.html"
        with make_test_dir(input_template, file_contents) as input_dir:
            test_env = create_env(input_dir)
            template_variables = load_template_variables(site_config)
            # Load the variables to be substituted.
            for key, value in substitutions.items():
                template_variables[key] = value

            published_dir = publish(
                test_env,
                Path(output_dir),
                template_variables)
            assert str(published_dir) == output_dir

            print(output_dir)
            print(input_dir)
            with open(Path(output_dir, input_template)) as test_handle:
                actual = test_handle.read()
                print(actual)
                assert actual == expected
