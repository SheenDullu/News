# from application import db
from datetime import datetime
import pymongo


def one_insert_in_articles(data):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["articles"]
    insert = col.insert_one(data)
    # print("Insert Status: ", insert.acknowledged)


def update_one_in_articles(url, dict_article):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["articles"]
    newvalues = {"$set": dict_article}
    update = col.update_one({'url': url}, newvalues)
    # print("Updated article ", url)


def bulk_insert_in_articles(articles):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["articles"]
    before = col.count_documents({})
    insert = col.insert_many(articles)
    after = col.count_documents({})
    print("Number of Inserts: ", (after-before))
    # return insert.inserted_ids


def in_seed_urls(channel, url, channel_url, topic, frequency):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["seed_urls"]

    data = {
        "channel_id": channel,
        "url": url,
        "channel_url": channel_url,
        "topic": topic,
        "created": datetime.now(),
        "frequency": frequency
    }
    insert = col.insert_one(data)
    print("Insert Status:", insert.acknowledged)


def in_topic(id, name):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["topic"]
    data = {
        "_id": id,
        "name": name
    }
    insert = col.insert_one(data)
    print("Insert Status:", insert.acknowledged)


def update_in_db_crawl_list(update_crawls_list):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    for old_url, new_url in update_crawls_list.items():
        select = {"url": old_url}
        new_values = {"$set": {"url": new_url}}
        col.update_one(select, new_values)
        print("Updated", old_url, "to", new_url)


def update_urls_to_crawl(update_urls_list):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    for url in update_urls_list:
        select = {"url": url}
        new_values = {"$set": {"visited": True}}
        col.update_one(select, new_values)
    print("Updated value to True")


def in_urls_to_crawl_seed(list_data):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    col.insert_many(list_data)
    count = col.count_documents({})
    print("New Count of Urls: ", count)


def in_urls_to_crawl(urls):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    col.insert_many(urls)
    count = col.count_documents({})
    print("New Count: ", count)


if __name__ == '__main__':
    in_topic(3, "entertainment")
