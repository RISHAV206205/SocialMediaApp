import requests
import os
from datetime import datetime

# Free News API configuration (no API key required)
SAURAV_NEWS_BASE = "https://saurav.tech/NewsAPI"

def get_news_by_category(category):
    """Fetch news from various APIs based on category"""
    
    if category == "general":
        return get_general_news()
    elif category == "sports":
        return get_sports_news()
    elif category == "technology":
        return get_tech_news()
    elif category == "finance":
        return get_financial_news()
    elif category == "entertainment":
        return get_entertainment_news()
    else:
        return get_general_news()

def get_general_news():
    """Fetch general news from free API"""
    try:
        url = f"{SAURAV_NEWS_BASE}/top-headlines/category/general/us.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return format_news_data(data.get("articles", []), "General News")
        else:
            return get_fallback_news("General")
    except Exception as e:
        return get_fallback_news("General")

def get_sports_news():
    """Fetch sports news from free API"""
    try:
        url = f"{SAURAV_NEWS_BASE}/top-headlines/category/sports/us.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return format_news_data(data.get("articles", []), "Sports News")
        else:
            return get_fallback_news("Sports")
    except Exception as e:
        return get_fallback_news("Sports")

def get_tech_news():
    """Fetch technology news from free API"""
    try:
        url = f"{SAURAV_NEWS_BASE}/top-headlines/category/technology/us.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return format_news_data(data.get("articles", []), "Technology News")
        else:
            return get_fallback_news("Technology")
    except Exception as e:
        return get_fallback_news("Technology")

def get_financial_news():
    """Fetch financial news from free API"""
    try:
        url = f"{SAURAV_NEWS_BASE}/top-headlines/category/business/us.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return format_news_data(data.get("articles", []), "Financial News")
        else:
            return get_fallback_news("Financial")
    except Exception as e:
        return get_fallback_news("Financial")

def get_entertainment_news():
    """Fetch entertainment news from free API"""
    try:
        url = f"{SAURAV_NEWS_BASE}/top-headlines/category/entertainment/us.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return format_news_data(data.get("articles", []), "Entertainment News")
        else:
            return get_fallback_news("Entertainment")
    except Exception as e:
        return get_fallback_news("Entertainment")


def format_news_data(articles, category_title):
    """Format news articles for display"""
    formatted_articles = []
    
    for article in articles:
        if article.get("title") and article.get("description"):
            formatted_articles.append({
                "title": article["title"],
                "description": article["description"],
                "url": article.get("url", "#"),
                "urlToImage": article.get("urlToImage"),
                "publishedAt": article.get("publishedAt"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "author": article.get("author")
            })
    
    return {
        "category": category_title,
        "articles": formatted_articles,
        "total_results": len(formatted_articles),
        "last_updated": datetime.now().isoformat()
    }

def get_fallback_news(category):
    """Return fallback news when APIs fail"""
    return {
        "category": f"{category} News",
        "articles": [],
        "total_results": 0,
        "last_updated": datetime.now().isoformat(),
        "error": "News service temporarily unavailable. Please check your API configuration."
    }
