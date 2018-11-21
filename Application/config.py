"""
Congigure different environments
"""

import os
class Config():
    DEBUG = False
    dbname = 'senditdb'

class DevelopmentConfig(Config):
    DEBUG =  True
    

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    dbname = 'test_senditdb'


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False



app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}

