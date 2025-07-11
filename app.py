from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Fallback keyword → topic mapping
TOPIC_MAP = {
    "amazon": "business",
    "prime day": "business",
    "oscars": "entertainment",
    "movies": "entertainment",
    "football": "sports",
    "cricket": "sports",
    "world cup": "sports",
    "nfl": "sports",
    "nba": "sports",
    "google": "technology",
    "apple": "technology",
    "microsoft": "technology",
    "ai": "technology",
    "covid": "health",
    "vaccine": "health",
    "nasa": "science",
    "spacex": "science"
}

def infer_topic_from_text(user_input: str):
    user_input = user_input.lower()
    for keyword, topic in TOPIC_MAP.items():
        if keyword in user_input:
            return topic
    return "general"

@app.route("/get_top_headlines", methods=["POST"])
def get_top_headlines():
    data = request.json
    topic = data.get("topic")
    country = data.get("country", "us")
    user_query = data.get("query", "")  # optional field

    # If topic not provided, infer from query
    if not topic:
        topic = infer_topic_from_text(user_query)

    print(f"🔍 Topic: {topic} | Country: {country}")

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category={topic}&country={country}&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    print(f"📡 NewsAPI Status: {response.status_code}")
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch headlines"}), 500

    articles = response.json().get("articles", [])[:3]

    headlines = [
        {
            "title": a["title"],
            "description": a["description"],
            "url": a["url"]
        } for a in articles
    ]
    return jsonify(headlines)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)