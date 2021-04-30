import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Servicios, Perfil, Solicitudes, Comunas
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
        perfil.Respuesta = request.json.get("Respuesta")
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


@app.route("/solicitudes", methods=["GET", "POST"])
def get_solicitudes():
    if request.method == "POST":
        solicitudes = Solicitudes()
        solicitudes.Id_Solicitud = request.json.get("Id_Solicitud")
        solicitudes.Id_Servicio = request.json.get("Id_Servicio")
        solicitudes.Id_Perfil = request.json.get("Id_Perfil")
        solicitudes.id_Comuna = request.json.get("id_Comuna")
        solicitudes.Estado_Solicitud = request.json.get("Estado_Solicitud")        
        solicitudes.Nombres = request.json.get("Nombres")
        solicitudes.Apellidos = request.json.get("Apellidos")
        solicitudes.Telefono_Contacto = request.json.get("Telefono_Contacto")
        solicitudes.Direccion = request.json.get("Direccion")
        solicitudes.Calificacion = request.json.get("Calificacion")
        solicitudes.Fecha = request.json.get("Fecha")
        solicitudes.Hora = request.json.get("Hora")

        db.session.add(solicitudes)
        db.session.commit()
        return jsonify(solicitudes.serialize_all_fields()), 200

    if request.method == "GET":
        solicitud = Solicitudes.query.all()
        solicitud = list(map(lambda solicitud: solicitud.serialize_strict(), solicitudes))
        return jsonify(solicitudes), 200


@app.route("/comunas", methods=["GET", "POST"])
def get_comunas():
    if request.method == "POST":
        comunas = Comunas()
        comunas.Id_Region = request.json.get("Id_Region")
        comunas.Id_Comuna = request.json.get("Id_Comuna")
        comunas.Nombre_Comuna = request.json.get("Nombre_Comuna")
        db.session.add(comunas)
        db.session.commit()
        return jsonify(comunas.serialize_all_fields()), 200

    if request.method == "GET":
        comunas = Comunas.query.all()
        comunas = list(map(lambda comuna: comuna.serialize_strict(), comunas))
        return jsonify(comunas), 200



if __name__ == "__main__":
    manager.run()