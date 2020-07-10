from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup


def check_url_standard(url, conf, channel_id):
    # if conf.get(str(channel_id), 'url_end') in url and url.split('/')[2] == conf.get(str(channel_id), 'source_url'):
    if len(url.split('/')) >= 3 and url.split('/')[2] == conf.get(str(channel_id), 'source_url'):
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
    content = requests.get(feed['url'].strip()).content
    soup = BeautifulSoup(content, 'lxml')
    para = soup.find('link', {'rel': 'canonical'})
    if para is None:
        return None, None
    links = get_links_from(soup, feed['channel_id'])
    return para['href'].strip(), links


def get_canonical_link_if_any(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')
    para = soup.find('link', {'rel': 'canonical'})
    if para is None:
        return None
    return para['href'].strip()
