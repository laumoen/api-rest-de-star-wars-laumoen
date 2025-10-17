import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Fav, Weapon

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")

if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def StarWarsAPI():
    return jsonify({"mensaje": "welcome to the api far far away! :)"})


@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


@app.route('/character', methods=['POST'])
def post_character():
    data = request.get_json()
    required_fields = ["name", "last_name", "race", "native_planet", "is_jedi"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "compulsory fields are missing... :("}), 400

    new_character = Character(
        name=data["name"],
        last_name=data["last_name"],
        race=data["race"],
        native_planet=data["native_planet"],
        is_jedi=data["is_jedi"]
    )

    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 201


@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planet', methods=['POST'])
def post_planet():
    data = request.get_json()
    required_fields = ["name", "solar_system"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "compulsory fields are missing... :("}), 400

    new_planet = Planet(
        name=data["name"],
        solar_system=data["solar_system"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201


@app.route('/weapon', methods=['GET'])
def get_weapons():
    weapons = Weapon.query.all()
    return jsonify([weapon.serialize() for weapon in weapons]), 200


@app.route('/weapon', methods=['POST'])
def post_weapon():
    data = request.get_json()
    required_fields = ["type", "name", "is_lethal", "weapon_owner_id"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "compulsory fields are missing... :("}), 400

    new_weapon = Weapon(
        type=data["type"],
        name=data["name"],
        is_lethal=data["is_lethal"],
        weapon_owner_id=data["weapon_owner_id"]
    )

    db.session.add(new_weapon)
    db.session.commit()

    return jsonify(new_weapon.serialize()), 201


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    app.run(debug=True)
