from orcidconfigmanager import OrcidConfig
import os
import ConfigParser

__author__ = 'cwilli34'


class ConfigManager(object):
    def __init__(self):
        self.Config = ConfigParser.ConfigParser()
        self.filename = 'orcid.SCconfig'
        self.exist = os.path.exists('orcid.SCconfig')
        self.d = []

    def get_orcid(self, orcid_id):
        orcid_profile = OrcidConfig(orcid_id)
        self.d = orcid_profile.get_dict()

    def write_config(self):
        ctgfile = None
        if self.exist:
            # Open existing file, read and write
            ctgfile = open("orcid_search.SCconfig", 'w+')
        else:
            # Create config file, write
            cfgfile = open("orcid_search.SCconfig", 'w')

        self.Config.add_section('OrcidUser')
        self.Config.set('OrcidUser', 'FirstName')
        self.Config.set('OrcidUser', 'LastName')
        self.Config.set('OrcidUser', 'Email')
        self.Config.set('OrcidUser', 'OrcidID')
        self.Config.set('OrcidUser', 'Institution')
        self.Config.set('OrcidUser', 'Department')
        self.Config.set('OrcidUser', 'ExternalID')

        self.Config.write(cfgfile)
        cfgfile.close()
