"""
Congigure different environments
"""

import os
class Config():
    DEBUG = False
    DB_NAME = 'senditdb'

class DevelopmentConfig(Config):
    DEBUG =  True
    

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DB_NAME = 'test_senditdb'


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True

app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'staging':StagingConfig,
    'production':ProductionConfig
}

