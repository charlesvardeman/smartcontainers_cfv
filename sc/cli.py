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
    pass

@cli.command()
@click.option('--config', '-c', help='Run configure comand')
def config(config):
    pass

@cli.command()
@click.argument('command')
@click.argument('image')
def docker(command, image):
    processdocker = Docker(command, image)
    processdocker.sanity_check()

@cli.command()
def search():
    pass

if __name__ == '__main__':
    cli()
