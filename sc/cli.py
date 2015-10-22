import click
import os
from configmanager import ConfigManager
from docker import Docker
from orcidfind import OrcidSearchResults, search_type
from pprintpp import pprint as pp

# from ._version import __version__

# Set sandbox variable
sandbox = False

class Settings(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

@click.group()
def cli():
    """Smartcontainers for software and data preservation."""
    pass

@cli.command()
@click.option('--config', '-c', help='Run configure command')
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
    """Publish a image to a public repository.


    :param 'image':
    """
    pass

@cli.command()
def preserve():
    """Preserve workflow to container using umbrella.


    :param 'image':
    """
    pass

########  Orcid Commands  ###############
@cli.command()
@click.option('-i', default=None, help='Search for an Orcid profile by Orcid ID.')
@click.option('-e', default=None, help='Search for an Orcid profile by email.')
def orcid(i, e):
    """Create a config file, based on an Orcid ID."""
    if i:
        config_by_id(i)
    elif e:
        config_by_email(e)
    elif i == None and e == None:
        config_by_search()
    else:
        print('You have not selected a viable option.')

def config_by_search():
    """Create a RDF Graph configuration file by searching for Orcid user."""
    search_type(args=['-c'])

def config_by_id(id):
    """Create a RDF Graph configuration file by Orcid ID."""
    config = ConfigManager(orcid_id=id, sandbox=sandbox)
    config.write_config()

def config_by_email(email):
    """Create a RDF Graph configuration file by Orcid email."""
    config = ConfigManager(orcid_email=email, sandbox=sandbox)
    config.write_config()

########  End Orcid  #####################
if __name__ == '__main__':
    cli()
