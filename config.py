import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = True
    DEVELOPMENT = True
    CSRF_ENABLED = True
    # SECRET_KEY = os.getenv("SECRET_KEY", "default-key")
    SQLALCHEMY_DATABASE_URI = os.environ["DEV_DATABASE_URL"]

class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]

class StagingConfig(Config):
    DEVELOPMENT = False

class DevelopmentConfig(Config):
    pass

