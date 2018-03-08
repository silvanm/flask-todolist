# -*- coding: utf-8 -*-
import json
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def create_sqlite_uri(db_name):
    if 'VCAP_SERVICES' in os.environ:
        vcap_services = json.loads(os.environ['VCAP_SERVICES'])
        return vcap_services['mariadbent'][0]['credentials']['database_uri'].replace('?reconnect=true', '')
    else:
        return f'mysql://root:coffy@localhost/{db_name}'


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret key, just for testing'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('todolist-dev')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('todolist-test')
    WTF_CSRF_ENABLED = False
    import logging
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    )
    logging.getLogger().setLevel(logging.DEBUG)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('todolist.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
