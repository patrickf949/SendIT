"""
Congigure different environments
"""

import os
class Config():
    """
    Base configuration for environments
    """
    DEBUG = False
    # dbname = 'senditdb'
    dbname = 'dd63hj5clrnj1s'
    hostname = 'ec2-54-225-196-122.compute-1.amazonaws.com'
    # hostname = 'localhost'

class DevelopmentConfig(Config):
    """
    Configuration for development environment
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configuration for Testing environment
    """
    TESTING = True
    DEBUG = True
    dbname = 'test_senditdb'
    hostname = 'localhost'


class ProductionConfig(Config):
    """
    Configuration for Production environment
    """
    TESTING = False
    DEBUG = False



APP_CONFIG = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig
}
