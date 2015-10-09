"""CLI program to read the orcidconfigmanager.py and create a RDF configuration
    file with Turtle syntax
"""
from orcidconfigmanager import OrcidConfig
import rdflib
import os

__author__ = 'cwilli34'


class ConfigManager(object):
    """ Configuration File Creator """

    def __init__(self, orcid_id=None, orcid_email=None, sandbox=True):
        """Initialize

        Parameters
        ----------
        :param orcid_id: string
            When s is true, click prompts will be executed and the basic_search() function will be executed.
        :param sandbox: boolean
            Should the sandbox be used. True by default. False (default) indicates production mode.
        """
        os.environ['SC_HOME'] = os.environ['HOME'] + '/.sc/'
        self.filename = 'orcid_turtle.SCconfig'
        self.config = OrcidConfig(orcid_id, orcid_email, sandbox)
        self.ctgfile = None

    def write_config(self):
        """Write the configuration file
            Writes the configuration file to the SC directory, or program home directory

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: none
        """
        config_path = os.getenv('SC_HOME')
        if os.path.exists(config_path):
            # Open existing file, read and write
            self.ctgfile = open(config_path + self.filename, 'w+')
        else:
            # Create config file, write
            os.mkdir(os.environ['SC_HOME'])
            self.ctgfile = open(config_path + self.filename, 'w')

        try:
            profile = self.config.get_turtle()
            self.ctgfile.write(str(profile))
            self.ctgfile.close()
            print('The configuration file has been created.')
        except:
            print('An unexpected error has occurred.  The configuration file could not be created.')
            self.ctgfile.close()

    def read_config(self):
        """Read the configuration file.  The configuration file is in a Turtle syntax format and
            is intended for RDF graph creation.  The 'result' returned will be parsed as RDF

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: object
            Returns data as a RDF object for creating RDF graphs
        :returns: string
            If the configuration file does not exist, return error string
        """
        # g = rdflib.Graph()
        config_path = os.getenv('SC_HOME')
        if not os.path.exists(config_path):
            # If the directory does not exist, we cannot read it.
            message = 'Directory does not exist. Cannot read file'
            return message
        elif not os.path.exists(config_path + self.filename):
            # If the file does not exist, we cannot read it.
            message = 'File does not exist. Cannot read file'
            return message
        else:
            # Open existing file, read and write
            self.ctgfile = open(config_path + self.filename, 'r')
            # Variable data is not used (This is for customizing the script later for future configuration).
            try:
                # data = self.ctgfile.read()
                # result = g.parse(self.ctgfile, format='turtle')
                self.ctgfile.close()
                message = 'File was read successfully.'
                return message
            except:
                self.ctgfile.close()
                message = 'File could not be read.  Try again'
                return message
