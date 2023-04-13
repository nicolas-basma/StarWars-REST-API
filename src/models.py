from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    gender = db.Column(db.String(120), nullable=False, unique=False)
    homeworld = db.Column(db.String(120), nullable=False, unique=False)#
    vehicles =  db.Column(db.String(120), nullable=False, unique=False)#

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "vehicles": self.vehicles
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    terrain = db.Column(db.Integer, nullable=True, unique=False)
    population = db.Column(db.Integer, nullable=True, unique=False)
    residents = db.Column(db.Integer, nullable=True, unique=False)#

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "residents": self.residents
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    model = db.Column(db.String(120), nullable=False, unique=True)
    passengers = db.Column(db.Integer, nullable=False, unique=False)
    pilots = db.Column(db.String(120), nullable=False, unique=False)#

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
            "pilots": self.pilots
        }
        
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=False)
    character = db.Column(db.String(120), nullable=False, unique=False)
    planets = db.Column(db.String(120), nullable=False, unique=False)
    vehicles = db.Column(db.String(120), nullable=False, unique=False)

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "character": self.character,
            "planets": self.planets,
            "vehicles": self.vehicles
        }

