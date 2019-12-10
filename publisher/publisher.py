from pathlib import Path
from typing import Dict, Union
from ipaddress import IPv4Address, IPv6Address

import jinja2
import toml


ACCEPTED_EXTENSIONS = (".html", ".j2", ".jinja2")

def publish(
        env: jinja2.Environment,
        dest_path: Path,
        template_variables: Dict) -> Path:
    """Take a template directory and a set of substitutions create a published
    directory with the same structure as the template_dir  with the requested
    substitutions.
    """
    # Create dest_path directory if it doesn't exist
    # TODO: Enable nested directory creation if we eventually want that for
    # organization.
    dest_path.mkdir(parents=True, exist_ok=True)

    for template_name in env.list_templates():
        if not template_name.endswith(ACCEPTED_EXTENSIONS):
            continue
        file_path = Path(dest_path, template_name)
        with open(file_path, "w") as output_handle:
            template = env.get_template(template_name)
            template_output = template.render(**template_variables)
            output_handle.write(template_output)
    return dest_path

def create_env(source_path: Path) -> jinja2.Environment:
    """Create the required jinja2 environment for publishing the site, set the
    environment variables, source_path, and dest_path
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(source_path)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
        undefined=jinja2.StrictUndefined)
    return env

# TODO: change str type to a url type
def load_template_variables(
        site_config: Path,
        site_url: str = "localhost") -> Dict:
    """Load the globally scoped variables that are available to all templates.
    """
    template_variables: Dict = {}
    # Static variables that we can just store in a file
    template_variables.update(toml.load(site_config))
    # Dynamic variables that will change depending on where the project path
    template_variables["css_path"] = Path(__file__).parent / "assets" / "css"
    template_variables["js_path"] = Path(__file__).parent / "assets" / "js"
    template_variables["image_path"] = Path(__file__).parent / "assets" / "image"
    template_variables["site_url"] = site_url
    return template_variables
