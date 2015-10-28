import click
import os
from configmanager import ConfigManager
from docker import Docker
from orcidfind import search_type
from pprintpp import pprint as pp

# from ._version import __version__

# Set sandbox variable
sandbox = False


class Settings(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

@click.group()
@click.version_option()
def cli():
    """Smartcontainers for software and data preservation.
    Smartcontainers provides a mechanism to add metadata to Docker
    containers as a JSON-LD label. The metadata is contexualized using
    W3C recommended PROV-O and ORCID IDs to capture provenance information.
    The sc command wrappes the docker commandline interface and passes any
    docker command line parameters through to docker. Any command that changes
    the state of the container is recorded in a prov graph and attached to the resultant
    image.
    """
    pass

@cli.group()
@click.option('--config', '-c', help='Run configure command')
def config(config):
    """Configure smartcontainers. Run sc config to get subcommand options for configuring """
    pass

# We may have to manually handle --help and pass it to docker
@cli.command()
@click.argument('command')
def docker(command):
    """Execute a docker command.
    Example: sc docker run <container id>
    """
    processdocker = Docker(command)
    processdocker.sanity_check()
    processdocker.do_command()

@cli.command()
@click.argument('image')
def search(image):
    """Search for information in docker metadata."""
    pass

@cli.command()
@click.argument('printLabel')
def print_md():
    """Print Metadata label from container."""
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

#  Orcid Commands
@config.command()
@click.option('-i', default=None, help='Search for an Orcid profile by Orcid ID.')
@click.option('-e', default=None, help='Search for an Orcid profile by email.')
def orcid(i, e):
    """Create a config file, based on an Orcid ID."""
    # Make sure sandbox variable is set correctly in cli.py before testing
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
    # Make sure sandbox variable is set correctly in cli.py before testing
    config = ConfigManager(orcid_id=id, sandbox=sandbox)
    config.write_config()

def config_by_email(orcid_email):
    """Create a RDF Graph configuration file by Orcid email."""
    # Make sure sandbox variable is set correctly in cli.py before testing
    email = 'email:' + orcid_email
    config = ConfigManager(orcid_email=email, sandbox=sandbox)
    config.write_config()

#  End Orcid  #####################
if __name__ == '__main__':
    cli()
