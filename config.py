import os

S3_BUCKET                 = os.getenv("S3_BUCKET_NAME")
S3_KEY                    = os.getenv("S3_ACCESS_KEY")
S3_SECRET                 = os.getenv("S3_SECRET_ACCESS_KEY")
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)


class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False
    GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID_KEY")
    GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET_KEY")


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = False
    GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID_KEY")
    GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET_KEY")

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
