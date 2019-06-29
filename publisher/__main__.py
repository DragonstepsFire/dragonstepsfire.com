import sys
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape

from publisher import publish

source_path = Path(__file__).parent / "templates"
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
def main(template_dir, target_dir):
    """Console script for firelightcircus.com"""

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']))
    published_to = publish(env, dest_path)
    click.echo(f"Published to {published_to}")
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
