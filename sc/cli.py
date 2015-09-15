import click
import os
from docker import Docker
# from ._version import __version__


class Settings(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

@click.group()
def cli():
    """Smartcontainers for software and data preservation."""
    pass

@cli.command()
@click.option('--config', '-c', help='Run configure comand')
def config(config):
    """Configure smartcontainers."""
    pass

# We may have to manually handle --help and pass it to docker
@cli.command()
@click.argument('command')
def docker(command):
    """Execute a docker command."""
    processdocker = Docker(command)
    processdocker.sanity_check()
    processdocker.do_command()

@cli.command()
@click.argument('image')
def search(image):
    """Search for information in docker metadata."""
    pass

@cli.command()
@click.argument('image')
def publish(image):
    """Publish a image to a public repository

    :param 'image':
    """
    pass

@cli.command()
def preserve():
    """Preserve workflow to container using umbrella.

    :param 'image':
    """

    pass

if __name__ == '__main__':
    cli()
