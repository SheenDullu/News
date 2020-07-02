import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'~\xd97\x173\xe9\x16&\x87#\x99\x10\x9a7\x17\xa3'

    MONGODB_SETTINGS = { 'db' : 'News' }


