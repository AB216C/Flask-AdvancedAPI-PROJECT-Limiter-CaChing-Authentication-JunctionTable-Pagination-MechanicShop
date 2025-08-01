from flask import Flask
from app.extentions import ma,limiter,cache
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp

def create_app(config_name): 
  app = Flask(__name__)
  app.config.from_object(f'config.{config_name}')
  app.config['CACHE_TYPE'] = 'SimpleCache'

  #initialize extentions

  ma.init_app(app)
  db.init_app(app)
  limiter.init_app(app)
  cache.init_app(app)

  #Register blueprints
  app.register_blueprint(customers_bp, url_prefix="/")
  app.register_blueprint(mechanics_bp, url_prefix="/")
  app.register_blueprint(service_tickets_bp, url_prefix="/")
  app.register_blueprint(inventory_bp, url_prefix="/")



  return app