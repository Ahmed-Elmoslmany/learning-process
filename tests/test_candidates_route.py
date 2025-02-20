from app import app

def test_update_candidate():
    create_data = {
        "firstname": "ahmed",
        "lastname": "elmoslmany",
        "email": "ahmedelmoslmany74@gmail.com"
    }
    response = app.test_client().post('/candidates', json=create_data)
    data = response.json[0]['data']
    assert response.status_code == 201
    assert data['firstname'] == 'ahmed'
    assert data['lastname'] == 'elmoslmany'
    assert data['email'] == 'ahmedelmoslmany74@gmail.com'

def test_get_candidate():
    response = app.test_client().get('/candidates/1')
    data = response.json[0]['data']
    assert response.status_code == 200
    assert data['id'] == 1
    assert data['firstname'] == 'ahmed'
    assert data['lastname'] == 'elmoslmany'
    assert data['email'] == 'ahmedelmoslmany74@gmail.com'
    
def test_delete_candidate():
    response = app.test_client().delete('/candidates/5')
    assert response.status_code == 200
    assert response.json[0]['data']['message'] == 'candidate deleted successfully'
    
def test_update_candidate():
    patch_data = {
        "firstname": "updated! ahmed",
        "lastname": "updated! elmoslmany",
        "email": "updated! ahmedelmoslmany74@gmail.com"
    }
    response = app.test_client().patch('/candidates/2', json=patch_data)
    data = response.json[0]['data']
    assert response.status_code == 200
    assert data['id'] == 2
    assert data['firstname'] == 'updated! ahmed'
    assert data['lastname'] == 'updated! elmoslmany'
    assert data['email'] == 'updated! ahmedelmoslmany74@gmail.com'