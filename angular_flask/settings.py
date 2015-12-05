class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/angular_flask.db'
    SECRET_KEY = 'temporary_secret_key'  # make sure to change this

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/angular_flask_testing.db'
    SESSION_TYPE='filesystem'
