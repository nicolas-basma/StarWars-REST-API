"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Vehicle, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


###########people#########################
@app.route('/people', methods=['GET'])
def all_people():
    characters = db.session.query(Character).all() ## Character.query.all()
    characters = list(map(lambda character: character.serialize(),characters))
    return jsonify(characters), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = db.session.query(Character).filter(Character.id == people_id).first()
    return jsonify(character.serialize()), 201


#############planets###############
@app.route('/planets', methods=['GET'])
def all_planets():
    planets = db.session.query(Planet).all()
    planets = list(map(lambda planet: planet.serialize(),planets))
    return jsonify(planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    planet = db.session.query(Planet).filter(Planet.id == planets_id).first()
    return jsonify(planet.serialize()), 201


#################vehicles#########################
@app.route('/vehicles', methods=['GET'])
def all_vehicles():
    vehicles = db.session.query(Vehicle).all()
    vehicles = list(map(lambda vehicle: vehicle.serialize(),vehicles))
    return jsonify(vehicles), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicles(vehicles_id):
    vehicle = db.session.query(Vehicle).filter(Vehicle.id == vehicles_id).first()
    return jsonify(vehicle.serialize()), 201



##################users##########################
@app.route('/users', methods=['GET'])
def all_users():
    users = db.session.query(User).all()
    users = list(map(lambda user: user.serialize(),users))
    return jsonify(users), 200

@app.route('/users/favorites', methods=['GET'])
def all_favorites():
    favorite_user = db.session.query(Favorite).all()
    favorite_user = list(map(lambda favorite: favorite_user.serialize(), favorite_user))
    return jsonify(favorite_user), 200






    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
