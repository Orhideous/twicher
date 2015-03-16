class Config:
    DEBUG = False
    TESTING = False
    DB_TYPE = 'sqlite'
    DB_NAME = None


class Development(Config):
    DEBUG = True
    DB_NAME = '/tmp/quotes_dev.sqlite'


class Testing(Config):
    TESTING = True
    DB_NAME = ':memory:'


class Production(Config):
    DB_NAME = 'quotes.sqlite'
