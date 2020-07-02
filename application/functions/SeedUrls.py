import datetime

import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from application.database.Fetch import *
from application.database.Insert import *


def process_channel_info():
    channel = {}
    channel_info = list(get_all_channel_name_id())
    for info in channel_info:
        channel[info['channel_id']] = info['name']
    return channel


def fill_urls_to_crawl_dict(channel, url, topic, published_date, description, page_depth):
    if published_date is not None:
        published_date = parse(published_date)
        datetime.combine(datetime.date(published_date), datetime.time(published_date))
    data = {
        "channel_id": channel,
        "url": url.strip(),
        "topic_via_channel": topic,
        "published_date": published_date,
        "description": description,
        "page_depth": page_depth,
        "visited": False
    }
    return data


def rss_cnn_crawler(channel, feeds, topic):
    list_feeds = []
    for feed in feeds:
        date = feed.pubDate
        if date is not None:
            date = date.text
        list_feeds.append(
            fill_urls_to_crawl_dict(channel, feed.origLink.text, topic, date, feed.description.text.split('<')[0], 1))
    return list_feeds


def rss_ht_crawler(channel, feeds, topic):
    list_feeds = []
    for feed in feeds:
        date = feed.pubDate
        if date is not None:
            date = date.text
        list_feeds.append(
            fill_urls_to_crawl_dict(channel, feed.guid.text, topic, date, feed.description.text, 1))
    return list_feeds


def rss_toi_crawler(channel, feeds, topic):
    list_feeds = []
    for feed in feeds:
        date = feed.pubDate
        if date is not None:
            date = date.text
        description = feed.description.text
        if '</a>' in description:
            list_a = description.split('</a>')
            description = list_a[len(list_a) - 1]
        list_feeds.append(fill_urls_to_crawl_dict(channel, feed.guid.text, topic, date, description, 1))
    return list_feeds


def crawl_seed_urls():
    print("Crawling Seed Urls Started")
    list_urls = get_all_seed_urls()
    for item in list_urls:
        content = requests.get(item['url']).content
        soup = BeautifulSoup(content, 'xml')
        feeds = soup.find_all('item')
        channel_id = item['channel']
        topic = item['topic']
        if channel_id == 1:
            list_feeds = rss_cnn_crawler(channel_id, feeds, topic)
        if channel_id == 2:
            list_feeds = rss_ht_crawler(channel_id, feeds, topic)

        in_urls_to_crawl_seed(list_feeds)
    print("Crawling seed urls completed")


# if __name__ == '__main__':
#     crawl_seed_urls()




