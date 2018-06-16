import os


def get_bool_value(varname):
    return os.getenv(varname, 'true').lower() in \
           ['true', 'on', '1']


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = get_bool_value('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[ART2CAT ]'
    MAIL_SENDER = 'ART2CAT Admin <yiming.whz@gmail.com>'
    ADMIN = os.getenv('ADMIN')
    SSL_REDIRECT = get_bool_value('SSL_REDIRECT')
    SQLALCHEMY_TRACK_MODIFICATIONS = get_bool_value('TRACK_MODIFICATIONS')
    SQLALCHEMY_RECORD_QUERIES = get_bool_value('RECORD_QUERIES')
    POSTS_PER_PAGE = int(os.getenv('POSTS_PER_PAGE', '20'))
    SLOW_DB_QUERY_TIME = float(os.getenv('SLOW_DB_QUERY_TIME', '0.5'))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
