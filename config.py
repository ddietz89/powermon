import os

class Config(object):

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql:///powermon'
    DB_USER = 'powermon'
    DB_PASS = 'powermongem'
    DB_DB = 'powermon'

    SECRET_KEY = os.urandom(32)
    SERVER_NAME = '192.168.10.20:5000'
    ADMINS = ['dan@dandietz.com']
