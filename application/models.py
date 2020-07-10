import flask
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from application import db


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class Seed_urls(db.Document):
    channel_id = db.IntField()
    topic_id = db.IntField()
    url = db.StringField(max_length=100)
    created = db.DateTimeField(default=datetime.now)


class Topics(db.Document):
    topic_id = db.IntField(unique=True, required=True)
    name = db.StringField(unique=True, required=True)


class Urls_to_crawl(db.Document):
    url = db.StringField(max_length=500, unique=True, required=True)
    channel_id = channel_id = db.IntField()
    title = db.StringField(max_length=200)
    topic_id = db.IntField()
    published_date = db.DateTimeField(default=datetime.now)
    description = db.StringField(max_length=500)
    visited = db.BooleanField(default=False)
    page_depth = db.IntField(required=True)


class Articles(db.Document):
    url = db.StringField(max_length=100, unique=True, required=True)
    title = db.StringField(max_length=200)
    newspaper_title = db.StringField(max_length=200)
    topic_id = db.IntField()
    channel_id = db.IntField()
    published_date = db.DateTimeField(default=datetime.now)
    newspaper_published_date = db.DateTimeField(default=datetime.now)
    description = db.StringField()
    newspaper_topic = db.StringField(max_length=50)
    newspaper_summary = db.StringField()
    newspaper_text = db.StringField()
    newspaper_authors = db.ListField(db.StringField(max_length=20))
    last_crawled = db.DateTimeField(default=datetime.now)
    newspaper_tags = db.ListField(db.StringField(max_length=20))
    newspaper_keywords = db.ListField(db.StringField(max_length=20))


class Following(db.Document):
    user_id = db.IntField()
    topic_id = db.IntField()
