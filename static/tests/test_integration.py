import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    res = client.get('/')
    assert res.status_code == 200

def test_api_predict_success(client):
    res = client.post('/predict', json={'tweet': 'emas naik banyak'})
    assert res.status_code == 200
    assert 'sentiment' in res.get_json()

def test_api_predict_invalid(client):
    res = client.post('/predict', json={'tweet': 'hi'})
    assert "Tidak Valid" in res.get_json()['sentiment']

def test_api_stats(client):
    res = client.get('/get_stats')
    assert res.status_code == 200
    assert 'sentiment' in res.get_json()

def test_404_error(client):
    res = client.get('/halaman_palsu')
    assert res.status_code == 404