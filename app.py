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
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logging.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Route for root URL
@app.route('/')
def index():
    logger.info("Index route accessed")
    return render_template('index.html')

# Route for graph
@app.route('/graph')
def graph():
    logger.info("Graph route accessed")
    return render_template('graph.html')

def transform_to_graph_data(entities, relationships):
    logger.debug("Transforming entities and relationships into graph data")
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
            "value": 1
        })

    logger.debug("Graph data transformation completed")
    return {"nodes": nodes, "links": links}

# API route
@app.route('/api/fetch', methods=['GET'])
def fetch_articles():
    queries = request.args.get('query', '').split(' ') 
    query = request.args.get('query', 'technology')
    logger.info(f"Query received: {query}")

    try:
        all_articles = [] 
        for query in queries: 
            logger.debug(f"Fetching articles for query: {query}")
            api_response = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
            logger.debug("API response received")
            if not api_response or 'articles' not in api_response:
                logger.warning(f"No articles found for query: {query}")
                return jsonify({'error': 'No articles found'}), 404
            all_articles.extend(api_response.get('articles', []))

        results = []
        all_entities = []
        all_relationships = []

        for article in all_articles:
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}".strip()
            if text:
                logger.debug(f"Processing article: {title}")
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
                logger.info("Generating ER diagram")
                er_diagram = generate_er_diagram(all_entities, all_relationships)
            except Exception as e:
                logger.error(f"Error generating diagram: {str(e)}")
                er_diagram = None
        else:
            er_diagram = None

        return jsonify({
            'results': results,
            'entities': all_entities,
            'relationships': all_relationships,
            'er_diagram': er_diagram,
            'graph_data': graph_data
        })

    except Exception as e:
        logger.error(f"Error in fetch_articles: {str(e)}")
        return jsonify({'error': str(e)}), 500

def extract_relationships(entities):
    logger.debug(f"Extracting relationships from entities: {entities}")
    relationships = []

    # Iterate over pairs of entities to infer relationships
    for entity1, entity2 in list(combinations(entities, 2)):
        types = [entity1['label'], entity2['label']]
        if 'ORG' in types and 'EVENT' in types: 
            relationship = "associated-with"
        elif types.count('ORG') == 2: 
            relationship = "competitor-to" 
        elif 'DATE' in types and 'EVENT' in types: 
            relationship = "happens-on"
        else:
            relationship = "related-to"

        relationships.append({
            "entity1": entity1,
            "entity2": entity2,
            "relationship": relationship
        })

    logger.debug(f"Inferred relationships: {relationships}")
    return relationships

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
