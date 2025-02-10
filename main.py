import logging
from flask import Flask, render_template

from scrapers.news_scraper import scrape_news_articles
from scrapers.reddit_scraper import scrape_reddit_subreddit
from scrapers.twitter_scraper import scrape_twitter_hashtag

from analysis.nlp_pipeline import analyze_text
from analysis.risk_scoring import compute_risk_score

from database.db_manager import init_db, save_document, get_latest_documents
from alerts.alert_system import send_discord_alert

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    """Render a basic dashboard of the latest items in the DB."""
    items = get_latest_documents(limit=10)
    return render_template("index.html", items=items)

@app.route("/run-scrapers")
def run_scrapers():
    """Manual endpoint to trigger scraping & analysis pipeline."""
    data_from_news = scrape_news_articles()
    data_from_reddit = scrape_reddit_subreddit(subreddit="worldnews", limit=3)
    data_from_twitter = scrape_twitter_hashtag("security", count=3)

    combined = data_from_news + data_from_reddit + data_from_twitter

    for entry in combined:
        content = entry.get("content", "")
        analysis_result = analyze_text(content)
        risk = compute_risk_score(analysis_result)

        entry["named_entities"] = analysis_result["named_entities"]
        entry["sentiment"] = analysis_result["sentiment"]
        entry["risk_score"] = risk

        save_document(entry)

        # If risk is high, send an alert
        if risk >= 50:
            subject = f"High-Risk Content (Score={risk})"
            body = f"Source: {entry.get('source')}\nTitle: {entry.get('title')}\nSnippet: {content[:200]}"
            send_discord_alert(subject, body)

    return "Scraping & Analysis Done!"

def main():
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
