from pathlib import Path
from typing import Dict
from jinja2 import Environment
import jinja2

ACCEPTED_EXTENSIONS = (".html",)

def publish(
        env: Environment,
        target_dir: Path) -> Path:
    """Take a template directory and a set of substitutions create a published
    directory with the same structure as the template_dir  with the requested
    substitutions.
    """
    # Create target directory if it doesn't exist
    # TODO: Enable nested directory creation if we eventually want that for
    # organization.
    target_dir.mkdir(parents=True, exist_ok=True)

    for template_name in env.list_templates():
        if not template_name.endswith(ACCEPTED_EXTENSIONS):
            continue
        file_path = Path(target_dir, template_name)
        with open(file_path, "w") as output_handle:
            template = env.get_template(template_name)
            template_output = template.render()
            output_handle.write(template_output)

