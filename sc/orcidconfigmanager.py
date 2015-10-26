"""CLI program that uses an Orcid ID and Python requests to lookup user data in
    Turtle syntax.  It passes this data to the configmanager.py
"""
import requests
from search import OrcidSearchResults

__author__ = 'cwilli34'


class OrcidConfig(object):
    """Class for OrcidConfig"""

    def __init__(self, orcid_id=None, orcid_email=None, sandbox=False):
        """Initialize

        Parameters
        ----------
        :param orcid_id: string
            Needs orcid_id to perform a request by orcid_id.
        :param orcid_email: string
            Needs an email address to perform a request by email.
        :param sandbox: boolean
            Should the sandbox be used. True by default. False (default) indicates production mode.
        """
        if orcid_email:
            self.search_obj = OrcidSearchResults(sandbox)
            self.data = self.search_obj.basic_search(orcid_email)
            self.orcid_id = self.get_id()
        else:
            self.orcid_id = orcid_id

        try:
            self.url = self.search_obj.url + self.orcid_id
            self.headers = {'Accept': 'text/turtle'}
            self.turtle_config = None
        except:
            print('Orcid ID or email is invalid.  Please try again.')
            exit()

    def get_id(self):
        """Get the Orcid_id from the email search

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: string
            returns the Orcid ID from the email search
        """
        if not self.data:
            print('Email not found.')
        else:
            id = self.data.keys()
            return id[0]

    def get_turtle(self):
        """Get the user information in a Turtle syntax

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: string
            user data in a text format with Turtle syntax
        """
        self.turtle_config = requests.get(self.url, headers=self.headers)

        if (self.turtle_config.status_code == 404) or (self.turtle_config.status_code == 500):
            print('Orcid ID not found.  Please try again.')
            exit()
        else:
            print(str(self.url) + ", Status: " + str(self.turtle_config.status_code))
            return self.turtle_config.text