import click
import os
#from ._version import __version__


class Config(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

@click.group()
def cli():
    pass

@cli.command()
@click.option('--config', '-c', help='Run configure comand')
#@click.option('--genMeta','-g', help='Docker image name')
#@click.version_option(version=__version__)
#@click.pass_context
def config(config):
#    ctx.obj = Archive(create, genMeta)
    pass

@cli.command()
@click.argument('command')
@click.argument('image')
def docker(command,image):
           click.echo('Command is: %s' % command )
           click.echo('image is: %s' % image)

@cli.command()
def search():
    pass

if __name__ == '__main__':
    cli()
