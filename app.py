from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Set this in your environment

@app.route("/get_top_headlines", methods=["POST"])
def get_top_headlines():
    data = request.json
    topic = data.get("topic", "general")
    country = data.get("country", "us")

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category={topic}&country={country}&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    response = requests.get(url)
    print(f"📦 NewsAPI status code: {response.status_code}")
    print(f"📝 Raw response: {response.json()}")

    articles = response.json().get("articles", [])[:3]  # Top 3 headlines

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