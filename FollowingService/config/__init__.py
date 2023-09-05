import os

class BaseConfig:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REPOSITORY_TYPE = 'SQLAlchemy'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URL = 'sqlite:///following.db'

class ProductionConfig(BaseConfig):
    DEBUG = False

def get_config():
    env = os.getenv('ENV', 'development').upper()
    return {
        'DEVELOPMENT': DevelopmentConfig,
        'PRODUCTION': ProductionConfig
    }.get(env, DevelopmentConfig)