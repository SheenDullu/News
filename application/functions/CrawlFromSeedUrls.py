from application.database.Fetch import *
from application.database.Insert import *
from application.functions.Utilities import get_canonical_link_and_ref


def crawling_to_depth(unique_urls, depth):
    print("DEPTH: ", depth)
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
        if page != feed['url'].strip():
            update_crawls_list[feed['url']] = page
            unique_urls.add(page)
        for url in ref:
            if url not in unique_urls:
                data = {
                    'url': url,
                    'channel_id': feed['channel_id'],
                    'visited': False,
                    'page_depth': depth + 1
                }
                page_urls.append(data)
                unique_urls.add(url)
    feeds_urls_to_crawl(page_urls)
    if len(update_crawls_list) is not 0:
        update_in_db_crawl_list(update_crawls_list)
    return unique_urls


def crawl_unvisited_seed_urls():
    print("crawling unvisited urls started")
    list_urls = list(get_level_urls_to_crawl())
    unique_urls = set(d['url'] for d in list_urls)
    depth = 1
    while depth < 3:
        unique_urls = crawling_to_depth(unique_urls, depth)
        depth += 1
    print("crawl_unvisited_seed_urls completed")


if __name__ == '__main__':
    crawl_unvisited_seed_urls()
