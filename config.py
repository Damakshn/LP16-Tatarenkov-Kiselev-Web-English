import os

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get("WEB_ENGLISH_SECRET_KEY")


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///../tmp/dev.db"


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///../database.db"


class TestConfig(Config):
    TESTING = True
