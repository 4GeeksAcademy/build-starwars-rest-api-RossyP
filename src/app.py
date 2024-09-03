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
from models import db, User, Character, Planet, Specie, Favorite
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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# -------------------------------------------------
# USERS
# -------------------------------------------------
@app.route("/users", methods=["GET"])
def get_users():
    try:
        query_results = User.query.all()
        results = list(map(lambda user: user.serialize(), query_results))
    
        response_body ={
            "msg": "Hello, this is your GET /users response ",
            "results":results
        }

        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500
    

@app.route("/users", methods=["POST"])
def add_users():
    try:
        data = request.json
        print(data)
        existing_user = User.query.filter((User.email == data.get("email")) | (User.name == data.get("name"))).first()
    
        if existing_user:
            return jsonify({"msg": "user already exists"}), 400

        new_user = User(
            name=data.get("name"),
            email=data.get("email")
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User added successfully", "user": new_user.serialize()}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        query_result = User.query.filter_by(id = user_id).first()
        print(query_result)
        response_body = {
            "msg": "Hello, this is your GET /user/user_id response ",
            "result":query_result.serialize()
        }
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500



@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({"msg": "User deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500


@app.route("/user/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.json

        existing_user = User.query.filter(User.email == data.get("email"), User.id != user_id).first()
        if existing_user:
            return jsonify({"msg":"Another user with that email already exists"}), 400
        
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]

        db.session.commit()
        
        return jsonify({"msg": "User updated successfully", "user": user.serialize()}), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500

# -------------------------------------------------
# CHARACTERS
# -------------------------------------------------
@app.route("/characters", methods=["GET"])
def get_characters():
    try:
        query_results  = Character.query.all()
        results = list(map(lambda character: character.serialize(), query_results))
        print(results)

        response_body = {
            "msg": "Hello, this is your GET /characters response ",
            "results":results
        }
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500


@app.route("/character/<int:character_id>", methods=["GET"])
def get_character(character_id):
    try:
        query_result = Character.query.filter_by(id = character_id).first()
        print(query_result)
        response_body = {
            "msg": "Hello, this is your GET /character/character_id response ",
            "result":query_result.serialize()
        }
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500


# -------------------------------------------------
# PLANETS
# -------------------------------------------------

@app.route("/planets", methods=["GET"])
def get_planets():
    try:
        query_results = Planet.query.all()
        results = list(map(lambda planet: planet.serialize(), query_results))
        print(results, "Soy el print planet")
        
        response_body = {
            "msg": "Hello, this is your GET /planets response ",
            "results":results
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500
    
@app.route("/planet/<int:planet_id>", methods=["GET"] )
def get_planet(planet_id):
    try:
        query_result = Planet.query.filter_by(id = planet_id).first()
        print(query_result, "Soy el print de PLanet ID")
        response_body = {
            "msg": "hello, this is your GET /planet/planet_id response",
            "result": query_result.serialize()
        }
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"erroe":"Internal error", "message": str(e)}), 500


# -------------------------------------------------
# SPECIES
# -------------------------------------------------

@app.route("/species", methods=["GET"])
def get_species():
    try:
        query_results = Specie.query.all()
        results = list(map(lambda specie: specie.serialize(), query_results))
        response_body = {
            "msg": "Hello, this is your GET /species response ",
            "results":results
        }

        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"error": "Internal erro", "message": str(e)}), 500


@app.route("/specie/<int:specie_id>", methods=["GET"])
def get_specie(specie_id):
    try:
        query_result = Specie.query.filter_by(id = specie_id).first()
        print(query_result)
        response_body = {
            "msg": "Hello, this is your GET /species/species_id response ",
            "result":query_result.serialize()
        }
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500


# -------------------------------------------------
# FAVORITES
# -------------------------------------------------

@app.route("/favorites", methods=["GET"])
def get_favorites():
    try:
        query_results = Favorite.query.all()
        results = list(map(lambda favorite: favorite.serialize(), query_results))
        response_body = {
            "msg": "Hello, this is your GET /favorites response",
            "result": results
        }

        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500


@app.route("/user/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        results = list(map(lambda favorite: favorite.serialize(), favorites))
        response_body = {
            "msg": "Hello, this is your GET /user/<user_id>/favorites response",
            "result": results
        }

        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"error":"Internal error", "message": str(e)})


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"error":"User ID is required"}), 400
        
        # Verifico que exista usuario y planeta
        user = User.query.get("user_id")
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        planet = Planet.query.get("planet_id")
        if planet is None:
            return jsonify({"error":"Planet not found"}), 404
        
        # Compruebo si planeta ya se encuentra como favorito
        existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if existing_favorite:
            return jsonify({"msg": "planet already exists in user favorites"}), 200
        
        # Creamos un nuevo favorito
        new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": "Planet added to favorites",
            "favorite": new_favorite.serialize()
        }
        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({"error": "Internal error", "message": str(e)}), 500




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
