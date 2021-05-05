from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    id_commune = db.Column (db.Integer, db.ForeignKey("communes.id", ondelete='CASCADE'), nullable=True)
    profiles = db.relationship('Profile', backref='user', cascade='all, delete', lazy=True) #uselist=False si la relacion es uno a uno
    
    def _repr_(self):
        return "<User %r>" % self.email

    def serialize_all_fields(self):
        return {
            "id": self.id,
            "email":self.email,
            "rut": self.rut,
            "full_name": self.full_name,
            "last_name": self.last_name,
            "phone":self.phone,  
            "address": self.address,
            "id_commune": self.id_commune
        }

    def serialize_strict(self):
        return {
            "id": self.id,
            "username":self.email
        }

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), nullable=False)
    question = db.Column(db.String(100), nullable=True)
    answer = db.Column(db.String(200), nullable=True)
    attention_communes = db.Column(db.String(200), nullable=True)
    experience = db.Column(db.String(200), nullable=True)
    id_user = db.Column (db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=True)
    ratings = db.relationship('Ratings', backref='profile', cascade='all, delete', lazy=True) 
    availabilities = db.relationship('Availability', backref='profile', cascade='all, delete', lazy=True) 
    requests = db.relationship('Requests', backref='profile', cascade='all, delete', lazy=True) 

    def __repr__(self):
        return "<Profile %r>" % self.role

    def serialize_all_fields(self):
        return {
        "id": self.id, 
        "role": self.role,
        "question":self.question,  
        "answer":self.answer,
        "attention_communes":self.attention_communes,  
        "experience": self.experience                              
        }

    def serialize_strict(self):
        return {
        "id": self.id,
        "role": self.role
        }

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False) #default=db.func.current_timestamp())
    hour = db.Column(db.String(10), nullable=False)
    id_profile = db.Column (db.Integer, db.ForeignKey("profile.id", ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return "<Availability %r>" % self.id

    def serialize_all_fields(self):
        return {
        "id": self.id,                
        "date": self.date,
        "hour":self.hour  
        }

    def serialize_strict(self):
        return {
        "id": self.id,
        "date": self.date
        }

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_service = db.Column(db.Integer, nullable=False)
    id_commune = db.Column(db.Integer, nullable=False)
    request_status = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(90), nullable=False)
    contact_phone = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.String(10), nullable=False)
    id_profile = db.Column (db.Integer, db.ForeignKey("profile.id", ondelete='CASCADE'), nullable=True)
    id_service = db.Column (db.Integer, db.ForeignKey("services.id", ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return "<Requests %r>" % self.request_status

    def serialize_all_fields(self):
        return {
        "id": self.id,
        "id_service": self.id_service,
        "id_profile": self.id_profile,
        "id_commune": self.id_commune,
        "request_status": self.request_status,
        "full_name":self.full_name,  
        "last_name": self.last_name,
        "contact_phone":self.contact_phone,  
        "address": self.address,  
        "date":self.date,
        "hour": self.hour                             
        }

    def serialize_strict(self):
        return {
        "id": self.id,  
        "id_service": self.id_service,
        "id_profile": self.id_profile,  
        "id_commune": self.id_commune,
        "request_status": self.request_status,
        }

class Services(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name_service = db.Column(db.String(50), nullable=False)
    requests = db.relationship('Requests', backref='services', cascade='all, delete', lazy=True) 

    def __repr__(self):
        return "<Services %r>" % self.name_service

    def serialize_all_fields(self):
        return {
        "id": self.id,
        "name_service":self.name_service  
        }

    def serialize_strict(self):
        return {
        "id": self.id,
        "name_service":self.name_service
        }

class Communes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_region = db.Column(db.String(100), nullable=False)
    name_commune = db.Column(db.String(150), nullable=False)
    user = db.relationship('User', backref='communes', cascade='all, delete', uselist=False) 

    def __repr__(self):
        return "<Communes %r>" % self.name_region

    def serialize_all_fields(self):
        return {
        "id":self.id,
        "name_region": self.name_region,
        "name_commune":self.name_commune  
        }

    def serialize_strict(self):
        return {
        "id":self.id,
        "name_region": self.name_region
        }

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_profile = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    profile_id = db.Column (db.Integer, db.ForeignKey("profile.id", ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return "<Ratings %r>" % self.id_profile

    def serialize_all_fields(self):
        return {
        "id":self.id,
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
