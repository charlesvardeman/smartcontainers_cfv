Feature: ORCID Management
  In order to link the container to a specific user we need an ID to link to. http://orcid.org/ was selected for this.

  Scenario: Create configuration from a valid ID
    Given an id "0000-0001-5663-6903"
    When it is a valid orcid id
    Then it should create a config file

  Scenario: Create configuration from an invalid ID
    Given an id "9000-0001-5663-6903"
    When it is an invalid orcid id
    Then it should return an error

  Scenario: Create configuration from a valid email
    Given an e-mail "jsweet@nd.edu"
    When it is valid orcid email
    Then it should create a config file

  Scenario: Create configuration from an invalid email
    Given an e-mail "jsweet@ndedu"
    When it is valid orcid email
    Then it should create a config file
