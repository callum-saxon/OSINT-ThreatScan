import requests
import logging

logging.basicConfig(level=logging.INFO)

def scrape_reddit_subreddit(subreddit="news", limit=5):

    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    headers = {'User-agent': 'MyOSINTAgent'}
    response = requests.get(url, headers=headers)

    posts_data = []
    if response.status_code == 200:
        data = response.json()
        children = data.get('data', {}).get('children', [])
        for post in children:
            post_info = post['data']
            title = post_info.get('title', "")
            content = post_info.get('selftext', "")
            posts_data.append({
                "source": f"reddit/{subreddit}",
                "title": title,
                "content": content
            })
    else:
        logging.error(f"Reddit scrape failed for /r/{subreddit}, code={response.status_code}")

    return posts_data
