from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

def extract_headlines(html):
    """Extracts headlines and URLs from the provided HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    headlines = []

    for article in soup.find_all("article"):
        title_tag = article.find("h2") or article.find("h3")
        if title_tag and title_tag.a:
            title = title_tag.get_text(strip=True)
            url = title_tag.a['href']
            headlines.append({"title": title, "url": url})

    return headlines

def clean_html(html):
    """Cleans the HTML content by removing unnecessary tags."""
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.decompose()
    return str(soup)

def format_data(headlines, source):
    """Formats the extracted headlines into a structured JSON format."""
    formatted_data = []
    for item in headlines:
        item["source"] = source
        item["article_date"] = datetime.now().strftime('%Y-%m-%d')
        formatted_data.append(item)
    return json.dumps(formatted_data, ensure_ascii=False)