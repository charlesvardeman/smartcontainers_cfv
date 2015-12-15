"""CLI program that allows the user to input keywords for a basic search of the Orcid API.  It uses
    the OrcidManager class to find the Orcid ID and data.
"""

from orcidmanager import OrcidManager
import click

__author__ = 'cwilli34'


def orcid_search(sandbox):
    """Get the Orcid_id from the email search

    Parameters
    ----------
    :param sandbox: boolean
        Should the sandbox be used. True (default) indicates development mode.

    Returns
    -------
    :returns orcid.orcid_Id: string
        Returns the Orcid ID from a basic search by user.
    """
    # Prompt and get search terms
    print('* You can leave fields blank *')
    query = {
        'first_name': click.prompt('Please enter a first name', default='', show_default=False),
        'last_name': click.prompt('Please enter a last name', default='', show_default=False),
        'email': click.prompt('Please enter an email', default='', show_default=False),
        'keywords': click.prompt('Please enter some keywords (like country, department or institution)',
                                 default='', show_default=False)
    }
    print('')

    first_name = query['first_name']
    last_name = query['last_name']
    email = query['email']
    keywords = query['keywords']

    if first_name:
        first_name = 'given-names:' + query['first_name']
    if last_name:
        last_name = 'family-name:' + query['last_name']
    if email:
        email = 'email:' + query['email']

    # Configures search string for lucene formatting
    if first_name and last_name:
        first_name += ' AND '
    elif first_name and (email or keywords):
        first_name += ' AND '
    if last_name and (email or keywords):
        last_name += ' AND '
    if not last_name and not first_name:
        if email and keywords:
            email += ' AND '
    else:
        if email and keywords:
            email = '(' + email + ' AND '
            keywords += ')'

    search_terms = first_name + last_name + email + keywords

    # View string input
    print search_terms + '\n'

    # Call OrcidManager from orcidmanager.py
    orcid = OrcidManager(query=search_terms, sandbox=sandbox)

    while orcid.orcid_id is None:
        orcid = orcid_search(sandbox)
        if orcid.orcid_id:
            break

    return orcid
