from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api
from application.functions.SeedUrls import *
from application.functions.CrawlFromSeedUrls import *
from application.functions.CrawlArticles import *

api = Api()

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
api.init_app(app)

# crawl_seed_urls()
# crawl_unvisited_seed_urls()
# crawl_for_articles()

from application import routes
