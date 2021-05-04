from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Services(db.Model):
    id_service = db.Column(db.Integer, primary_key=True)
    name_service = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Services %r>" % self.name_service

    def serialize_all_fields(self):
        return {
        "id_service": self.id_service,
        "name_service":self.name_service  
        }

    def serialize_strict(self):
        return {
        "id_service": self.id_service,
        "name_service":self.name_service
        }


class Profile(db.Model):
    id_profile = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    question = db.Column(db.String(100), nullable=True)
    answer = db.Column(db.String(200), nullable=True)
    id_commune = db.Column(db.Integer, primary_key=True)
    attention_communes = db.Column(db.String(200), nullable=True)
    experience = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        return "<Profile %r>" % self.role

    def serialize_all_fields(self):
        return {
        "id_profile": self.id_profile,
        "role": self.role,
        "full_name":self.full_name,  
        "last_name": self.last_name,
        "phone":self.phone,  
        "address": self.address,
        "question":self.question,  
        "answer":self.answer,
        "id_commune": self.id_commune,
        "attention_communes":self.attention_communes,  
        "experience": self.experience                              
        }

    def serialize_strict(self):
        return {
        "id_profile": self.id_profile,  
        "role": self.role
        }


class Communes(db.Model):
    name_region = db.Column(db.String(100), nullable=False)
    id_commune = db.Column(db.Integer, primary_key=True)
    name_commune = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return "<Communes %r>" % self.id_commune

    def serialize_all_fields(self):
        return {
        "name_region": self.name_region,
        "id_commune":self.id_commune,
        "name_commune":self.name_commune  
        }

    def serialize_strict(self):
        return {
        "name_region": self.name_region,
        "id_commune":self.id_commune
        }


class Availability(db.Model):
    id_profile = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False) #default=db.func.current_timestamp())
    hour = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Availability %r>" % self.id_profile

    def serialize_all_fields(self):
        return {
        "id_profile": self.id_profile,                
        "date": self.date,
        "hour":self.hour  
        }

    def serialize_strict(self):
        return {
        "id_profile": self.id_profile,
        "date": self.date
        }


class Ratings(db.Model):
    id_profile = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Ratings %r>" % self.id_profile

    def serialize_all_fields(self):
        return {
        "id_profile": self.id_profile,                
        "rating": self.rating 
        }

    def serialize_strict(self):
        return {
        "id_profile": self.id_profile
        }


class User(db.Model):    
    id_user = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(9), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    password_previous = db.Column(db.String(50), nullable=True)    

    def __repr__(self):
        return "<User %r>" % self.id_user

    def serialize_all_fields(self):
        return {
        "id_user": self.id_user,
        "rut":self.rut,
        "email":self.email         
        }

    def serialize_strict(self):
        return {
        "id_user": self.id_user,
        "rut":self.rut
        }


class Requests(db.Model):
    id_request = db.Column(db.Integer, primary_key=True)
    id_service = db.Column(db.Integer, nullable=False)
    id_profile = db.Column(db.Integer, nullable=False)
    id_commune = db.Column(db.Integer, nullable=False)
    request_status = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    contact_phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Requests %r>" % self.id_request

    def serialize_all_fields(self):
        return {
        "id_request": self.id_request,
        "id_service": self.id_service,
        "id_profile": self.id_profile,
        "id_commune": self.id_commune,
        "request_status": self.request_status,
        "full_name":self.full_name,  
        "last_name": self.last_name,
        "contact_phone":self.contact_phone,  
        "address": self.address,
        "rating":self.rating,  
        "date":self.date,
        "hour": self.hour                             
        }

    def serialize_strict(self):
        return {
        "id_request": self.id_request,  
        "id_service": self.id_service,
        "id_profile": self.id_profile,  
        "id_commune": self.id_commune
        }

