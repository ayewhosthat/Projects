import unittest
from datetime import datetime, timedelta
from .. newsapi import fetch_latest_news
API_key = '7ef2016e43554bb984ae1da0b1eaba9e'

#  test 1: fetch should fail when no keywords are provided
class Test_Keywords(unittest.TestCase):
    def test_no_keywords(self):
        with self.assertRaises(ValueError):
            fetch_latest_news(api_key=API_key, news_keywords=[])
            # raise ValueError since keywords is empty

    def test_with_keywords(self):
        news_keywords = ['McGill', 'sports']
        try:
            fetch_latest_news(api_key=API_key, news_keywords=news_keywords)
        except Exception as e:
            self.fail(f"fetch_latest_news raised an exception: {e}")
            # the test fails if an exception is thrown, so if no exception is thrown, then the test is considered a success

# test 2: published range
class Test_Published_Range(unittest.TestCase):
    def test_within_range(self):
        curr = datetime.now()
        lookback_days = 5
        news_keywords=['McGill', 'tuition']
        start = curr - timedelta(days=lookback_days)
        results = fetch_latest_news(api_key=API_key, news_keywords=news_keywords, lookback_days=lookback_days)

        for article in results:
            publishDate = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            # parsing the publishedAt field from the article into a date object
            # it is important that we set the parse format equal to the formatting format, otherwise we would get 
            # discrepancies due to minutes, etc
            
            # now, we want to make sure that the difference between the published date and the current date does not
            # exceed lookback_days
            self.assertGreaterEqual(publishDate, start)

    def test_outside_range(self):
        current_date = datetime.now()
        lookback_days = 7
        start_date = current_date - timedelta(days=lookback_days + 1)
        news_keywords = ['McGill', 'tuition']
        # Fetch news articles and ensure none are older than the specified lookback period
        news_articles = fetch_latest_news(api_key=API_key, news_keywords=news_keywords, lookback_days=lookback_days)
        for article in news_articles:
            article_published_at = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            self.assertGreaterEqual(article_published_at, start_date)


# test 3: keyword validity
class Test_Keywords(unittest.TestCase):
    def test_valid_keywords(self):
        news_keywords = ['McGill', 'sports']
        try:
            fetch_latest_news(api_key=API_key, news_keywords=news_keywords)
        except Exception as e:
            self.fail(f"fetch_latest_news raised an exception: {e}")

    def test_invalid_keywords(self):
        news_keywords = ['M@Gill', '$port$']
        with self.assertRaises(ValueError):
            fetch_latest_news(api_key=API_key, news_keywords=news_keywords)

if __name__ == '__main__':
    unittest.main()