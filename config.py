import os
class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Mahirane231995@localhost/Shop'

  DEBUG = True #cause debugging for any changes you make  


## Adding configuration for testing purposes

class TestingConfig:
  SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
  DEBUG = True
  CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
  CACHE_TYPE = "SimpleCache"

