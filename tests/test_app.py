import pytest
from flask import Flask
from app import app, transform_to_graph_data, extract_relationships
from src.final_prj_5400.ner import extract_entities

@pytest.fixture
def client():
    """Fixture to initialize the Flask test client."""
    app.testing = True
    client = app.test_client()
    return client

def test_index_route(client):
    """Test the index route renders successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data

def test_graph_route(client):
    """Test the graph route renders successfully."""
    response = client.get('/graph')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data

def test_transform_to_graph_data():
    """Test graph data transformation."""
    entities = [{'text': 'Apple', 'label': 'ORG'}, {'text': 'San Francisco', 'label': 'GPE'}]
    relationships = [
        {'entity1': {'text': 'Apple'}, 'entity2': {'text': 'San Francisco'}, 'relationship': 'located-in'}
    ]
    graph_data = transform_to_graph_data(entities, relationships)
    assert "nodes" in graph_data
    assert "links" in graph_data
    assert len(graph_data["nodes"]) == len(entities)
    assert len(graph_data["links"]) == len(relationships)

def test_extract_relationships():
    """Test relationship extraction."""
    entities = [{'text': 'Apple', 'label': 'ORG'}, {'text': 'iPhone 15 Launch', 'label': 'EVENT'}]
    relationships = extract_relationships(entities)
    assert len(relationships) == 1
    assert relationships[0]["relationship"] == "associated-with"