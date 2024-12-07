def extract_relationships(entities):
    relationships = []
    for i in range(len(entities) - 1):
        relationships.append({
            'entity1': entities[i]['text'],
            'entity2': entities[i + 1]['text'],
            'relationship': 'related-to'
        })
    return relationships