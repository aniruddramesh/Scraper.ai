from flask import Flask, request, jsonify
from scraper import scrape_page
from ai_processor import format_with_gemini
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Web Scraper AI API (Gemini) is running!"})

@app.route("/process", methods=["POST"])
def process_url():
    data = request.get_json(force=True)

    url = data.get("url")
    prompt = data.get("prompt")
    prefer_selenium = bool(data.get("prefer_selenium", True))

    if not url:
        return jsonify({"error": "missing 'url' in JSON body"}), 400
    if not prompt:
        return jsonify({"error": "missing 'prompt' in JSON body"}), 400

    try:
        scraped_text = scrape_page(url, prefer_selenium=prefer_selenium)
    except Exception as e:
        return jsonify({"error": "scraping_failed", "details": str(e)}), 500

    try:
        ai_output = format_with_gemini(scraped_text, prompt)
    except Exception as e:
        return jsonify({"error": "ai_failed", "details": str(e)}), 500

    return jsonify({
        "url": url,
        "prompt": prompt,
        "result": ai_output
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
