class Config:
    pass

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "sqlite:///dev.db"

    