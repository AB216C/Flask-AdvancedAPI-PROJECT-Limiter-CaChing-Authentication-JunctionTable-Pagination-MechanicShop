

# Packages Installation

Remove current Environment


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


# Project Description: AdvancedApi(Mechanic Shop)


The project involves relationship between customerS, mechanics, service_tickets, and inventory(car parts) at the mechanic shop. All these elements are represented by model as a table.

Those tables have one-to-many relationship between customer and service_tickets, many-to-many relationship between service_tickets and mechanics which is displayed using Service_Mechanic table. Additionally, there is many to many relationship between inventory and service_tickets which is displayed in the model using Service_Inventory junction table.


Each table has routes and schemas embedded in blueprints folder. The routes are essential for RESTFUL design and they demonstrate the purpose for the application  or api being created through CRUD actions. While schemas are essentials for input data validation and serializing SQLALchemy objects into JSON responses(outputs).


POSTMAN was used to test each end points from the routes for all tables and the results was shown in the TestingShopEndpoints.postman_collection.json file. 



