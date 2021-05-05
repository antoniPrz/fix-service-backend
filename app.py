import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Services, Profile, Communes, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR, 'test.db')
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
#Crear un nuevo usuario
@app.route("/user/register", methods=["POST"])
def get_user():
    user = User()
    user.email = request.json.get("email")
    user.rut = request.json.get("rut")
    password_hash = bcrypt.generate_password_hash(request.json.get('password'))
    user.password = password_hash

    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize_all_fields()), 200

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
            profile.address = request.qjson.get("address")
            profile.id_profile = request.json.get("id_profile")
            profile.role = request.json.get("role")
            profile.phone = request.json.get("phone")
            profile.address = request.json.get("address")
            profile.question = request.json.get("question")
            profile.answer = request.json.get("answer")
            profile.id_commune = request.json.get("id_commune")

            db.session.commit()
            return jsonify("Profile updated"), 200
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
        service.Id_Service = request.json.get("Id_Service")
        service.Name_Service = request.json.get("Name_Service")
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
        communes.Id_Region = request.json.get("Id_Region")
        communes.Id_Commune = request.json.get("Id_Commune")
        communes.Name_Commune = request.json.get("Name_Commune")
        db.session.add(communes)
        db.session.commit()
        return jsonify(communes.serialize_all_fields()), 200

    if request.method == "GET":
        communes = Communes.query.all()
        communes = list(map(lambda commune: commune.serialize_strict(), communes))
        return jsonify(communes), 200



if __name__ == "__main__":
    manager.run()