import os



class BaseConfig:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    REPOSITORY_TYPE = 'SQLAlchemy'
    EVENT_PUBLISHER = 'kafka'
    

class TestingConfig(BaseConfig):
    DEBUG = True
    DATABASE_URL = 'sqlite:///following.db'
    EVENT_PUBLISHER = 'faux-broker'

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URL = 'sqlite:///following.db'
    KAFKA_CONFIG = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'following-service',
        'group.id': 'following-service',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    }

class ProductionConfig(BaseConfig):
    DEBUG = False

_env = None

ENVIRONMENT_REGISTRY = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def set_config(new_env="development"):
    global _env
    _env = ENVIRONMENT_REGISTRY.get(new_env, DevelopmentConfig)
    return _env

def get_config():
    global _env
    #set_config('testing')
    print("ASH")
    print(_env)
    return _env or set_config(os.environ.get('ENVIRONMENT'))