class Config:
    DEBUG = False
    TESTING = False


class Development(Config):
    DEBUG = True
    REDIS_URL = "redis://127.0.0.1:6389/7"

