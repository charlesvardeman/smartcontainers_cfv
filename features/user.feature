Feature: User Information Generation

    Scenario: A known user with an ORCID ID starts Smart Containers
        Given a valid orcid id
        When it is given to smart containers on start
        Then it should create an RDF graph
        And it should contain the user's ORCID information

    Scenario: An unknown user starts Smart Containers
        Given an unknown user
        When it is given to smart containers on start
        Then it should create an RDF graph
        And it should contain a blank node for the unknown user
        And it should contain a has account node containing the username and hostname
