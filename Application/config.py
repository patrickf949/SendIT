"""
Congigure different environments
"""

import os
class Config():
    DEBUG = False
    dbname = 'dd63hj5clrnj1s'
    hostname = 'ec2-54-225-196-122.compute-1.amazonaws.com'

class DevelopmentConfig(Config):
    DEBUG =  True
    

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    dbname = 'test_senditdb'
    hostname = 'localhost'


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False



app_config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}

