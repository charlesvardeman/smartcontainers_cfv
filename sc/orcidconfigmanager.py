from search import OrcidSearchResults
import requests

__author__ = 'cwilli34'


class OrcidConfig(object):
    def __init__(self, orcid_id, sandbox=True):
        if sandbox is True:
            self.url = 'http://sandbox.orcid.org/' + orcid_id
        else:
            self.url = 'http://pub.orcid.org/' + orcid_id
        self.headers = {'Accept': 'text/turtle'}
        self.turtle_config = None

    def get_turtle(self):
        self.turtle_config = requests.get(self.url, headers=self.headers)
        return self.turtle_config.text
