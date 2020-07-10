from datetime import datetime
import pymongo


def call_database():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    return db


def find_in_seed_urls(channel_id, topic_id, url):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["News"]
    col = db["seed_urls"]
    condition = {
        'channel': channel_id,
        'topic': topic_id,
        'url': url
    }
    find = col.find_one(condition)
    print("Found Status: ", find)
    return find


def one_insert_in_seed_urls(channel_id, topic_id, url):
    db = call_database()
    col = db["seed_urls"]

    data = {
        'channel_id': channel_id,
        'topic_id': topic_id,
        'url': url,
        'created_at': datetime.utcnow()
    }
    insert = col.insert_one(data)
    print("Insert Status: ", insert.acknowledged)


def one_insert_in_channel(name, url):
    db = call_database()
    col = db["channel"]

    data = {
        'channel_id': col.count_documents(filter={}) + 1,
        'name': name.upper(),
        'source_url': url,
        'created_at': datetime.now()
    }
    try:
        insert = col.insert_one(data)
    except pymongo.errors.OperationFailure as e:
        print(e.code)
        print(e.details)
    print("Insert Status for ", url, " : ", insert.acknowledged)


def find_channel(name):
    db = call_database()
    col = db["channel"]
    condition = {
        'name': name.upper()
    }
    select = {
        '_id': 0,
        'channel_id': 1
    }
    find = col.find_one(condition, select)
    print("Found Status: ", find)
    return find


def one_insert_in_topic(name):
    db = call_database()
    col = db["topics"]

    data = {
        'topic_id': col.count_documents(filter={}) + 1,
        'name': name.upper()
    }
    try:
        insert = col.insert_one(data)
    except pymongo.errors.OperationFailure as e:
        print(e.code)
        print(e.details)
    print("Insert Status for ", name, " : ", insert.acknowledged)


def find_topic(name):
    db = call_database()
    col = db["topics"]
    condition = {
        'name': name.upper()
    }
    select = {
        '_id': 0,
        'topic_id': 1
    }
    find = col.find_one(condition, select)
    print("Found Status: ", find)
    return find


def find_insert_in_databse(channel_name, channel_source, topic_name, url):
    channel = find_channel(channel_name)
    if channel is not None:
        channel_id = channel['channel_id']
    else:
        one_insert_in_channel(channel_name, channel_source)
        channel = find_channel(channel_name)
        channel_id = channel['channel_id']

    topic = find_topic(topic_name)
    if topic is not None:
        topic_id = topic['topic_id']
    else:
        one_insert_in_topic(topic_name)
        topic = find_topic(topic_name)
        topic_id = topic['topic_id']

    seed_urls = find_in_seed_urls(channel_id, topic_id, url)
    if seed_urls is not None:
        print('already in database')
    else:
        one_insert_in_seed_urls(channel_id, topic_id, url)


if __name__ == '__main__':
    find_insert_in_databse('hindustantimes', 'www.hindustantimes.com', 'health and fitness',
                           'https://www.hindustantimes.com/rss/health-fitness/rssfeed.xml')
