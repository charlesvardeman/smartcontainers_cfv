"""CLI program that uses an Orcid ID and Python requests to lookup user data in
    Turtle syntax.  It passes this data to the configmanager.py
"""
import requests

__author__ = 'cwilli34'


class OrcidConfig(object):
    """Class for OrcidConfig"""

    def __init__(self, orcid_id=None, orcid_email=None, sandbox=True):
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
            if sandbox is True:
                self.url = 'http://sandbox.orcid.org/search/orcid-bio/?q=email:' + orcid_email
                self.headers = {'Accept': 'application/orcid+json'}
                self.orcid_id = self.get_id()
            else:
                self.url = 'http://pub.orcid.org/search/orcid-bio/?q=email:' + orcid_email
                self.headers = {'Accept': 'application/orcid+json'}
                self.orcid_id = self.get_id()
        else:
            self.orcid_id = orcid_id
        try:
            if sandbox is True:
                self.url = 'http://sandbox.orcid.org/' + self.orcid_id
                self.headers = {'Accept': 'text/turtle'}
            else:
                self.url = 'http://pub.orcid.org/' + self.orcid_id
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

        data = requests.get(self.url, headers=self.headers)
        data_object = data.json()

        if data_object['orcid-search-results']['num-found'] == 0:
            print('Email not found.')
        else:
            id = data_object['orcid-search-results']['orcid-search-result'][0]['orcid-profile']['orcid-identifier']['path']
            return id

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
        return self.turtle_config.text
