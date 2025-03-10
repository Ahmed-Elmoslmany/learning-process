Feature: Meta data about our project

    Scenario: Get project meta data
    Given I want to know project meta data
    When I send a GET request to "/about"
    Then The response status code should be 200
    And The response should contain project "CandidatesExporter"
    And The response should contain author "AE Company"
    And The response should contain author email "ahmedelmoslmany74@gmail.com"
