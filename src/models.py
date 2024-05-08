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
    fav_characters = db.relationship('FavCharacter', backref='Character', lazy=True)
    fav_planets = db.relationship('FavPlanet', backref='Planet', lazy=True)
    


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "esta vivo": self.is_active,
            "Character favoritos": self.fav_characters,
            "Planets favoritos": self.fav_planets,
            # do not serialize the password, its a security breach
        }
    

class FavCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship('People')
    
    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.email
    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "people_name": self.character.name,
            
        }


class FavPlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets')
    
    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "planets_name": self.planets.name,
            
        }




