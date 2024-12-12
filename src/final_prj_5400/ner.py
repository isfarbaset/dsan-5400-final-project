import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extracts named entities from a given text using spaCy.

    This function uses a pre-loaded spaCy model to analyze the input text
    and extract named entities. Each entity is represented as a dictionary
    containing the entity's text and its label.

    Args:
        text (str): The input text from which to extract named entities.

    Returns:
        list of dict: A list of dictionaries, where each dictionary represents
                      an entity with the following keys:
                      - 'text': The string of the entity as it appears in the input text.
                      - 'label': The label assigned to the entity (e.g., "PERSON", "ORG").

    Example:
        text = "Apple is looking to hire new employees in San Francisco."
        
        entities = extract_entities(text)

        Output:
        [
            {'text': 'Apple', 'label': 'ORG'},
            {'text': 'San Francisco', 'label': 'GPE'}
        ]
    """
    doc = nlp(text)
    entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
    return entities