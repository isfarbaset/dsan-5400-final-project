from flask import Flask, render_template, request, jsonify
from src.final_prj_5400.ner import extract_entities
from src.final_prj_5400.final_prj_5400 import extract_relationships

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def extract():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']
    entities = extract_entities(text)
    relationships = extract_relationships(entities)

    return jsonify({'entities': entities, 'relationships': relationships})

if __name__ == '__main__':
    app.run(debug=True)