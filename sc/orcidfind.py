__author__ = 'cwilli34'

from search import OrcidSearchResults
import click
import simplejson as json

# For testing
from pprintpp import pprint as pp

SEARCH_VERSION = "/v1.2"
API_VERSION = "/v2.0_rc1"

__version__ = "0.1_alpha"

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()

# def abort_if_false(ctx, param, value):
#     if not value:
#         ctx.abort()

@click.command()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('-s', is_flag=True, help='Basic search for user (when Orcid ID is unknown)')
@click.option('-a', is_flag=True, help='Review a user profile by Orcid ID')

def search_type(s, a):
    if s:
        query = click.prompt('Please enter your search terms')
        print('')
        basic_search(query)
    elif a:
        print('There are several ways of getting summarized information on an Orcid user:\n\n'
              '1. Summary* (A complete profile of the user)\n'
              '2. Education\n'
              '3. Employment\n'
              '4. Funding\n'
              '5. Peer Review\n'
              '6. Work\n')
        print('*Summary data is in JSON format. Sometimes a large amount of data can be passed from the '
              'Orcid database. Because of this all output will be written to an external text file.  The text '
              'file will be saved in the program\'s directory.\n')
        selection = click.prompt('Please enter your selection')
        record_type = None
        put_code = None

        print('')

        if selection == '1':
            record_type = None
        if selection == '2':
            record_type = 'education'
        elif selection == '3':
            record_type = 'employment'
        elif selection == '4':
            record_type = 'funding'
        elif selection == '5':
            record_type = 'peer-review'
        elif selection == '6':
            record_type = 'work'

        query = click.prompt('Please enter the Orcid ID')

        advanced_search(query, record_type, put_code)

def basic_search(query):
    """ Function for initializing a search for an orcid id"""
    terms = query.replace(' ', ' AND ')
    print terms

    search_obj = OrcidSearchResults()
    results = search_obj.basic_search(terms)
    actual_total = search_obj.actual_total_results
    total_results = search_obj.total_results

    # orcid_id = search_obj.orcid_id

    search_obj.print_basic()

    if total_results < actual_total:
        print 'Actual Total Results: {}'.format(actual_total)

def advanced_search(query, record_type, put_code):
    search_obj = OrcidSearchResults()

    if record_type is not None:
        put_code = click.prompt('Please enter the put-code (must match record type)')
        results = search_obj.advanced_search(query, record_type, put_code)
        print('')
        print(json.dumps(results, sort_keys = True, indent=4, ensure_ascii=False))

        while True:
            send_to_file = click.prompt('Would you like to send this output to a file [y/N]?')

            if send_to_file == ('y' or 'Y' or 'yes' or 'YES' or 'Yes'):
                with open(query + '_' + record_type + '_' + put_code + '.json', 'w') as outfile:
                    json.dump(results, outfile, sort_keys = True, indent=4, ensure_ascii=False)
                break
            elif send_to_file == ('n' or 'N' or 'no' or 'NO' or 'No'):
                break
            else:
                print('You did not pick an appropriate answer.')
    else:
        results = search_obj.advanced_search(query)

        with open(query + '.json', 'w') as outfile:
            json.dump(results, outfile, sort_keys = True, indent=4, ensure_ascii=False)

    while True:
        new_instance = click.prompt('Back to \'Selection\' menu [y/exit]?')

        if new_instance == ('y' or 'Y' or 'yes' or 'YES' or 'Yes'):
            search_type(s=False, a=True)
            break
        elif new_instance == ('exit' or 'EXIT' or 'Exit'):
            exit(1)
        else:
            print('You did not pick an appropriate answer.')

if __name__=='__main__':
    search_type()

####################  Extra testing ###########################################
# search_obj = OrcidSearchResults()
# results = search_obj.search('coull AND brent')
# actual_total = search_obj.actual_total_results
# total_results = search_obj.total_results
# orcid_id = search_obj.orcid_id
#
#
# search_obj.print_results()
#
# pp(results)
# pp(orcid_id)
# pp(total_results)
# pp(actual_total)


# Examples
# Get the summary
# summary = api.read_record_public('0000-0003-1519-9457', 'activities')

# Get a specific record
# employment = api.read_record_public('0000-0003-1519-9457', 'employment', '16372')
# school = api.read_record_public('0000-0003-1519-9457', 'education', '16371')

# Print - For Testing
# pp(employment)
# pp(school)
# pp(search_results)
# print school['organization']['name']


# search_results = api.search_public('Notre Dame')['orcid-search-results']['orcid-search-result'][0]['orcid-profile']['orcid-bio']['personal-details']['family-name']['value']

# school_encoded = ComplexEncoder().encode(school['organization']['address']['city'])
# print school_encoded.strip('"')
# print json.dumps(school['organization']['name'])
###############################################################################