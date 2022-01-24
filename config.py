import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", "default-key")
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

