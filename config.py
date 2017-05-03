import os


class Config(object):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + Config.BASE_DIR + \
                              '/chum/chum.sqlite3'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SECRET_KEY = 'abcdefghijklmnopqrstuvwxyz1234567890'


app_configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Config
}
