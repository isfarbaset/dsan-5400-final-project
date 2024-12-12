import sys
import os

# Add the parent directory to the system path for module imports.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
import pytest

@pytest.fixture
def client():
    """
    Fixture to set up a test client for the Flask app.

    This fixture initializes a test client for the Flask application,
    providing a context for testing endpoints without running the server.
    """
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """
    Test the root route ('/') for a successful response.

    Ensures that the index route returns a status code of 200,
    indicating that the route is functioning as expected.
    """
    response = client.get('/')
    assert response.status_code == 200