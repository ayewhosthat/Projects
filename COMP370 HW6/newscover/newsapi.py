import requests
from datetime import datetime, timedelta
NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
# defining global base url which we query and then filter the results based on the parameters given to the function

def fetch_latest_news(api_key, news_keywords, lookback_days=10):
    if not news_keywords:
        # case: news_keywords is None
        raise ValueError("Empty news_keywords list. Please provide at least one keyword when querying for articles")
    
    if any(not(keyword.isalpha()) for keyword in news_keywords):
        # we use a comprehension and check whether each keyword is fully alphabetic
        raise ValueError("Keywords cannot contain special characters")

    # default 10 lookback days
    stop = datetime.now()
    start = stop - timedelta(days=lookback_days)

    # must format dates correctly to be in YYYY-MM-DD format
    stop_format, start_format = stop.strftime("%Y-%m-%dT%H:%M:%SZ"), start.strftime("%Y-%m-%dT%H:%M:%SZ")
    # here it is important to format both start and stop in terms of the time that we want to parse so that there is no
    # discrepancy
    # set query parameters when making request
    query_parameters = {
        "apiKey": api_key, # parameter
        "q": ' AND '.join(news_keywords),
        "language": "en",
        "from": start_format,
        "to": stop_format,
        "sortBy": "publishedAt"
    }

    info = requests.get(NEWS_API_BASE_URL, params=query_parameters)

    if info.status_code == 200:
        news_articles = info.json()["articles"]
        return news_articles
    else:
        # If the request was not successful, raise an exception
        info.raise_for_status()

news_articles = fetch_latest_news(api_key='7ef2016e43554bb984ae1da0b1eaba9e', news_keywords=[], lookback_days=31)
print(news_articles)
print(len(news_articles))