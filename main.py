import os
from flask import Flask, request, jsonify
from utils.data_ingestion import scrape_article
from utils.processing import analyze_sentiment

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Render!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Analyze endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Scrape the article
    article = scrape_article(url)

    # Analyze the sentiment of the article content
    sentiment = analyze_sentiment(article.get('content', ''))

    # Return the results
    return jsonify({
        "title": article.get('title', 'No Title'),
        "sentiment": sentiment
    })

if __name__ == '__main__':
    app.run(debug=True)
