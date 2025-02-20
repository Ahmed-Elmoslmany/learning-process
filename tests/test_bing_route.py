from app import app

def test_bing_route():
    response = app.test_client().get('/bing')
    assert response.status_code == 200
    assert response.data == b'bong!'