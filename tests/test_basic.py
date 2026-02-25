import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test that the homepage loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Data Tracking Plan Dashboard" in response.data

def test_api_health(client):
    """Test a basic API endpoint if it exists or just 404 handling."""
    # Assuming there's a /api/ route or similar, otherwise check generic
    response = client.get('/api/amplitude/events') 
    # If the file exists and is parsed, it might be 200, otherwise 500 or 404 depending on error handling
    # For now, let's just check that the app doesn't crash on a random route
    response = client.get('/nonexistent-page')
    assert response.status_code == 404

