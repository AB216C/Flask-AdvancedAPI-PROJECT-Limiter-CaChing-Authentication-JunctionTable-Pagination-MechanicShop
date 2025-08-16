from flask import Flask
from app.extentions import ma,limiter,cache
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask import send_from_directory,cross_origin



SWAGGER_URL = '/api/docs' 
API_URL = '/swagger.yaml'


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Your API's Name"
    }
)

def create_app(config_name): 
  app = Flask(__name__)
  app.config.from_object(f'config.{config_name}')
  app.config['CACHE_TYPE'] = 'SimpleCache'

  # to enable cors
  CORS(app)
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
  app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint

# swagger.yaml via custom route
  @app.route('/swagger.yaml')
  @cross_origin()
  def send_swagger():
    return send_from_directory('static', 'swagger.yaml')

  return app