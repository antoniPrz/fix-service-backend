import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Servicios, Perfil
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

@app.route("/servicio", methods=["GET", "POST"])
def get_servicios():
    if request.method == "POST":
        servicio = Servicios()
        servicio.Id_Servicio = request.json.get("Id_Servicio")
        servicio.Nombre_Servicio = request.json.get("Nombre_Servicio")
        db.session.add(servicio)
        db.session.commit()
        return jsonify(servicio.serialize_all_fields()), 200

    if request.method == "GET":
        servicios = Servicios.query.all()
        servicios = list(map(lambda servicio: servicio.serialize_strict(), servicios))
        return jsonify(servicios), 200

@app.route("/perfil", methods=["GET", "POST"])
def get_perfil():
    if request.method == "POST":
        perfil = Perfil()
        perfil.Id_Perfil = request.json.get("Id_Perfil")
        perfil.Rut = request.json.get("Rut")
        perfil.Rol = request.json.get("Rol")
        perfil.Nombres = request.json.get("Nombres")
        perfil.Apellidos = request.json.get("Apellidos")
        perfil.Telefono = request.json.get("Telefono")
        perfil.Direccion = request.json.get("Direccion")
        perfil.Pregunta = request.json.get("Pregunta")
        perfil.Id_Comuna = request.json.get("Id_Comuna")
        perfil.Comunas_Atencion = request.json.get("Comunas_Atencion")
        perfil.Experiencia = request.json.get("Experiencia")

        db.session.add(perfil)
        db.session.commit()
        return jsonify(perfil.serialize_all_fields()), 200

    if request.method == "GET":
        perfiles = Perfil.query.all()
        perfiles = list(map(lambda perfil: perfil.serialize_strict(), perfiles))
        return jsonify(perfiles), 200


if __name__ == "__main__":
    manager.run()