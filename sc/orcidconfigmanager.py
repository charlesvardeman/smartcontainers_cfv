from search import OrcidSearchResults

__author__ = 'cwilli34'


class OrcidConfig(object):

    def __init__(self, orcid_id):
        search_obj = OrcidSearchResults(sandbox=False)
        response = search_obj.turle_search(orcid_id)
        self.config_dict = dict(response)

    def get_dict(self):
        return self.config_dict


