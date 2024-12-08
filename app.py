from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient
from src.final_prj_5400.ner import extract_entities
from src.final_prj_5400.final_prj_5400 import extract_relationships
import logging
from er_visualization import generate_er_diagram

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

# API route
@app.route('/api/fetch', methods=['GET'])
def fetch_articles():
    query = request.args.get('query', 'technology')
    logger.debug(f"Query received: {query}")
    try:
        articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        logger.debug(f"Full NewsAPI Response: {articles}")  # Log full response

        if not articles or 'articles' not in articles:
            logger.error("No articles found in NewsAPI response.")
            return jsonify({'error': 'No articles found'}), 404

        results = []
        all_entities = set()
        all_relationships = []

        for article in articles.get('articles', []):
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}".strip()
            if text:
                logger.debug(f"Processing text: {text[:100]}...")  # Log the first 100 characters
                try:
                    entities = extract_entities(text)
                    logger.debug(f"Extracted entities: {entities}")

                    # Convert entities to hashable type before updating the set
                    hashable_entities = {tuple(entity.items()) for entity in entities}
                    all_entities.update(hashable_entities)

                    relationships = extract_relationships(entities)
                    logger.debug(f"Extracted relationships: {relationships}")
                    all_relationships.extend(relationships)

                    results.append({'entities': entities, 'relationships': relationships})
                except Exception as extraction_error:
                    logger.error(f"Error extracting entities/relationships: {str(extraction_error)}")
                    results.append({'entities': [], 'relationships': []})

        try:
            # Convert hashable entities back to dictionaries for diagram generation
            entities_for_diagram = [dict(entity_tuple) for entity_tuple in all_entities]
            logger.debug(f"Entities for diagram: {entities_for_diagram}")
            logger.debug(f"Relationships for diagram: {all_relationships}")

            er_diagram = generate_er_diagram(entities_for_diagram, all_relationships)
            logger.debug(f"Generated ER Diagram: {er_diagram[:100]}...")  # Log first 100 chars of the diagram
        except Exception as er_error:
            logger.error(f"Failed to generate ER diagram: {str(er_error)}")
            return jsonify({'error': 'Failed to generate ER diagram.'}), 500

        return jsonify({'results': results, 'er_diagram': er_diagram})
    except Exception as e:
        logger.error(f"Error in fetch_articles: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while fetching articles. Please try again.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
