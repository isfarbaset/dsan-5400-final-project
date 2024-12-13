from src.final_prj_5400.ner import extract_entities

def test_extract_entities():
    """Test named entity extraction using spaCy."""
    text = "Apple is headquartered in Cupertino."
    entities = extract_entities(text)
    assert len(entities) > 0
    assert entities[0]["text"] == "Apple"
    assert entities[0]["label"] == "ORG"
    assert entities[1]["text"] == "Cupertino"
    assert entities[1]["label"] == "GPE"