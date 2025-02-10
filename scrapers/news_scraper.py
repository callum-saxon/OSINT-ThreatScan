import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

def scrape_news_articles():
    
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    articles_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h3')
        for h in headlines[:5]:
            title = h.get_text().strip()
            link = h.find('a')
            if not link or not link.get('href'):
                continue

            article_url = "https://www.bbc.com" + link.get('href')
            content = get_article_content(article_url)

            articles_data.append({
                "source": "BBC",
                "title": title,
                "url": article_url,
                "content": content
            })
    else:
        logging.error(f"Failed to scrape {url}, status code: {response.status_code}")

    return articles_data

def get_article_content(url):
    """
    Helper to grab the raw text from the article.
    """
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            page_soup = BeautifulSoup(resp.text, 'html.parser')
            paragraphs = page_soup.find_all('p')
            content = " ".join(p.get_text().strip() for p in paragraphs)
            return content
    except Exception as e:
        logging.error(f"Error scraping article content: {e}")
    return ""
