Feature: User Authentication

    Scenario: User Resgiter new account
        Given a request url http://127.0.0.1:5000/register
            And a request json payload
                """
                {
                    "name": "test",
                    "email": "tesfdffsddt@gmail.com",
                    "password": "123456789",
                    "confirmationPassword": "123456789"
                }
                """
        When the request sends POST
        Then the response status is 201
            And the response json at $.name is equal to "test"


    Scenario: User Resgiter with already existed email
        Given a request url http://127.0.0.1:5000/register
            And a request json payload
                """
                {
                    "name": "test",
                    "email": "test@gmail.com",
                    "password": "123456789",
                    "confirmationPassword": "123456789"
                }
                """
        When the request sends POST
        Then the response status is 400
            And the response json at $.message is equal to "this email is already exist!"


    Scenario: Valid user try to login
        Given a request url http://127.0.0.1:5000/login
            And a request json payload
                """
                {
                    "email": "test@gmail.com",
                    "password": "123456789"
                }
                """
        When the request sends POST
        Then the response status is 200
            And the response json at $.name is equal to "test"
            And the response json at $.email is equal to "test@gmail.com"