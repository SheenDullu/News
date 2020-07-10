# from application import db
from datetime import datetime

import pymongo
from bson import ObjectId
from pymongo.errors import PyMongoError


def one_insert_in_articles(data):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["articles"]
    insert = col.insert_one(data)
    print("Insert Status: ", insert.acknowledged)


def update_one_in_articles(article):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["articles"]
    col.delete_one({'url': article['url']})
    insert = col.insert_one(article)
    print("updated: ", article['url'])


def bulk_insert_in_articles(articles):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["articles"]
    try:
        col.insert_many(articles, ordered=False)
    except pymongo.errors.OperationFailure as e:
        print(e.code)
        print(e.details)
    print("Inserted")


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
        if col.find_one({'url': new_url}) is not None:
            continue
        select = {"url": old_url}
        new_values = {"$set": {"url": new_url}}
        col.update_one(select, new_values)
        print("Updated", old_url, "to", new_url)


def update_text_in_url(url, text):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    select = {"url": url}
    new_values = {"$set": {"content": text}}
    col.update_one(select, new_values)


def delete_urls_to_crawl(delete_urls):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    for url in delete_urls:
        select = {'url': url}
        delete = col.delete_one(select)
        print("Deleted ", delete.acknowledged, url)


def feeds_urls_to_crawl(list_feeds):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["urls_to_crawl"]
    try:
        col.insert_many(list_feeds, ordered=False)
    except pymongo.errors.OperationFailure as e:
        print(e.details)
    print("Inserted ")


def delete_url(id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["article"]
    data = {
        '_id': id
    }
    delete = col.delete_one(ObjectId(id))
    print(delete.acknowledged)


if __name__ == '__main__':
    in_topic(3, "entertainment")
