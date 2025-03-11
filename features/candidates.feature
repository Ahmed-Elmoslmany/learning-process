Feature: Candidates CRUD Operations

    Scenario: get single candidate
    Given a request url http://127.0.0.1:5000/candidates/1
    When the request sends GET
    Then the response status is 200
        And the response json at $.data.firstName is equal to "ahmed"
        And the response json at $.data.lastName is equal to "elmoslmany"