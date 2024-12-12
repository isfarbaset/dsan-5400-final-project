def extract_relationships(entities):
    """
    Extracts relationships between consecutive entities.

    This function takes a list of entities, and for each consecutive pair of entities,
    it creates a relationship dictionary. The relationship is defined as "related-to"
    by default. The output is a list of such relationship dictionaries.

    Args:
        entities (list of dict): A list of entities where each entity is represented
                                 as a dictionary with a 'text' key containing the entity name.

    Returns:
        list of dict: A list of relationships, where each relationship is represented as
                      a dictionary with the following keys:
                      - 'entity1': The text of the first entity in the pair.
                      - 'entity2': The text of the second entity in the pair.
                      - 'relationship': The relationship type (default is "related-to").

    Example:
        entities = [
            {'text': 'Alice'},
            {'text': 'Bob'},
            {'text': 'Charlie'}
        ]

        relationships = extract_relationships(entities)

        Output:
        [
            {'entity1': 'Alice', 'entity2': 'Bob', 'relationship': 'related-to'},
            {'entity1': 'Bob', 'entity2': 'Charlie', 'relationship': 'related-to'}
        ]
    """
    relationships = []
    for i in range(len(entities) - 1):
        relationships.append({
            'entity1': entities[i]['text'],
            'entity2': entities[i + 1]['text'],
            'relationship': 'related-to'
        })
    return relationships