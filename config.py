class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Mahirane231995@localhost/Shop'

  DEBUG = True #cause debugging for any changes you make  

class TestingConfig:
  pass

class ProductionConfig:
  pass

## Adding configuration for testing purposes

class TestingConfig:
  SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
  DEBUG = True
  CACHE_TYPE = 'SimpleCache'

  