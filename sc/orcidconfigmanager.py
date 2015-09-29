"""CLI program that uses an Orcid ID and Python requests to lookup user data in
    Turtle syntax.  It passes this data to the configmanager.py
"""
import requests

__author__ = 'cwilli34'


class OrcidConfig(object):
    """Class for OrcidConfig"""

    def __init__(self, orcid_id, sandbox=True):
        """Initialize

        Parameters
        ----------
        :param orcid_id: string
            When s is true, click prompts will be executed and the basic_search() function will be executed.
        :param sandbox: boolean
            Should the sandbox be used. True by default. False (default) indicates production mode.
        """
        if sandbox is True:
            self.url = 'http://sandbox.orcid.org/' + orcid_id
        else:
            self.url = 'http://pub.orcid.org/' + orcid_id
        self.headers = {'Accept': 'text/turtle'}
        self.turtle_config = None

    def get_turtle(self):
        """Get the user information in a Turtle syntax

        Parameters
        ----------
        :param orcid_id: None

        Returns
        -------
        :returns: string
            user data in a text format with Turtle syntax
        """
        self.turtle_config = requests.get(self.url, headers=self.headers)
        return self.turtle_config.text
