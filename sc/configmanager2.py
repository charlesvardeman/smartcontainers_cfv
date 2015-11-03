"""Configuration manager for reading and writing SC configuration files."""

from orcidsearch import OrcidSearchResults
import os

__author__ = 'cwilli34'


class ConfigManager(object):
    """ Configuration File Creator """

    def __init__(self, filename='sc.config'):
        """Initialize

        Parameters
        ----------
        :param: none

        Returns
        -------
        :returns: none
        """
        self.filename = filename

        if os.environ.get('SC_HOME'):
            self.config_path = os.getenv('SC_HOME')
        else:
            os.environ['SC_HOME'] = os.environ['HOME'] + '/.sc/'
            self.config_path = os.getenv('SC_HOME')

        self.config_id = None

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
        if os.path.exists(self.config_path):
            # Open existing file, read and write
            ctgfile = open(self.config_path + self.filename, 'w+')
        else:
            # Create config file, write
            os.mkdir(self.config_path)
            ctgfile = open(self.config_path + self.filename, 'w')

        try:
            ctgfile.write(str(self.config_id))
            ctgfile.close()
            print('The configuration file has been created.')
        except:
            print('An unexpected error has occurred.  The configuration file could not be created.')
            ctgfile.close()

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
            ctgfile = open(self.config_path + self.filename, 'r')
            # Variable data is not used (This is for customizing the script later for future configuration).
            try:
                contents = ctgfile.read()
                print(contents + '\n')
                ctgfile.close()
                message = 'File was read successfully.'
                return message
            except:
                ctgfile.close()
                message = 'File could not be read.  Please try again.'
                return message

    def get_config(self, _id=None, email=None, sandbox=True):
        """Gets the configuration data to send to the write function

        Parameters
        ----------
        :param _id: string
            If a config_id has been passed, then self.config_id = _id and returned.
        :param email: string
            If an email has been passed, then the email will be searched for using OrcidSearchResults(),
            an Orcid ID will be found and returned.
        :param sandbox: boolean
            Should the sandbox be used. True (default) indicates development mode.

        Returns
        -------
        :returns self.config_id: string
            Returns the config_id
        """
        if _id:
            self.config_id = _id
            return self.config_id
        elif email:
            search_obj = OrcidSearchResults(sandbox)
            data = search_obj.basic_search(email)

            if not data:
                print('Email not found.')
            else:
                keys = data.keys()
                self.config_id = keys[0]
                return self.config_id
