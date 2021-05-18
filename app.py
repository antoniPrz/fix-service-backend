import os, re
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Services, Profile, Communes, Availability, Ratings, User, Requests, Specialty
from flask_bcrypt import Bcrypt
from datetime import date, datetime, time, timedelta
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy.sql import text
import datetime

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
    #validacion al informar email y password
    if email == "":
        return jsonify("Debe informar su email."), 400
    if password == "":
        return jsonify("Debe informar su contraseña."), 400            

    #Regular expression that checks a valid email
    ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    #Regular expression that checks a valid password
    preg = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
    user = User()
    #Checking email     
    if (re.search(ereg,request.json.get("email"))):
        user.email = request.json.get("email")               
    else:
        return jsonify("Formato de email erróneo."), 400
    #Checking password
    if (re.search(preg,request.json.get('password'))):
        pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
        user.password = pw_hash
    else:
        return jsonify("Formato de contraseña errónea."), 400
    #valida que el usario exista    
    user = User.query.filter_by(email=email).first()
    profile = Profile.query.filter_by(id_user=request.json.get("email")).first()

    if user is None:             
        return jsonify("Usuario no existe."), 404
    if bcrypt.check_password_hash(user.password, password): #retorna booleano
        access_token =create_access_token(identity=email)
        return jsonify({
            "user": user.serialize_all_fields(),     
            "profile" : profile.serialize_all_fields(),
            "access_token": access_token
        }),200
    else:
        return jsonify("Ha ingresado mal la contraseña."), 400


#Editar un usuario
@app.route('/user/profile/<int:id>', methods=['PUT'])
def get_profile_id(id):
    if request.method == 'PUT':
        if id is not None:
            profile = Profile.query.filter_by(id=id).first()
            if profile is None :
                return jsonify("Usuario no existe."), 404
            user = User.query.filter_by(id=profile.id).first()
            #Para la primera etapa en name_region sera por defecto Region Metropolitana
            region= "Region Metropolitana"           
            #Regular expression that checks a valid phone
            phonereg = '^(56)?(\s?)(0?9)(\s?)[9876543]\d{7}$'
            #Regular expression that checks a valid password
            preg = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
            #Checking password
            if (re.search(preg,request.json.get('password'))):
                pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
                user.password = pw_hash
            else:
                return jsonify("Formato de contraseña errónea."), 400
            #Checking phone
            if (re.search(phonereg,request.json.get('phone'))):
                user.phone = request.json.get("phone")
            else:
                return jsonify("Formato de teléfono erróneo."), 400          
           
            user.name_commune = request.json.get("name_commune")
            user.address = request.json.get("address")
            profile.id_profile = request.json.get("id_profile")
            profile.role = request.json.get("role")
            profile.phone = request.json.get("phone")
            profile.question = request.json.get("question")
            profile.answer = request.json.get("answer")
            #validacion entrada
            if user.name_commune == "":
                return jsonify("Debe informar su comuna de residencia."), 400  
            if user.address == "":
                return jsonify("Debe informar su dirección."), 400                               

            if profile.role != "client":
                email_client= profile.id_communes
                Communes.query.filter_by(
                    email = (email_client)
                ).delete(synchronize_session=False)         
                profile.experience = request.json.get("experience")
                attetion_communes = request.json.get("communes")
                for name_commune in attetion_communes:
                    communes=Communes()
                    communes.name_commune=name_commune 
                    communes.email = user.email
                    communes.name_region = region
                    db.session.add(communes)                
                Specialty.query.filter_by(
                    id_user = (user.email)
                ).delete(synchronize_session=False)
                specialties = request.json.get("name_specialty")
                for name_specialty in specialties:
                    specialty=Specialty ()
                    specialty.name_specialty=name_specialty
                    specialty.id_user = user.email
                    db.session.add(specialty)

            db.session.commit()
            return jsonify("Su perfil ha sido actualizado."), 200
        else:
            return jsonify("Usuario no existe."), 404

#Crear un nuevo usuario          
@app.route('/user/profile', methods=["GET", "POST"])
def get_profile():
    if request.method == "POST":
        #valida que el usuario ya exista como cliente o especialista
        email = request.json.get("email")
        rut_reg =request.json.get("rut")
        user = User.query.filter_by(email=email).first() 
        rut_user = User.query.filter_by(rut=rut_reg).first()    
    
        if user != None:             
            return jsonify("Usted ya existe como cliente. Ingrese a su sesión y seleccione editar perfil."), 404

        if rut_user != None:             
            return jsonify("El rut ingresado ya existe en nuestros registros."), 404

        #valida que venga informado el email
        if email == "":
            return jsonify("Debe informar su email."), 400                  
        #Para la primera etapa en name_region sera por defecto Region Metropolitana
        region= "Region Metropolitana"
        #Regular expression that checks a valid email
        ereg = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        #Regular expression that checks a valid password
        preg = '^.*(?=.{4,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).*$'
        #Regular expression that checks a valid phone
        phonereg = '^(56)?(\s?)(0?9)(\s?)[9876543]\d{7}$'
        #Regular expression that checks a valid rut
        rut = '^[1-9]{1}[0-9]{6,7}-[0-9kK]{1}$'
        user = User() 

        #Checking email
        if (re.search(ereg,request.json.get("email"))):
            user.email = request.json.get("email")
        else:
            return jsonify("Formato de email erróneo."), 400
        #Checking password
        if (re.search(preg,request.json.get('password'))):
            pw_hash = bcrypt.generate_password_hash(request.json.get("password"))
            user.password = pw_hash
        else:
            return jsonify("Formato de contraseña errónea."), 400
        #Checking rut
        if (re.search(rut,request.json.get('rut'))):
            user.rut = request.json.get("rut")
        else:
            return jsonify("Formato de RUT erróneo."), 400            
        #Checking phone
        if (re.search(phonereg,request.json.get('phone'))):
            user.phone = request.json.get("phone")
        else:
            return jsonify("Formato de teléfono erróneo."), 400

        user.full_name = request.json.get("full_name")     
        user.last_name = request.json.get("last_name")
        user.address = request.json.get("address")
        user.name_commune = request.json.get("name_commune")
        #validacion campos de entrada
        if user.full_name == "":
            return jsonify("Debe informar su nombre."), 400   
        if user.last_name == "":
            return jsonify("Debe informar su apellido."), 400  
        if user.address == "":
            return jsonify("Debe informar su dirección."), 400  
        if user.name_commune == "":
            return jsonify("Debe informar su comuna de residencia."), 400                                              
        db.session.add(user)

        profile = Profile()
        profile.role = request.json.get("role")
        profile.question = request.json.get("question")
        profile.answer = request.json.get("answer")
        profile.id_user = request.json.get("email")

        if profile.role != "client":
            profile.experience = request.json.get("experience")
            profile.id_communes= request.json.get("email")
            for day in range(15):
                availability = Availability()
                date = datetime.date.today () + timedelta(days=day)
                availability.date=date
                availability.morning = True
                availability.afternoon = True
                availability.evening = True
                availability.id_user = request.json.get("email")
                db.session.add(availability)
            attetion_communes = request.json.get("communes")
            for name_commune in attetion_communes:
                communes=Communes()
                communes.name_commune=name_commune
                communes.email = request.json.get("email")
                communes.name_region = region
                db.session.add(communes)
            specialties = request.json.get("name_specialty")
            for name_specialty in specialties:
                specialty=Specialty ()
                specialty.name_specialty=name_specialty
                specialty.id_user = request.json.get("email")
                db.session.add(specialty)
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


@app.route("/service/default", methods=["GET"])
def get_services_default():
    
    if request.method == "GET":
        specialties = Specialty.query.filter_by(name_specialty='carpintero').all()
        answer = []
        date = datetime.date.today() + timedelta(days=1)
        date=date.strftime("%Y-%m-%d %H:%M:%S.%S%S%S")
        counter = 0
        
        for specialty in specialties:
            profile = Profile.query.filter_by(id_user=specialty.id_user).first()
            availability = Availability.query.filter_by(date=date, morning=True, id_user=specialty.id_user).first()
            user=User.query.filter_by(email=specialty.id_user).first()
            
            if user !=None and availability != None and profile != None:
                counter = counter+1
                answer.append({
                    'specialty':specialty.serialize_all_fields(), 
                    'user':user.serialize_all_fields(), 
                    'availability': availability.serialize_all_fields(),
                    'profile': profile.serialize_all_fields()
                    })
        if counter > 0:    
            return jsonify(answer), 200
        else:
            return jsonify("No hay especialistas disponibles."), 200

@app.route("/service", methods=["POST"])
def get_services():
    if request.method == "POST":
        speciality = request.json.get("name_specialty")
        commun = request.json.get("name_commune")
        specialties = Specialty.query.filter_by(name_specialty=speciality).all()
        communes = Communes.query.filter_by(name_commune=commun).all()
        answer = []
        date = request.json.get("date")
        date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
        #validaciones de entrada
        if speciality == "":
            return jsonify("Debe informar la especialidad del trabajo a realizar."), 400 
        if commun == "":
            return jsonify("Debe informar la comuna donde el especialista irá."), 400       
        if date == "":
            return jsonify("Debe informar la fecha cuando se realizará el trabajo."), 400       
        counter = 0
        for specialty in specialties:
            for commune in communes:
                profile = Profile.query.filter_by(id_user=specialty.id_user, id_communes = commune.email).first()
            
                availability= None
                if request.json.get("morning") == True and request.json.get("afternoon") == False and request.json.get("evening") == False:
                    availability = Availability.query.filter_by(date=date, morning=True, id_user=specialty.id_user).first()
            
                elif request.json.get("morning") == False and request.json.get("afternoon") == True and request.json.get("evening") == False:
                    availability = Availability.query.filter_by(date=date, afternoon=True, id_user=specialty.id_user).first()
            
                elif request.json.get("morning") == False and request.json.get("afternoon") == False and request.json.get("evening") == True:
                    availability = Availability.query.filter_by(date=date, evening=True, id_user=specialty.id_user).first()
           
                user=User.query.filter_by(email=specialty.id_user).first()
            
                if user !=None and availability != None and profile != None:
                    counter = counter+1
                    answer.append({
                        'specialty':specialty.serialize_all_fields(), 
                        'user':user.serialize_all_fields(), 
                        'availability': availability.serialize_all_fields(),
                        'profile': profile.serialize_all_fields()
                        })
        if counter > 0:    
            return jsonify(answer), 200
        else:
            return jsonify("No hay especialistas disponibles backend"), 200
#Cesar fin

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


@app.route("/availability", methods=["GET", "POST"])
def get_availability():
    if request.method == "POST":
        availability = Availability()
        availability.id = request.json.get("id")             
        availability.date = request.json.get("date")
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

@app.route("/user/requests/<int:id>", methods=["GET", "POST"])
def get_requests(id):
    if request.method == "POST":
        if id is not None:
            user = User.query.filter_by(id=id).first()
            if user is None :
                return jsonify("Usuario no existe."), 404
        
        request_status ="pendiente"
        #date = request.json.get("date") #2021-05-22
        date = request.json.get("date")
        date = datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S.%f')
        #y, m, d = date.split('-')
        #date_rv = datetime.datetime(int(y), int(m), int(d))                  
        requests = Requests()
        requests.name_specialty = request.json.get("name_specialty")
        requests.name_commune = request.json.get("name_commune")
        requests.request_status = request_status
        requests.full_name = request.json.get("full_name")
        requests.last_name = request.json.get("last_name")
        requests.contact_phone = request.json.get("contact_phone")
        requests.address = request.json.get("address")
        #requests.date = date_rv
        requests.date = date
        requests.hour = request.json.get("hour")
        requests.id_user = user.email
        requests.id_profile = request.json.get("id_profile")
        db.session.add(requests)
        db.session.commit()
        return jsonify({'requests':requests.serialize_all_fields()}), 200

    if request.method == "GET":
        requests = Requests.query.all()
        requests = list(map(lambda request: request.serialize_strict(), requests))
        return jsonify(requests), 200


if __name__ == "__main__":
    manager.run()





