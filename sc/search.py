__author__ = 'cwilli34'

from colorama import Fore, Style
import orcid

# For testing
import simplejson as json


class OrcidSearchResults(object):
    def __init__(self, sandbox=True):
        self.api = orcid.PublicAPI(sandbox)
        self.s_dict = dict()
        self.orcid_id = []

    def basic_search(self, query):
        search_results = self.api.search_public(query, start=0, rows=100)
        results = search_results.get('orcid-search-results', None)
        self.actual_total_results = results.get('num-found', 0)
        result = results.get('orcid-search-result', None)

        if self.actual_total_results > 99:
            self.total_results = 100
        else:
            self.total_results = self.actual_total_results

        for p in range(self.total_results):
            try:
                f_name = result[p]['orcid-profile']['orcid-bio']['personal-details']['given-names']['value']
            except TypeError:
                pass
            try:
                l_name = result[p]['orcid-profile']['orcid-bio']['personal-details']['family-name']['value']
            except TypeError:
                pass


            contact_details = result[p]['orcid-profile']['orcid-bio'].get('contact-details', None)

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
                        l[k+1] = c

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

        ######## For testing ###############
        # results = self.api.search_public(query)
        # pp(results)

    def advanced_search(self, query, record_type=None, put_code=None):
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
        result_text = Fore.YELLOW + Style.BRIGHT + "Search Results: " + Fore.RESET + '(' + \
                      str(self.total_results) + ' Total)'
        result_warning_text = Fore.RED + Style.BRIGHT + "You have a lot of results!!\n" + Fore.RESET + \
                              "Please modify or add more search terms to narrow your results.\n"

        print result_text
        if self.total_results > 30:
            print result_warning_text

        for p in self.s_dict:
            email = self.s_dict[p].get('email')
            l_name = self.s_dict[p].get('l_name')
            f_name = self.s_dict[p].get('f_name')

            id_text = Fore.BLUE + '{0:14}{1:80}'.format('Orcid ID:', Fore.RESET + p.encode('utf8'))
            l_name_text = Fore.BLUE + '{0:14}{1:80}'.format('Last Name:', Fore.RESET + l_name.encode('utf8'))
            f_name_text = Fore.BLUE + '{0:14}{1:80}'.format('First Name:',  Fore.RESET + f_name.encode('utf8'))
            email_text = Fore.BLUE + 'Email:'  + Fore.RESET

            print id_text
            print l_name_text
            print f_name_text

            if email is not None:

                for e in email:
                    email_address_text = email[e]
                    if e == 1:
                        print '{0:24}'.format(email_text) + '{0:80}'.format(email_address_text.encode('utf8'))
                    else:
                        print '{0:14}'.format("") + '{0:80}'.format(email_address_text.encode('utf8'))

            print("")

    # def print_advance(self):


# class ComplexEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, complex):
#             return [obj.real, obj.imag]
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, obj)


