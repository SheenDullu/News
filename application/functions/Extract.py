from newspaper import Article, ArticleException

from application.database.Fetch import *
from application.database.Insert import *


def crawl_for_articles():
    articles = []
    urls_to_update = []
    unvisited_articles = all_unvisited_urls()
    count = 0
    for item in unvisited_articles:
        url = item['url'].strip()
        data = from_articles(url)
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
        except ArticleException:
            continue
        if data is None:
            if item['page_depth'] is 1:
                articles.append(store_seed_article(item, article))
                urls_to_update.append(url.strip())
            else:
                articles.append(store_article_lib(url, article))
                urls_to_update.append(url.strip())
        else:
            if len(list(data)) is 1:
                update_article(data, article)
                urls_to_update.append(url.strip())

        count += 1
        print(count)
    if len(articles) == 0:
        return
    bulk_insert_in_articles(articles)
    update_urls_to_crawl(urls_to_update)
    print("crawl_for_articles completed")


def store_seed_article(item, article):
    dict_article = {
        'url': article.url,
        'title': article.title,
        'topic_via_channel': item['topic_via_channel'],
        'published_date': item['published_date'],
        'description': item['description'],
        'summary': article.summary,
        'authors': article.authors,
        'keywords': article.keywords,
        'last_crawled': datetime.now()
    }
    print("inserting seed ")
    # one_insert_in_articles(dict_article)
    return dict_article


def store_article_lib(url, article):
    dict_article = {
        'url': article.url,
        'title': article.title,
        'topic_via_channel': None,
        'published_date': article.publish_date,
        'description': None,
        'summary': article.summary,
        'authors': article.authors,
        'last_crawled': datetime.now(),
        'keywords': article.keywords
    }
    print("inserting lib ")
    # one_insert_in_articles(dict_article)
    return dict_article


def update_article(item, article):
    if item['published_date'] != article.publish_date:
        dict_article = {
            'title': article.title,
            'topic_via_channel': item['topic_via_channel'],
            'published_date': item['published_date'],
            'description': item['description'],
            'summary': article.summary,
            'authors': article.authors,
            'keywords': article.keywords,
            'last_crawled': datetime.now()
        }
        print("updating ")
        update_one_in_articles(item['url'], dict_article)


if __name__ == '__main__':
    crawl_for_articles()
