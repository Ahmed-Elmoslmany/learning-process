Feature: Meta data about our project

    Scenario: Get project meta data
    Given a request url http://127.0.0.1:5000/about
    When the request sends GET
    Then the response status is 200
        And the response json at $.project is equal to "CandidatesExporter"
        And the response json at $.package is equal to "CandidatesExporter"
        And the response json at $.description contains "Custom tasks to automate"
        And the response json at $.description contains "developement CandidatesExporter"
        And the response json at $.copyright is equal to "2025 AE company"
        And the response json at $.author is equal to "AE Company"
        And the response json at $.author_email is equal to "ahmedelmoslmany74@gmail.com"
        And the response json at $.release is equal to "0"
        And the response json at $.build_number is equal to "0.1"
        And the response json at $.version is equal to "0.0.1"
        
