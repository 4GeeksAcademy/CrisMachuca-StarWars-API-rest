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
from models import db, User, People, Planets
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

# ENDPOINTS

#USER

@app.route('/user', methods=['GET'])
def handle_hello():
    all_users= User.query.all()
    print(all_users)
    results = list(map(lambda user: user.serialize(), all_users))
    print(list(results))
    response_body = {
        "msg": "Leer los usuarios "
    }

    return jsonify(results), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data: return "The '" + field + "' cannot be empty", 400
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()

    return "User created!", 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200

@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

#PEOPLE

@app.route('/people', methods=['GET'])
def get_people():
    all_people= People.query.all()
    print(all_people)
    results = list(map(lambda character: character.serialize(), all_people))
    print(list(results))
    response_body = {
        "msg": "Leer los personajes "
    }

    return jsonify(results), 200

@app.route('/people', methods=['POST'])
def create_character():
    data = request.json
    required_fields = ["name", "url"]
    for field in required_fields:
        if field not in data: return "The '" + field + "' cannot be empty", 400
    new_character = People(**data)
    db.session.add(new_character)
    db.session.commit()

    return "Character created!", 200

@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = People.query.filter_by(id=character_id).first()
    return jsonify(character.serialize()), 200

@app.route("/people/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = People.query.get(character_id)

    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted'}), 200

#PLANETS

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets= Planets.query.all()
    print(all_planets)
    results = list(map(lambda planet: planet.serialize(), all_planets))
    print(list(results))
    response_body = {
        "msg": "Leer los planetas "
    }

    return jsonify(results), 200

@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    required_fields = ["name", "url"]
    for field in required_fields:
        if field not in data: return "The '" + field + "' cannot be empty", 400
    new_planet = Planets(**data)
    db.session.add(new_planet)
    db.session.commit()

    return "Planet created!", 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    return jsonify(planet.serialize()), 200

@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)

    db.session.delete(planet)
    db.session.commit()
    return jsonify({'message': 'Planet deleted'}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
