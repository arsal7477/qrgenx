import pytest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert b"healthy" in response.data

def test_qr_generation(client):
    test_data = {"data": "https://example.com"}
    response = client.post('/generate', json=test_data)
    assert response.status_code == 200
    assert response.mimetype == 'image/png'

def test_missing_data(client):
    response = client.post('/generate', json={})
    assert response.status_code == 400
    assert b"Missing data" in response.data
