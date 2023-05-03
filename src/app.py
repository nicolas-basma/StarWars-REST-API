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
    character = db.get_or_404(Character, people_id)
    return jsonify(character.serialize()), 201


#############planets###############
@app.route('/planets', methods=['GET'])
def all_planets():
    planets = db.session.query(Planet).all()
    planets = list(map(lambda planet: planet.serialize(),planets))
    return jsonify(planets), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):
    planet = db.get_or_404(Planet, planets_id)
    return jsonify(planet.serialize()), 201


#################vehicles#########################
@app.route('/vehicles', methods=['GET'])
def all_vehicles():
    vehicles = db.session.query(Vehicle).all()
    print(vehicles)
    vehicles = list(map(lambda vehicle: vehicle.serialize(),vehicles))
    return jsonify(vehicles), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicles(vehicles_id):
    vehicle = db.get_or_404(Vehicle, vehicles_id)
    return jsonify(vehicle.serialize()), 201



##################users##########################
@app.route('/users', methods=['GET'])
def all_users():
    users = db.session.query(User).all()
    users = list(map(lambda user: user.serialize(),users))
    return jsonify(users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def handle_get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize()
)

#################usersFavorites###################
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_get_favorite(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.favorites())

@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def handle_add_people(user_id, people_id):
    user = User.query.get_or_404(user_id)
    user.add_favorite('people' , people_id)
    return  {"message": "favorite added"}, 200

@app.route('/users/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def handle_delete_people(user_id, people_id):
    user = User.query.get_or_404(user_id)
    user.remove_favorite('people' , people_id)
    return  {"message": "favorite deleted"}, 200

@app.route('/users/<int:user_id>/favorites/planets/<int:planets_id>', methods=['POST'])
def handle_add_planets(user_id, planets_id):
    user = User.query.get_or_404(user_id)
    user.add_favorite('planets' , planets_id)
    return  {"message": "favorite added"}, 200

@app.route('/users/<int:user_id>/favorites/planets/<int:planets_id>', methods=['DELETE'])
def handle_delete_planets(user_id, planets_id):
    user = User.query.get_or_404(user_id)
    user.remove_favorite('planets' , planets_id)
    return  {"message": "favorite deleted"}, 200

@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicles_id>', methods=['POST'])
def handle_add_vehicles(user_id, vehicles_id):
    user = User.query.get_or_404(user_id)
    user.add_favorite('vehicles' , vehicles_id)
    return  {"message": "favorite added"}, 200

@app.route('/users/<int:user_id>/favorites/vehicles/<int:vehicles_id>', methods=['DELETE'])
def handle_delete_vehicles(user_id, vehicles_id):
    user = User.query.get_or_404(user_id)
    user.remove_favorite('vehicles' , vehicles_id)
    return  {"message": "favorite deleted"}, 200

@app.route("/add-people", methods=["POST"])
def add_people():
    new_people = request.json
    new_char = Character(
        name = new_people["name"],
        gender = new_people["gender"]
    )
    db.session.add(new_char)
    db.session.commit()
    return {"message": "Character created successfully"}, 200

@app.route("/delete-people/<int:people_id>", methods=["DELETE"])
def delete_people(people_id):
    people = Character.query.get(people_id)
    db.session.delete(people)
    db.session.commit()
    return {"message": "Character deleted successfully"}, 200

@app.route("/add-planet", methods=["POST"])
def add_planet():
    new_planet = request.json
    new_planet = Planet(
        name = new_planet["name"],
        terrain = new_planet["terrain"],
        population = new_planet["population"],
        resident = new_planet["resident"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return {"message": "Planet created successfully"}, 200

@app.route("/delete-planet/<int:planets_id>", methods=["DELETE"])
def delete_planet(planets_id):
    planet = Planet.query.get(planets_id)
    db.session.delete(planet)
    db.session.commit()
    return {"message": "Planet deleted successfully"}, 200

@app.route("/add-vehicle", methods=["POST"])
def add_vehicle():
    new_vehicle = request.json
    new_vehicle = Vehicle(
        name = new_vehicle["name"],
        model = new_vehicle["model"],
        passenger = new_vehicle["passenger"],
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return {"message": "Vehicle created successfully"}, 200

@app.route("/delete-vehicle/<int:vehicles_id>", methods=["DELETE"])
def delete_vehicle(vehicles_id):
    vehicle = Vehicle.query.get(vehicles_id)
    db.session.delete(vehicle)
    db.session.commit()
    return {"message": "Vehicle deleted successfully"}, 200
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
