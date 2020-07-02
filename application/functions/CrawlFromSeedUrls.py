from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup

from application.database.Fetch import *
from application.database.Insert import *


def check_url_standard(url, conf, channel_id):
    if conf.get(str(channel_id), 'url_end') in url and url.split('/')[2] == conf.get(str(channel_id), 'source_url'):
        return True
    return False


def get_links_from(soup, channel_id):
    conf = ConfigParser()
    conf.read('news_config.ini')
    para = soup.find_all(class_=conf.get(str(channel_id), 'class'))
    links = set()
    for p in para:
        for a in p.find_all('a'):
            if check_url_standard(a['href'], conf, channel_id):
                links.add(a['href'].strip())
    return links


def get_canonical_link_and_ref(feed):
    content = requests.get(feed['url']).content
    soup = BeautifulSoup(content, 'lxml')
    para = soup.find('link', {'rel': 'canonical'})
    if para is None:
        return None, None
    return para['href'], get_links_from(soup, feed['channel_id'])


def crawling_to_depth(unique_urls, depth):
    update_crawls_list = {}
    feeds = list(get_level_urls_to_crawl(depth))
    page_urls = []
    count = 0
    for feed in feeds:
        count += 1
        print(count, " ", feed['url'])
        page, ref = get_canonical_link_and_ref(feed)
        if page is None:
            continue
        if page != feed['url']:
            update_crawls_list[feed['url']] = page
            unique_urls.add(page)
        for url in ref:
            if url not in unique_urls:
                data = {
                    'url': url,
                    'visited': False,
                    'page_depth': depth + 1,
                    'channel_id': feed['channel_id']
                }
                page_urls.append(data)
                unique_urls.add(url)
    in_urls_to_crawl_seed(page_urls)
    if len(update_crawls_list) is not 0:
        update_in_db_crawl_list(update_crawls_list)
    return unique_urls


def crawl_unvisited_seed_urls():
    print("crawling unvisited urls started")
    list_urls = list(get_level_urls_to_crawl())
    unique_urls = {d['url'] for d in list_urls}
    depth = 1
    while depth < 3:
        unique_urls = crawling_to_depth(unique_urls, depth)
        depth += 1
    print("crawl_unvisited_seed_urls completed")


if __name__ == '__main__':
    crawl_unvisited_seed_urls()
