import sys
import click

from publisher import publish


@click.command()
def main(args=None):
    """Console script for firelightcircus.com"""
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
