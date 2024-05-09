from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "URL": self.url,
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "URL": self.url,
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    fav_characters = db.relationship('FavCharacter', backref='user_relation', lazy=True)
    fav_planets = db.relationship('FavPlanet', backref='user_relation', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "esta_vivo": self.is_active,
            "characters_favoritos": [fav_char.serialize() for fav_char in self.fav_characters],
            "planets_favoritos": [fav_planet.serialize() for fav_planet in self.fav_planets],
        }



class FavCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship('People', backref='favorite_characters')

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.people.name

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people.id,
            "people_name": self.people.name,
        }

class FavPlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets', backref='favorite_planets')

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.planets.name

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planets.id,
            "planet_name": self.planets.name,
        }
