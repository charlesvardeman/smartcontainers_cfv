from orcidconfigmanager import OrcidConfig
import rdflib
import os

__author__ = 'cwilli34'


class ConfigManager(object):
    def __init__(self, orcid_id, sandbox=True):
        self.file = 'orcid_turtle.SCconfig'
        self.exist = os.path.exists(self.file)
        self.config = OrcidConfig(orcid_id, sandbox)
        self.ctgfile = None

    def write_config(self):
        if self.exist:
            # Open existing file, read and write
            self.ctgfile = open(self.file, 'w+')
        else:
            # Create config file, write
            self.ctgfile = open(self.file, 'w')
        profile = self.config.get_turtle()
        self.ctgfile.write(str(profile))
        self.ctgfile.close()

    def read_config(self):
        g = rdflib.Graph()
        if not self.exist:
            message = 'File does not exist. Cannot read file'
            return message
        else:
            self.ctgfile = open(self.file, 'r')
            data = self.ctgfile.read()
            result = g.parse(self.ctgfile, format='turtle')
            self.ctgfile.close()
            return result
