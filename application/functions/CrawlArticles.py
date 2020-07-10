from newspaper import Article, ArticleException

from application.database.Fetch import *
from application.database.Insert import *
import datetime
import pytz


utc = pytz.UTC


def parse_data(article, news_feed):
    article['newspaper_title'] = news_feed.title
    date = news_feed.publish_date
    if date is not None:
        date.replace(tzinfo=utc)
    article['newspaper_published_date'] = date
    article['newspaper_topic'] = news_feed.meta_data['section']
    article['newspaper_text'] = news_feed.text
    article['newspaper_summary'] = news_feed.summary
    article['newspaper_authors'] = list(news_feed.authors)
    article['newspaper_keywords'] = list(news_feed.keywords)
    article['newspaper_tags'] = list(news_feed.tags)
    article['last_crawled'] = datetime.datetime.now().replace(tzinfo=utc)
    return article


def crawl_for_articles():
    print("crawl_for_articles started")
    articles = list()
    unvisited_articles = all_unvisited_urls()
    count = 0
    delete_urls = set()
    for article in unvisited_articles:
        url = article['url'].strip()
        count += 1
        print(count, " ", url)
        data = from_articles(url)
        try:
            news_feed = Article(url)
            news_feed.download()
            news_feed.parse()
            news_feed.nlp()
            if 'type' in news_feed.meta_data['og'] and news_feed.meta_data['og']['type'] != 'article':
                print('delete ', url)
                delete_urls.add(url)
                continue
        except ArticleException as e:
            print("error occurred ", e)
            continue

        if data.count() == 0:
            articles.append(parse_data(article, news_feed))
            delete_urls.add(url)
        else:
            if data.count() == 1:
                update_article(data, news_feed, article)
                delete_urls.add(url)

    if len(articles) == 0:
        print("No article found. crawl_for_articles completed")
        return
    bulk_insert_in_articles(articles)
    delete_urls_to_crawl(list(delete_urls))
    print("crawl_for_articles completed")
    return


def update_article(data, news_feed, article):
    print('Update:')
    last_crawled = data[0]['last_crawled'].replace(tzinfo=utc)
    news_mod_date = news_feed.publish_date.replace(tzinfo=utc) if news_feed.publish_date is not None else None
    if news_mod_date is not None and last_crawled < news_mod_date:
        article['newspaper_title'] = news_feed.title
        article['newspaper_text'] = news_feed.text
        article['newspaper_summary'] = news_feed.summary
        article['newspaper_authors'] = list(news_feed.authors)
        article['newspaper_keywords'] = list(news_feed.keywords)
        article['newspaper_tags'] = list(news_feed.tags)
        article['newspaper_last_modified'] = news_mod_date
        article['last_crawled'] = datetime.now()
        update_one_in_articles(article)


if __name__ == '__main__':
    crawl_for_articles()
    # print("oops")
