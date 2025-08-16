# Packages Installation

Start with:
python3 -m venv path/to/venv.  ->This will add a new environment

source path/to/venv/bin/activate

Packages:
python3 -m pip install xyz

python3 -m pip install flask_marshmallow

python3 -m pip install flask_sqlalchemy

python3 -m pip install marshmallow-sqlalchemy

python3 -m pip install mysql-connector-python

python3 -m pip install python-jose #To handle authentication

python3 -m pip install Flask-Caching

python3 -m pip install Flask-Limiter

python3 -m pip install flask-swagger flask_swagger_ui

python3 -m pip install -r src/requirements.txt

<!-- python3 -m pip install swagger-cli -->
npm install -g swagger-cli

# To add all installed packages to requirements.txt
pip freeze > requirements.txt

# TO RUN TEST-Test Drivent Development
python -m unittest discover -s tests -p "test_*.py"

# For deployment purpose, install the following:
python3 -m pip install gunicorn

# TO ACCESS EXTERNAL DATABASE: SQLALCHEMY_DATABASE_URI = <external database url from render> from .env file, the following has to be installed:

python3 -m  pip install python-dotenv

# Your Flask app is trying to use PostgreSQL via SQLAlchemy, and it requires the psycopg2 package to communicate with the PostgreSQL database

python3 -m pip install psycopg2-binary


# Project Description: AdvancedApi(Mechanic Shop)

The project involves the relationship between customers, mechanics, service_tickets, and inventory(car parts) at the mechanic shop. All these elements are represented by the model as a table.

Those tables have a one-to-many relationship between customer and service_tickets, a many-to-many relationship between service_tickets and mechanics, which is displayed using the Service_Mechanic table. Additionally, there is many to many relationship between inventory and service_tickets, which is displayed in the model using the Service_Inventory junction table.

Each table has routes and schemas embedded in the blueprints folder. The routes are essential for RESTFUL design, and they demonstrate the purpose for the application  or api being created through CRUD actions. While schemas are essentials for input data validation and serializing SQLALchemy objects into JSON responses(outputs).

The routes use Rate limiting and caching by which limiting prevent too many request from a single user. A user has a limited number of requests from a certain route per a certain time. While caching is being used to handle more traffic from the clients.  Some routes require a token to access them. This prevents unauthorized users from accessing the routes.

POSTMAN was used to test each end points from the routes for all tables, and the results was shown in the TestingShopEndpoints.postman_collection.json file. 

Plus, API documentation was incorporated using both Swagger.yaml file. This(link: # http://127.0.0.1:5000/api/docs/#/) was essential to check if yaml file has accurate information.

Further, each defined routes was tested in the processes called Test Driven Development(TDD) in REST API development,  and code were written using "tests folder" to show positive and negative tests of API using the following code:
# python -m unittest discover -s tests -p "test_*.py"

In addition, CI pipeline is introducted using workflow file called main.yaml and with github actions you can isee if build and test run green.


SQL lite and MYSQL are local database.









