from flask import Flask, request, jsonify
from utils.data_ingestion import scrape_article
from utils.processing import analyze_sentiment
import os

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Hello, Render!"

# Analyze endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "Missing 'url' in request body"}), 400

        # Scrape the article and perform sentiment analysis
        article_text = scrape_article(url)
        sentiment = analyze_sentiment(article_text)

        return jsonify({"url": url, "sentiment": sentiment})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
