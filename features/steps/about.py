import requests
from behave import given, when, then

API_URL = "http://localhost:5000"

@given('I want to know project meta data')
def step_given_want_project_data(context):
    context.base_url = API_URL
    

@when('I send a GET request to "{end_point}"')
def step_when_send_get_request(context, end_point):
    context.response = requests.get(f'{API_URL}{end_point}')
    

@then('The response status code should be {status_code:d}')
def step_then_check_status_code(context, status_code):
    assert context.response.status_code == status_code    
    

@then('The response should contain project "{project_name}"')
def step_then_check_project_name(context, project_name):
    response_json = context.response.json()
    response_project_name = response_json.get('project')
    assert response_project_name == project_name


@then('The response should contain author "{author_name}"')
def step_then_check_author_name(context, author_name):
    response_json = context.response.json()
    response_author_name = response_json.get('author')
    assert response_author_name == author_name    


@then('The response should contain author email "{author_email}"')
def step_then_check_author_email(context, author_email):
    response_json = context.response.json()
    response_author_email = response_json.get('author_email')
    assert response_author_email == author_email    
    
    