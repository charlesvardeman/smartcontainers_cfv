"""CLI program to search for a user's Orcid ID, utilizes the python-orcid library
    and Orcid API.
"""
from search import OrcidSearchResults
import click
import simplejson as json
import io
from configmanager import ConfigManager
from os.path import expanduser
import os

# For testing
from pprintpp import pprint as pp

SEARCH_VERSION = "/v1.2"
API_VERSION = "/v2.0_rc1"

__version__ = "0.1"
__author__ = 'cwilli34'

# Set sandbox variable
sandbox = True

# Print program version
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()

# Initialize click
@click.command()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('-a', is_flag=True, help='Review a user profile by Orcid ID')
@click.option('-b', is_flag=True, help='Basic search for user (when Orcid ID is unknown)')
@click.option('-c', is_flag=True, help='Basic search and automated RDF config file creation (when Orcid ID is unknown)')
def search_type(a, b, c):
    """Program main function that accepts click arguments. This function will call the basic_search() or
        advanced_search() functions

    Parameters
    ----------
    :param s: flag
        When s is true, click prompts will be executed and the basic_search() function will be executed.
    :param a: flag
        When a is true, click prompts will be executed and the advanced_search() function will be executed
    """
    if b or c:
        # Prompt and get search terms
        print('* You can leave fields blank *')
        query = {
            'first_name': click.prompt('Please enter a first name', default='', show_default=False),
            'last_name': click.prompt('Please enter a last name', default='', show_default=False),
            'email': click.prompt('Please enter an email', default='', show_default=False),
            'institution': click.prompt('Please enter an institution', default='', show_default=False),
            'department': click.prompt('Please enter a department', default='', show_default=False)
        }
        print('')

        first_name = query['first_name']
        last_name = query['last_name']
        email = query['email']
        institution = query['institution']
        department = query['department']

        # Configures search string for lucene formatting
        if first_name and last_name:
            first_name = first_name + ' AND '
        elif first_name and (email or institution or department):
            first_name = first_name + ' AND '
        if last_name and (email or institution or department):
            last_name = last_name + ' AND '
        if not last_name and not first_name:
            if email and (institution or department):
                email = email + ' AND '
            if institution and department:
                institution = '"' + institution + '"' + ' AND '
            elif (email and institution and not department) or institution:
                institution = '"' + institution + '"'
            if department:
                department = '"' + department + '"'
        else:
            if email and (institution or department):
                email = '(' + email + ' AND '
            if not email and institution and department:
                institution = '(' + '"' + institution + '"' + ' AND '
            elif email and institution and not department:
                institution = '"' + institution + '"' + ')'
            elif email and institution and department:
                institution = '"' + institution + '"' + ' AND '
            elif institution:
                institution = '"' + institution + '"'
            if (email or institution) and department:
                department = '"' + department + '"' + ')'
            elif department:
                department = '"' + department + '"'

        search_terms = first_name + last_name + email + institution + department

        # View string input
        print search_terms + '\n'

        # Call basic_search_config() function
        basic_search_config(search_terms)

        # if c:
        #     # Call basic_search_config() function
        #     basic_search_config(search_terms)
        # else:
        #     # Call basic_search() function
        #     basic_search(search_terms)


    elif a:
        # Print selection options, and prompt for choice
        print('There are several ways of getting summarized information on an Orcid user:\n\n'
              '1. Summary* (A complete profile of the user)\n'
              '2. Education\n'
              '3. Employment\n'
              '4. Funding\n'
              '5. Peer Review\n'
              '6. Work\n'
              '7. Create a RDF configuration file\n'
              '8. Read a RDF configuration file\n')
        print('*Summary data is in JSON format. Sometimes a large amount of data can be passed from the '
              'Orcid database. Because of this all output will be written to an external text file.  The text '
              'file will be saved in the program\'s directory.\n')
        selection = click.prompt('Please enter your selection')
        print('')

        record_type = None

        # Once record_type choice is chosen, and/or put-code is entered, advanced_search() function is called.
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
        elif selection == '7':
            record_type = 'write-rdf'
        elif selection == '8':
            record_type = 'read-rdf'

        query = click.prompt('Please enter the Orcid ID')
        print('')

        advanced_search(query, record_type)


def basic_search(query):
    """ Function for initializing a search for an orcid id.

    Parameters
    ----------
    :param query: string
        Query built from user input.

    Returns
    -------
    :returns: no return.
    """

    # Initialize and populate all variables and dictionaries
    search_obj = OrcidSearchResults(sandbox)
    search_obj.basic_search(query)
    actual_total = search_obj.actual_total_results
    total_results = search_obj.total_results
    # orcid_id = search_obj.orcid_id

    # Print results
    search_obj.print_basic()

    # Print total results if actual results are above 100
    if total_results < actual_total:
        print 'Actual Total Results: {}'.format(actual_total)
        print('')

    # Ask user if they would like to search again.
    while True:
        new_instance = click.prompt('Would you like to search again [y/N]?')
        print('')

        if new_instance == ('y' or 'Y' or 'yes' or 'YES' or 'Yes'):
            search_type(args = ['-b'])
            break
        elif new_instance == ('n' or 'N' or 'no' or 'NO' or 'No'):
            exit(1)
        else:
            print('You did not pick an appropriate answer.')

def basic_search_config(query):
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
    search_obj = OrcidSearchResults(sandbox)
    search_obj.basic_search(query)
    actual_total = search_obj.actual_total_results
    total_results = search_obj.total_results
    # orcid_id = search_obj.orcid_id

    # Print results
    search_obj.print_basic_alt()

    # Print total results if actual results are above 100
    if total_results < actual_total:
        print 'Actual Total Results: {}'.format(actual_total)
        print('')

    # Get list of Orcid ID's from results
    id_list = search_obj.orcid_id

    # Write config if only one result was found
    if total_results == 1:
        orcid_id = id_list[0]
        config = ConfigManager(orcid_id=orcid_id, sandbox=sandbox)
        config.write_config()
    # Allow user to select Orcid profile if multiple results are found
    else:
        id_dict = dict()
        # Get list of Orcid ID's and correspond count with ID
        for i, id in enumerate(id_list):
            id_dict[i + 1] = id

        selected = click.prompt('Select the result # of the record')
        print("")
        orcid_id = id_dict[int(selected)]

        config = ConfigManager(orcid_id=orcid_id, sandbox=sandbox)
        config.write_config()

def advanced_search(query, record_type):
    """ Function for initializing an advanced search for an orcid id.  Utilizes OrcidSearchResults() class
        from search.py

    Parameters
    ----------
    :param query: string
        Orcid ID inputted by user
    :param record_type: string
        User selected record_type that they want to display.  Must have corresponding put-code

    Returns
    -------
    :returns: no return.
        Will write to file for a 'activities' record, or print record to screen for all other records.
        Will prompt user to see if they would like to write customer records to file.

        A large amount of information can be gathered for a 'activities' record_type.  The only option
        allowed at this time is for the JSON output to be written to a JSON file.
    """
    search_obj = OrcidSearchResults(sandbox)

    # Will be 'not None' only if record type is other than 'activities'
    if record_type == 'write-rdf':
        config = ConfigManager(orcid_id=query, sandbox=sandbox)
        config.write_config()
    elif record_type == 'read-rdf':
        config = ConfigManager(orcid_id=query, sandbox=sandbox)
        rdf_graph = config.read_config()
        print rdf_graph
    elif record_type is not None:
        put_code = click.prompt('Please enter the put-code (must match record type)')
        results = search_obj.advanced_search(query, record_type, put_code)
        print('')
        print(json.dumps(results, sort_keys=True, indent=4, ensure_ascii=False))

        # Ask user if they would like to send this information to file
        while True:
            send_to_file = click.prompt('Would you like to send this output to a file [y/N]?')

            if send_to_file == ('y' or 'Y' or 'yes' or 'YES' or 'Yes'):
                with io.open(query + '_' + record_type + '_' + put_code + '.json', 'w', encoding='utf8') \
                        as json_file:
                    data = json.dumps(results, json_file, sort_keys=True, indent=4, ensure_ascii=False)
                    # unicode(data) auto-decodes data to unicode if str
                    json_file.write(unicode(data))
                break
            elif send_to_file == ('n' or 'N' or 'no' or 'NO' or 'No'):
                break
            else:
                print('You did not pick an appropriate answer.')
    else:
        # When 'activities' (option 1 - summary) is selected, prints to file
        results = search_obj.advanced_search(query)

        home_path = expanduser("~")
        dir_path = home_path + "/.sc/"
        filename = query + '.json'
        if os.path.exists(dir_path):
            config_path = dir_path + filename
        else:
            os.mkdir(home_path + "/.sc/")
            config_path = dir_path + filename

        with io.open(config_path, 'w', encoding='utf8') as json_file:
            data = json.dumps(results, json_file, sort_keys=True, indent=4, ensure_ascii=False)
            # unicode(data) auto-decodes data to unicode if str
            json_file.write(unicode(data))

    # Ask user if they would like to go back to the advanced search selection menu
    while True:
        new_instance = click.prompt('Back to \'Selection\' menu [y/exit]?')
        print('')

        if new_instance == ('y' or 'Y' or 'yes' or 'YES' or 'Yes'):
            search_type(args = ['-a'])
            break
        elif new_instance == ('exit' or 'EXIT' or 'Exit'):
            exit(1)
        else:
            print('You did not pick an appropriate answer.')

if __name__ == '__main__':
    search_type()
