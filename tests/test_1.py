import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import pytest

@pytest.fixture
def client():
    """Fixture to set up a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the root route ('/') for a successful response."""
    response = client.get('/')
    assert response.status_code == 200
