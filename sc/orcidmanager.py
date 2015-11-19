"""Class that receives an Orcid ID and Python requests to lookup user data and output to
    Turtle syntax.  It also finds an Orcid ID for basic search terms and email address searches.
"""

import requests
from orcidsearch.search import OrcidSearchResults
import click

__author__ = 'cwilli34'


# noinspection PyBroadException
class OrcidManager(object):
    """Class for OrcidManager"""

    def __init__(self, query=None, orcid_id=None, orcid_email=None, sandbox=True):
        """Initialize

        Parameters
        ----------
        :param orcid_id: string
            Needs orcid_id to perform a request by orcid_id.
        :param orcid_email: string
            Needs an email address to perform a request by email.
        """
        if orcid_email:
            self.search_obj = OrcidSearchResults(sandbox)
            self.data = self.search_obj.basic_search(orcid_email)
            self.orcid_id = self.get_id()
        elif query:
            self.sandbox = sandbox
            self.search_obj = OrcidSearchResults(sandbox)
            self.search_obj.basic_search(query)
            self.orcid_id = self.select_id()
        else:
            self.search_obj = OrcidSearchResults(sandbox)
            self.orcid_id = orcid_id

        if self.orcid_id is not None:
            try:
                self.url = self.search_obj.api._endpoint_public + '/' + self.orcid_id
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
        :returns orcid_id[0]: string
            returns the Orcid ID from the email search
        """
        if not self.data:
            print('No data was found.')
        else:
            orcid_id = self.data.keys()
            return orcid_id[0]

    def get_turtle(self):
        """Get the user information in a Turtle syntax

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns self.turtle_config.text: string
            user data in a text format with Turtle syntax
        """
        self.turtle_config = requests.get(self.url, headers=self.headers)

        if (self.turtle_config.status_code == 404) or (self.turtle_config.status_code == 500):
            print('Orcid ID not found.  Please try again.')
            exit()
        else:
            print(str(self.url) + ", Status: " + str(self.turtle_config.status_code))
            return self.turtle_config.text

    def select_id(self):
        """ Function for initializing a search for an orcid id, and then creates a RDF
            configuration file automatically.

        Parameters
        ----------
        :param query: string
            Query built from user input.

        Returns
        -------
        :returns: no return.
        """

        # Initialize and populate all variables and dictionaries
        actual_total = self.search_obj.actual_total_results
        total_results = self.search_obj.total_results
        # orcid_id = search_obj.orcid_id

        # Print results
        self.search_obj.print_basic_alt()

        # Print total results if actual results are above 100
        if total_results < actual_total:
            print 'Actual Total Results: {}'.format(actual_total)
            print('')

        # Get list of Orcid ID's from results
        id_list = self.search_obj.orcid_id

        # Return ID if only one result was found
        if total_results == 1:
            orcid_id = id_list[0]
            return orcid_id
        # If no results are found
        elif total_results == 0:
            print("No results where found. Please try again.\n")
            orcid_id = None
            return orcid_id

        # Allow user to select Orcid profile if multiple results are found
        else:
            id_dict = dict()
            # Get list of Orcid ID's and correspond count with ID
            for i, d in enumerate(id_list):
                id_dict[i + 1] = d

            selected = None
            while not selected:
                try:
                    selected = click.prompt('Select the result # of the record (Type "N" for another search, '
                                            '"Exit" to abort)')
                    print("")
                    orcid_id = id_dict[int(selected)]
                    return orcid_id
                except KeyError:
                    print('That is not a valid selection.  Please try again.\n')
                    selected = None
                except ValueError:
                    if selected in ('N', 'n'):
                        return None
                    elif selected in ('exit', 'Exit', 'EXIT'):
                        exit()
                    else:
                        print('That is not a valid selection.  Please try again.\n')
                        selected = None
