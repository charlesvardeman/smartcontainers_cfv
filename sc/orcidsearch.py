from colorama import Fore, Style
import orcid
import requests

# For testing
import simplejson as json

__author__ = 'cwilli34'


class OrcidSearchResults(object):

    """Using the Orcid Public API."""

    def __init__(self, sandbox=True):
        """Initialize public API for class.

        Parameters
        ----------
        :param sandbox: boolean
            Should the sandbox be used. True (default) indicates development mode.
        """
        self.api = orcid.PublicAPI(sandbox)
        self.s_dict = dict()
        self.orcid_id = []
        self.url = self.api._endpoint_public

    def basic_search(self, query):
        """Basic search based on search terms entered by user to find an Orcid ID.

        Parameters
        ----------
        :param query: string
            A phrase, or group of search terms with boolean operators for lucene search

        Returns
        -------
        :returns self.s_dict: dict type
            Records with minimal information based on search terms used.
        """
        search_results = self.api.search_public(query, start=0, rows=100)
        results = search_results.get('orcid-search-results', None)
        self.actual_total_results = results.get('num-found', 0)
        result = results.get('orcid-search-result', None)

        # Actual results versus displayed results
        if self.actual_total_results > 99:
            self.total_results = 100
        else:
            self.total_results = self.actual_total_results

        # Only last name, first name, Orcid ID, and email will be displayed for each record
        for p in range(self.total_results):
            try:
                f_name = result[p]['orcid-profile']['orcid-bio']['personal-details']['given-names']['value']
            except TypeError:
                pass
            try:
                l_name = result[p]['orcid-profile']['orcid-bio']['personal-details']['family-name']['value']
            except TypeError:
                pass
            try:
                contact_details = result[p]['orcid-profile']['orcid-bio'].get('contact-details', None)
            except AttributeError:
                pass

            if contact_details is None:
                self.s_dict.update(
                    {
                        result[p]['orcid-profile']['orcid-identifier']['path']:
                            {
                                'f_name': f_name,
                                'l_name': l_name
                            }
                    }
                )
            else:
                email = contact_details.get('email', None)

                if email is None or email == []:
                    self.s_dict.update(
                        {
                            result[p]['orcid-profile']['orcid-identifier']['path']:
                                {
                                    'f_name': f_name,
                                    'l_name': l_name
                                }
                        }
                    )
                else:
                    l = dict()
                    for k, e in enumerate(email):
                        c = e.get('value')
                        l[k + 1] = c

                    self.s_dict.update(
                        {
                            result[p]['orcid-profile']['orcid-identifier']['path']:
                                {
                                    'f_name': f_name,
                                    'l_name': l_name,
                                    'email': l
                                }
                        }
                    )

        # To just get a list of Orcid ID's without any other profile information
        self.orcid_id = self.s_dict.keys()

        return self.s_dict

        # For testing ###
        # results = self.api.search_public(query)
        # pp(results)

    def advanced_search(self, query, record_type=None, put_code=None):
        """Advance search once the Orcid ID is known.  Can find more detailed record information with
            Orcid ID, record type and put codes.

        Parameters
        ----------
        :param query: string
            Id of the queried author.
        :param record_type: string
            One of 'activities', 'education', 'employment', 'funding',
            'peer-review', 'work'. 'activities' is more of a summary.
        :param put_code: string
            The id of the queried work. Must be given if 'request_type' is not
            'activities'.

        Returns
        -------
        :returns: summary, dict type
            summary of user records.
        :returns: education, dict type
            user's education record.
        :returns: employment, dict type
            user's employment record.
        :returns: funding, dict type
            user's funding record.
        :returns: peer_review, dict type
            user's peer review record.
        :returns: work, dict type
            user's research works and publications.
        """
        if put_code and record_type:
            if record_type == 'education':
                education = self.api.read_record_public(query, record_type, put_code)
                return education
            elif record_type == 'employment':
                employment = self.api.read_record_public(query, record_type, put_code)
                return employment
            elif record_type == 'funding':
                funding = self.api.read_record_public(query, record_type, put_code)
                return funding
            elif record_type == 'peer-review':
                peer_review = self.api.read_record_public(query, record_type, put_code)
                return peer_review
            elif record_type == 'work':
                work = self.api.read_record_public(query, record_type, put_code)
                return work

        summary = self.api.read_record_public(query, 'activities')
        return summary

    def print_basic(self):
        """Print basic search results for better user readability.

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: None
        """
        result_text = Fore.YELLOW + Style.BRIGHT + "Search Results: " + Fore.RESET + '(' + \
                      str(self.total_results) + ' Total)'
        result_warning_text = Fore.RED + Style.BRIGHT + "You have a lot of results!!\n" + Fore.RESET + \
                              "Please modify or add more search terms to narrow your results.\n"

        print result_text + '\n'
        if self.total_results > 30:
            print result_warning_text

        for i, p in enumerate(self.s_dict):
            email = self.s_dict[p].get('email')
            l_name = self.s_dict[p].get('l_name')
            f_name = self.s_dict[p].get('f_name')

            id_text = Fore.BLUE + '{0:14}{1:40}'.format('Orcid ID:', Fore.RESET + p.encode('utf8'))
            l_name_text = Fore.BLUE + '{0:14}{1:40}'.format('Last Name:', Fore.RESET + l_name.encode('utf8'))
            f_name_text = Fore.BLUE + '{0:14}{1:40}'.format('First Name:',  Fore.RESET + f_name.encode('utf8'))
            email_text = Fore.BLUE + 'Email:' + Fore.RESET
            count = Fore.BLUE + Style.BRIGHT + '{0:14}{1:40}'.format('Result:', Fore.RESET + Fore.YELLOW + Style.BRIGHT + str(i + 1).encode('utf8') + Fore.RESET)

            print count
            print id_text
            print l_name_text
            print f_name_text

            if email is not None:
                for e in email:
                    email_address_text = email[e]
                    if e == 1:
                        print '{0:24}'.format(email_text) + '{0:40}'.format(email_address_text.encode('utf8'))
                    else:
                        print '{0:14}'.format("") + '{0:40}'.format(email_address_text.encode('utf8'))

            print("")

    def print_basic_alt(self):
        """Print basic search results for better user readability (Alternative Format).

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: None
        """
        result_text = Fore.YELLOW + Style.BRIGHT + "Search Results: " + Fore.RESET + '(' + \
                      str(self.total_results) + ' Total)'
        result_warning_text = Fore.RED + Style.BRIGHT + "You have a lot of results!!\n" + Fore.RESET + \
                              "Please modify or add more search terms to narrow your results.\n"

        print result_text + '\n'
        if self.total_results > 30:
            print result_warning_text

        for i, p in enumerate(self.s_dict):
            email = self.s_dict[p].get('email')
            l_name = self.s_dict[p].get('l_name')
            f_name = self.s_dict[p].get('f_name')

            id_text = p.encode('utf8')
            l_name_text = l_name.encode('utf8')
            f_name_text = f_name.encode('utf8')
            count = Fore.BLUE + Style.BRIGHT + 'Result: ' + Fore.RESET + Fore.YELLOW + Style.BRIGHT + str(i + 1) + Fore.RESET

            email_list = []

            if email is not None:
                for e in email:
                    email_list.insert(e, email[e])

            print(count + ', ' + id_text + ', ' + f_name_text + ' ' + l_name_text + (' (' if email_list else '') +  ', '.join(email_list) + (') ' if email_list else ''))

        print('')

    # Possible to create advance printing dialogs so less code is required in the calling program
    # def print_advance(self):
