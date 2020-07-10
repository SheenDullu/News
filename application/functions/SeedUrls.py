import datetime
import pytz
from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from application.database.Fetch import *
from application.database.Insert import *
from application.functions.Utilities import check_url_standard


utc = pytz.UTC


def fill_urls_to_crawl_dict(channel, url, title, topic, published_date, description, page_depth):
    if published_date is not None:
        published_date = parse(published_date)
        published_date = published_date.replace(tzinfo=utc)
    data = {
        "url": url.strip(),
        "published_date": published_date,
        "channel_id": channel,
        "topic_id": topic,
        "title": title,
        "description": description,
        "page_depth": page_depth,
        "visited": False
    }
    return data


def rss_cnn_crawler(channel, feeds, topic, conf):
    list_feeds = []
    for feed in feeds:
        url = feed.guid.text.strip()
        if not check_url_standard(url, conf, channel):
            continue
        date = feed.pubDate
        if date is not None:
            date = date.text
        list_feeds.append(fill_urls_to_crawl_dict(channel, url, feed.title.text, topic, date,
                                    feed.description.text.split('<')[0], 1))
    return list_feeds


def rss_ht_crawler(channel, feeds, topic, conf):
    list_feeds = []
    for feed in feeds:
        url = feed.guid.text.strip()
        if not check_url_standard(url, conf, channel):
            continue
        date = feed.pubDate
        if date is not None:
            date = date.text
        description = feed.description.text
        list_feeds.append(fill_urls_to_crawl_dict(channel, url, feed.title.text, topic, date,
                                                  description, 1))
    return list_feeds


def rss_wion_crawler(channel, feeds, topic, conf):
    list_feeds = []
    for feed in feeds:
        url = feed.guid.text.strip()
        if not check_url_standard(url, conf, channel):
            continue
        date = feed.pubDate
        if date is not None:
            date = date.text
        description = feed.description.text
        list_feeds.append(fill_urls_to_crawl_dict(channel, url, feed.title.text, topic, date,
                                                  description, 1))
    return list_feeds


def crawl_seed_urls():
    print("Crawling Seed Urls Started")
    list_urls = get_all_seed_urls()
    conf = ConfigParser()
    conf.read('news_config.ini')
    for item in list_urls:
        content = requests.get(item['url']).content
        soup = BeautifulSoup(content, 'xml')
        feeds = soup.find_all('item')
        channel_id = item['channel_id']
        topic = item['topic_id']
        if channel_id == 1:
            list_feeds = rss_cnn_crawler(channel_id, feeds, topic, conf)
        else:
            list_feeds = rss_ht_crawler(channel_id, feeds, topic, conf)
        # elif channel_id == 3:
        #     list_feeds = rss_wion_crawler(channel_id, feeds, topic, conf)
        if len(list_feeds) != 0:
            feeds_urls_to_crawl(list_feeds)
    print("Crawling seed urls completed")


if __name__ == '__main__':
    crawl_seed_urls()




