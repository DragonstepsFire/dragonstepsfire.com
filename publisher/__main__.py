"""The publish portion of this repository should really be it's own project
"""
import sys
from pathlib import Path

import click
import jinja2

from publisher.publisher import publish, create_env, load_template_variables

source_path = Path(__file__).parent / "templates"
site_config = Path(__file__).parent / "site_config.toml"
# TODO: Let users publish to their home directory
#home_dest_path = Path.home() / "firelightcircus_site"
dest_path = Path.cwd() / "firelightcircus_site"

@click.command()
@click.option(
    '-t',
    '--template-dir',
    type=click.Path(exists=True),
    default=str(source_path.absolute()))
@click.option(
    '-o',
    '--target-dir',
    type=click.Path(exists=False, writable=True),
    default=str(dest_path.absolute()))
@click.option(
    '-c',
    '--site-config',
    type=click.Path(exists=False, writable=True),
    default=str(site_config.absolute()))
@click.option(
    '-s',
    '--site-url',
    default="firelightcircus.com")
def main(
        template_dir: Path,
        target_dir: Path,
        site_config: Path,
        site_url: str):
    """Console script for firelightcircus.com"""

    env = create_env(source_path=template_dir)
    template_variables = load_template_variables(site_config, site_url)
    published_to = publish(env, dest_path, template_variables)
    click.echo(f"Finished Publishing to '{published_to}'")
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
