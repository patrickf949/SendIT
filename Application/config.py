class Config():
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG =  True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True

appConfig = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'staging':StagingConfig,
    'production':ProductionConfig
}

dbname= 'senditdb'