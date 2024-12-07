from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient
from src.final_prj_5400.ner import extract_entities
from src.final_prj_5400.final_prj_5400 import extract_relationships

app = Flask(__name__, static_folder="static")

NEWS_API_KEY = '481b1e4a75874d2f9a23e3329031364c'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Route for root URL
@app.route('/')
def index():
    # Option 1: Return a simple message
    # return 'Welcome to the Entity Relationship Extraction App!' 

    # Option 2: Render the HTML template
    return render_template('index.html')

# Example API route
@app.route('/api/fetch', methods=['GET'])
def fetch_articles():
    query = request.args.get('query', 'technology')
    print(f"Query received: {query}")  # Debugging log
    try:
        articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy')
        print(f"API Response: {articles}")  # Debugging log

        results = []
        for article in articles.get('articles', []):
            text = article['title'] + ". " + article['description']
            entities = extract_entities(text)
            relationships = extract_relationships(entities)
            results.append({'entities': entities, 'relationships': relationships})

        return jsonify({'results': results})
    except Exception as e:
        print(f"Error: {e}")  # Debugging log
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)