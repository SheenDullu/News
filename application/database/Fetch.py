import pymongo


def call_database():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    return db


def get_all_channel_urls():
    db = call_database()
    col = db["channel"]
    select = {
        "_id": 0,
        "channel_id": 1,
        "url": 1
        # "name": 1
    }
    return col.find({}, select)


def get_class_for_channel(channel):
    db = call_database()
    col = db["article_html"]
    select = {
        "_id": 0,
        # "channel_id": 1,
        "class": 1
    }
    return col.find({"channel_id": channel}, select)


def get_all_channel_name_id():
    db = call_database()
    col = db["channel"]
    select = {
        "_id": 0,
        "channel_id": 1,
        # "url": 1,
        "name": 1
    }
    return col.find({}, select)


def get_all_seed_urls():
    db = call_database()
    col = db["seed_urls"]
    select = {
        "_id": 0,
        "url": 1,
        "topic": 1,
        "channel": 1
    }
    return col.find({}, select)


def all_unvisited_urls():
    db = call_database()
    col = db["urls_to_crawl"]
    condition = {
        'visited': False
    }
    return col.find(condition)


def get_level_urls_to_crawl(query=None):
    db = call_database()
    col = db["urls_to_crawl"]
    if query is None:
        query = 1
    condition = {
        'page_depth': query,
        'visited': False
    }
    select = {
        "_id": 0,
        "url": 1,
        "channel_id": 1
    }
    return col.find(condition, select)


def from_articles(url):
    db = call_database()
    col = db["articles"]

    condition = {
        'url': url
    }
    fetch = col.find_one(condition)
    return fetch


def from_topic(name):
    db = call_database()
    col = db["topic"]

    condition = {
        'name': name
    }
    fetch = col.find_one(condition)
    return fetch['_id']


# def from_topic():
#     client = pymongo.MongoClient("mongodb://localhost:27017")
#     db = client["News"]
#     col = db["topic"]
#     fetch = col.find()
#     return fetch


if __name__ == '__main__':
    # print(from_articles('https://www.cnn.com/2020/06/21/politics/trump-future-rallies/index.html'))
    print(from_topic('politics'))