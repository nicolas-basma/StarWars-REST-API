from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

favorite_character = db.Table("favorite_character",
db.Column("id", db.Integer, primary_key=True),
db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
db.Column("character_id",db.Integer, db.ForeignKey("character.id")))

favorite_planet = db.Table("favorite_planet",
db.Column("id", db.Integer, primary_key=True),
db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
db.Column("planet_id", db.Integer, db.ForeignKey("planet.id")))

favorite_vehicle = db.Table("favorite_vehicle",
db.Column("id", db.Integer, primary_key=True),
db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
db.Column("vehicle_id",db.Integer,db.ForeignKey("vehicle.id")))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    favorite_characters = db.relationship("Character",  backref=db.backref('users'), secondary=favorite_character)
    favorite_planets = db.relationship("Planet", backref=db.backref('users'), secondary=favorite_planet)
    favorite_vehicles = db.relationship("Vehicle", backref=db.backref('users'),secondary=favorite_vehicle)
    def __repr__(self):
        return '%r' % self.email
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_characters": [f'{character}' for character in self.favorite_characters],
            "favorite_vehicles": [f'{vehicle}' for vehicle in self.favorite_vehicles],
            "favorite_planets": [f'{planet}' for planet in self.favorite_planets]
            # do not serialize the password, its a security breach
        }
    def favorites(self):
        return {
            "favorite_characters": [character.serialize() for character in self.favorite_characters],
            "favorite_vehicles": [vehicle.serialize() for vehicle in self.favorite_vehicles],
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets]
        }
    def add_favorite(self, type, id):
        if type == "people":
            self.favorite_characters.append(Character.query.get(id))
        elif type == "planets":
            self.favorite_planets.append(Planet.query.get(id))
        elif type == "vehicles":
            self.favorite_vehicles.append(Vehicle.query.get(id))
        db.session.commit()

    def remove_favorite(self, type, id):
        if type == "people":
            self.favorite_characters.remove(Character.query.get(id))
        elif type == "planets":
            self.favorite_planets.remove(Planet.query.get(id))
        elif type == "vehicles":
            self.favorite_vehicles.remove(Vehicle.query.get(id))
        db.session.commit()


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    gender = db.Column(db.String(120), nullable=False, unique=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"))
    homeworld = db.relationship("Planet", back_populates="residents")
    vehicle =  db.relationship("Vehicle", back_populates="pilots")
    def __repr__(self):
        return "%r" % self.name
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "homeworld": self.homeworld.name,
            "vehicle": self.vehicle.name
        }



class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    terrain = db.Column(db.Integer, nullable=True, unique=False)
    population = db.Column(db.Integer, nullable=True, unique=False)
    residents = db.relationship("Character",back_populates="homeworld")
    def __repr__(self):
        return '%r' % self.name
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "residents": [resident.name for resident in self.residents]
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    model = db.Column(db.String(120), nullable=False, unique=True)
    passengers = db.Column(db.Integer, nullable=False, unique=False)
    pilots = db.relationship("Character", back_populates="vehicle")
    def __repr__(self):
        return '%r' % self.name
    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
            "pilots": [pilot.name for pilot in self.pilots]
        }

