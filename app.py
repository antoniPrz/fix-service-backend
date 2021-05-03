import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Services, Profile, Communes, Availability
from flask_bcrypt import Bcrypt
from datetime import date, datetime, time
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

@app.route("/profile", methods=["GET", "POST"])
def get_profile():
    if request.method == "POST":
        profile = Profile()
        profile.Id_Profile = request.json.get("Id_Profile")
        profile.Rut = request.json.get("Rut")
        profile.Rol = request.json.get("Rol")
        profile.Full_Name = request.json.get("Full_Name")
        profile.Last_Name = request.json.get("Last_Name")
        profile.Phone = request.json.get("Phone")
        profile.Address = request.json.get("Address")
        profile.Question = request.json.get("Question")
        profile.Answer = request.json.get("Answer")
        profile.Id_Commune = request.json.get("Id_Commune")
        profile.Attention_Communes = request.json.get("Attention_Communes")
        profile.Experience = request.json.get("Experience")

        db.session.add(profile)
        db.session.commit()
        return jsonify(profile.serialize_all_fields()), 200

    if request.method == "GET":
        profiles = Profile.query.all()
        profiles = list(map(lambda profile: profile.serialize_strict(), profiles))
        return jsonify(profiles), 200

@app.route("/communes", methods=["GET", "POST"])
def get_communes():
    if request.method == "POST":
        communes = Communes()
        communes.Name_Region = request.json.get("Name_Region")
        communes.Id_Commune = request.json.get("Id_Commune")
        communes.Name_Commune = request.json.get("Name_Commune")
        db.session.add(communes)
        db.session.commit()
        return jsonify(communes.serialize_all_fields()), 200

    if request.method == "GET":
        communes = Communes.query.all()
        communes = list(map(lambda commune: commune.serialize_strict(), communes))
        return jsonify(communes), 200

@app.route("/availability", methods=["GET", "POST"])
def get_availability():
    if request.method == "POST":
        availability = Availability()
<<<<<<< HEAD
        availability.Id = request.json.get("Id")
        availability.date = request.json.get("date")
        availability.time = request.json.get("time")
        
        db.session.add(availability)
        db.session.commit()
        return jsonify(availability.serialize_all_fields()), 200
=======
        availability.Id_Profile = request.json.get("Id_Profile")
        #availability.Year = request.json.get("Year")
        #availability.Month = request.json.get("Month")
        #availability.Day = request.json.get("Day")
        #availability.Hour = request.json.get("Hour")
        #availability.Minute = request.json.get("Minute")
        #availability.Second = request.json.get("Second")                
        availability.Date = request.json.get("Date")
        availability.Hour = request.json.get("Hour")
        db.session.add(availability)
        db.session.commit()
        return jsonify(availability.serialize_all_fields()), 200

    if request.method == "GET":
        availabilitys = Availability.query.all()
        availabilitys = list(map(lambda availability: availability.serialize_strict(), availabilitys))
        return jsonify(availabilitys), 200
>>>>>>> aron

    if request.method == "GET":
        availabilities = Availability.query.all()
        availabilities = list(map(lambda availability: availability.serialize_strict(), availabilities))
        return jsonify(availabilities), 200

if __name__ == "__main__":
    manager.run()