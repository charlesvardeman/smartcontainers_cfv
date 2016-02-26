Feature: Docker Containers

    Scenario: Smart containers should pass through any docker commands it doesnt want to keep data on
        Given a docker command that we dont intercept
        When it is given to smart containers to run
        Then it should excecute successfully

    Scenario: Smart containers should be able to extract information stored in a container
        Given a docker container with smart container information
        When it is asked to extract the data
        Then it should pull the data out of the container
        And display it in a way that the user wants

    Scenario: Smart containers intercept the run command and store information in the containers label
        Given a docker run command
        When it is given to smart containers to run
        Then it should extract the command line information
        And it should excecute successfully
        And it adds a label to the executed container

    Scenario: Smart containers intercept the build command and store information in the containers label
        Given a docker build command
        When it is given to smart containers to run
        Then it should extract the command line information
        And it should excecute successfully
        And it adds a label to the executed container
