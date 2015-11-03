"""Configuration manager for reading and writing SC configuration files."""

from search import OrcidSearchResults
import os

__author__ = 'cwilli34'


class ConfigManager(object):
    """ Configuration File Creator """

    def __init__(self):
        """Initialize

        Parameters
        ----------
        :param: none

        Returns
        -------
        :returns: none
        """
        self.filename = 'orcid_turtle.SCconfig'

        if os.environ.get('SC_HOME'):
            self.config_path = os.getenv('SC_HOME')
        else:
            os.environ['SC_HOME'] = os.environ['HOME'] + '/.sc/'
            self.config_path = os.getenv('SC_HOME')

    def write_config(self, user_id=None, email=None, sandbox=True):
        """Write the configuration file
           Writes the configuration file to the SC directory, or program home directory

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: none
        """
        if os.path.exists(self.config_path):
            # Open existing file, read and write
            self.ctgfile = open(self.config_path + self.filename, 'w+')
        else:
            # Create config file, write
            os.mkdir(self.config_path)
            self.ctgfile = open(self.config_path + self.filename, 'w')

        try:
            config_id = self.get_config(user_id, email, sandbox)
            self.ctgfile.write(str(config_id))
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
        if not os.path.exists(self.config_path):
            # If the directory does not exist, we cannot read it.
            message = 'Directory does not exist. Cannot read file.'
            return message
        elif not os.path.exists(self.config_path + self.filename):
            # If the file does not exist, we cannot read it.
            message = 'File does not exist. Cannot read file.'
            return message
        else:
            # Open existing file, read and write
            self.ctgfile = open(self.config_path + self.filename, 'r')
            # Variable data is not used (This is for customizing the script later for future configuration).
            try:
                print(self.ctgfile)
                self.ctgfile.close()
                message = 'File was read successfully.'
                return message
            except:
                self.ctgfile.close()
                message = 'File could not be read.  Please try again.'
                return message

    def get_config(self, user_id=None, email=None, sandbox=True):
        """Write the configuration file
        Writes the configuration file to the SC directory, or program home directory

        Parameters
        ----------
        :param query: string
            Will gather a query string, like a id or email, and then it will search for that string to find
            the Orcid ID that will be written to file.

        Returns
        -------
        :returns: none
        """
        if user_id:
            config_id = user_id
            return config_id
        elif email:
            self.search_obj = OrcidSearchResults(sandbox)
            self.data = self.search_obj.basic_search(email)

            if not self.data:
                print('Email not found.')
            else:
                keys = self.data.keys()
                config_id = keys[0]
                return config_id
