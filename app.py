from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient
from src.final_prj_5400.ner import extract_entities
from src.final_prj_5400.final_prj_5400 import extract_relationships
import logging
from itertools import combinations

app = Flask(__name__, static_folder="static")

NEWS_API_KEY = '481b1e4a75874d2f9a23e3329031364c'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Route for root URL
@app.route('/')
def index():
    return render_template('index.html')

# Route for graph
@app.route('/graph')
def graph():
    return render_template('graph.html')

def transform_to_graph_data(entities, relationships):
    nodes = []
    links = []
    entity_to_index = {}

    # Create nodes
    for index, entity in enumerate(entities):
        nodes.append({"id": entity['text'], "group": entity['label']})
        entity_to_index[entity['text']] = index

    # Create links
    for rel in relationships:
        source = rel['entity1']['text']
        target = rel['entity2']['text']
        links.append({
            "source": entity_to_index[source],
            "target": entity_to_index[target],
            "value": 1  # You can adjust this value based on your needs
        })

    return {"nodes": nodes, "links": links}

# API route
@app.route('/api/fetch', methods=['GET'])
def fetch_articles():
    query = request.args.get('query', 'technology')
    logger.debug(f"Query received: {query}")
    try:
        articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        logger.debug(f"API Response received")

        if not articles or 'articles' not in articles:
            return jsonify({'error': 'No articles found'}), 404

        results = []
        all_entities = []
        all_relationships = []

        for article in articles.get('articles', []):
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}".strip()
            if text:
                try:
                    entities = extract_entities(text)
                    relationships = extract_relationships(entities)
                    
                    results.append({'entities': entities, 'relationships': relationships})
                    all_entities.extend(entities)
                    all_relationships.extend(relationships)
                except Exception as e:
                    logger.error(f"Error processing article: {str(e)}")
                    continue

        # Transform data to graph format
        graph_data = transform_to_graph_data(all_entities, all_relationships)

        if all_entities and all_relationships:
            try:
                er_diagram = generate_er_diagram(all_entities, all_relationships)
            except Exception as e:
                logger.error(f"Error generating diagram: {str(e)}")
                er_diagram = None
        else:
            er_diagram = None

        return jsonify({
            'results': results,
            'er_diagram': er_diagram,
            'graph_data': graph_data
        })

    except Exception as e:
        logger.error(f"Error in fetch_articles: {str(e)}")
        return jsonify({'error': str(e)}), 500

def extract_relationships(entities):
    # Placeholder: Ensure entities are in the expected format
    print(f"Entities received for relationship extraction: {entities}")

    relationships = []

    # Iterate over pairs of entities to infer relationships
    for entity1, entity2 in list(combinations(entities, 2)):
        # Infer relationships based on entity types
        types = [entity1['label'], entity2['label']]
        if 'ORG' in types and 'EVENT' in types: 
            relationship = "associated-with"
        elif types.count('ORG') == 2: 
            relationship = "competitor-to" 
        elif 'DATE' in types and 'EVENT' in types: 
            relationship = "happens-on"
        else:
            relationship = "related-to"

        # Append the relationship
        relationships.append({
            "entity1": entity1,
            "entity2": entity2,
            "relationship": relationship
        })

    print(f"Inferred relationships: {relationships}")
    return relationships

if __name__ == '__main__':
    app.run(debug=True)