import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Services, Profile, Communes, Availability, Ratings, User, Requests
from flask_bcrypt import Bcrypt
from datetime import date, datetime, time
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, 'te_ayudo.db')
app.config["DEBUG"] = True
app.config["ENV"] = "development"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'secret-key'
app.config["JWT_SECRET_KEY"] = 'encrypt'

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route("/")
def main():
    return render_template('index.html')

#Cesar inicio
#login usuario
@app.route("/user/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    #valida que el usario exista
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify("This user doesn't exist"), 404

    if bcrypt.check_password_hash(user.password, password): #retorna booleano
        access_token =create_access_token(identity=email)
        return jsonify({
            "user": user.serialize_all_fields(),
            "access_token": access_token
        })
#Editar un usuario
@app.route('/user/profile/<int:id>', methods=['PUT'])
def get_profile_id(id):
    if request.method == 'PUT':
        if id is not None:
            profile = Profile.query.filter_by(id=id).first()
            if profile is None :
                return jsonify("This user doesn't exist"), 200
            user = User.query.filter_by(id=profile.user_id).first()
            password_hash = bcrypt.generate_password_hash(request.json.get('password'))
            user.password = password_hash
            user.id_commune = request.json.get("id_commune")
            user.address = request.qjson.get("address")
            profile.id_profile = request.json.get("id_profile")
            profile.role = request.json.get("role")
            profile.phone = request.json.get("phone")
            profile.question = request.json.get("question")
            profile.answer = request.json.get("answer")


            db.session.commit()
            return jsonify("Profile updated"), 200

#Crear un nuevo usuario          
@app.route('/user/profile', methods=["GET", "POST"])
def get_profile():
    if request.method == "POST":
        user = User()
        user.email = request.json.get("email")
        user.rut = request.json.get("rut")
        user.full_name = request.json.get("full_name")
        user.last_name = request.json.get("last_name")
        user.phone = request.json.get("phone")
        user.address = request.json.get("address")
        user.id_commune = request.json.get("id_commune")
        password_hash = bcrypt.generate_password_hash(request.json.get('password'))
        user.password = password_hash

        db.session.add(user)
        db.session.commit()

        profile = Profile()
        profile.role = request.json.get("role")
        profile.question = request.json.get("question")
        profile.answer = request.json.get("answer")
       
        if profile.role != "client":    
            profile.attention_communes = request.json.get("attention_communes")
            profile.experience = request.json.get("experience")

        db.session.add(profile)
        db.session.commit()
        return jsonify({
            'user':user.serialize_all_fields(),
            'profile':profile.serialize_all_fields()
            }), 200

    if request.method == "GET":
        profiles = Profile.query.all()
        profiles = list(map(lambda profile: profile.serialize_strict(), profiles))
        return jsonify(profiles), 200
#Cesar fin


@app.route("/service", methods=["GET", "POST"])
def get_services():
    if request.method == "POST":
        service = Services()
        service.id = request.json.get("id")
        service.name_service = request.json.get("name_service")
        db.session.add(service)
        db.session.commit()
        return jsonify(service.serialize_all_fields()), 200

    if request.method == "GET":
        services = Services.query.all()
        services = list(map(lambda service: service.serialize_strict(), services))
        return jsonify(services), 200


@app.route("/communes", methods=["GET", "POST"])
def get_communes():
    if request.method == "POST":
        communes = Communes()
        communes.id = request.json.get("id")
        communes.name_region = request.json.get("name_region")
        communes.name_commune = request.json.get("name_commune")
        db.session.add(communes)
        db.session.commit()
        return jsonify(communes.serialize_all_fields()), 200

    if request.method == "GET":
        communes = Communes.query.all()
        communes = list(map(lambda commune: commune.serialize_strict(), communes))
        return jsonify(communes), 200

<<<<<<< HEAD

@app.route("/availability", methods=["GET", "POST"])
def get_availability():
    if request.method == "POST":
        availability = Availability()
        availability.id = request.json.get("id")             
        availability.date = request.json.get("date")
        availability.hour = request.json.get("hour")
        db.session.add(availability)
        db.session.commit()
        return jsonify(availability.serialize_all_fields()), 200

    if request.method == "GET":
        availabilitys = Availability.query.all()
        availabilitys = list(map(lambda availability: availability.serialize_strict(), availabilitys))
        return jsonify(availabilitys), 200


@app.route("/ratings", methods=["GET", "POST"])
def get_ratings():
    if request.method == "POST":
        rating = Ratings()
        rating.id = request.json.get("id")             
        rating.rating = request.json.get("rating")
        db.session.add(rating)
        db.session.commit()
        return jsonify(rating.serialize_all_fields()), 200

    if request.method == "GET":
        ratings = Ratings.query.all()
        ratings = list(map(lambda rating: rating.serialize_strict(), ratings))
        return jsonify(ratings), 200


@app.route("/requests", methods=["GET", "POST"])
def get_requests():
    if request.method == "POST":
        requests = Requests()
        requests.id = request.json.get("id")
        requests.id_service = request.json.get("id_service")
        requests.id_commune = request.json.get("id_commune")
        requests.request_status = request.json.get("request_status")
        requests.full_name = request.json.get("full_name")
        requests.last_name = request.json.get("last_name")
        requests.contact_phone = request.json.get("contact_phone")
        requests.address = request.json.get("address")
        requests.date = request.json.get("date")
        requests.hour = request.json.get("hour")

        db.session.add(requests)
        db.session.commit()
        return jsonify(requests.serialize_all_fields()), 200

    if request.method == "GET":
        requests = Requests.query.all()
        requests = list(map(lambda request: request.serialize_strict(), requests))
        return jsonify(requests), 200


if __name__ == "__main__":
    manager.run()






