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
            'er_diagram': er_diagram
        })

    except Exception as e:
        logger.error(f"Error in fetch_articles: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
