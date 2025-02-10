import logging

logging.basicConfig(level=logging.INFO)

def scrape_twitter_hashtag(hashtag="news", count=5):

    tweets_data = []
    for i in range(count):
        tweets_data.append({
            "source": "twitter",
            "author": f"User_{i}",
            "content": f"Mock tweet about #{hashtag} number {i}"
        })
    return tweets_data
