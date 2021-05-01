from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Services(db.Model):
    Id_Service = db.Column(db.Integer, primary_key=True)
    Name_Service = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Services %r>" % self.Name_Service

    def serialize_all_fields(self):
        return {
        "Id_Service": self.Id_Service,
        "Name_Service":self.Name_Service  
        }

    def serialize_strict(self):
        return {
        "Id_Service": self.Id_Service,
        "Name_Service":self.Name_Service
        }


class Profile(db.Model):
    Id_Profile = db.Column(db.Integer, primary_key=True)
    Rut = db.Column(db.Integer, primary_key=True)
    Rol = db.Column(db.String(15), nullable=False)
    Full_Name = db.Column(db.String(60), nullable=False)
    Last_Name = db.Column(db.String(90), nullable=False)
    Phone = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(150), nullable=False)
    Question = db.Column(db.String(100), nullable=True)
    Answer = db.Column(db.String(200), nullable=True)
    Id_Commune = db.Column(db.Integer, primary_key=True)
    Attention_Communes = db.Column(db.String(200), nullable=True)
    Experience = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        return "<Profile %r>" % self.Rol

    def serialize_all_fields(self):
        return {
        "Id_Profile": self.Id_Profile,
        "Rut":self.Rut,  
        "Rol": self.Rol,
        "Full_Name":self.Full_Name,  
        "Last_Name": self.Last_Name,
        "Phone":self.Phone,  
        "Address": self.Address,
        "Question":self.Question,  
        "Answer":self.Answer,
        "Id_Commune": self.Id_Commune,
        "Attention_Communes":self.Attention_Communes,  
        "Experience": self.Experience                              
        }

    def serialize_strict(self):
        return {
        "Id_Profile": self.Id_Profile,
        "Rut":self.Rut,  
        "Rol": self.Rol
        }


class Communes(db.Model):
    Id_Region = db.Column(db.Integer, nullable=False)
    Id_Commune = db.Column(db.Integer, primary_key=True)
    Name_Commune = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return "<Communes %r>" % self.Id_Commune

    def serialize_all_fields(self):
        return {
        "Id_Region": self.Id_Region,
        "Id_Commune":self.Id_Commune,
        "Name_Commune":self.Name_Commune  
        }

    def serialize_strict(self):
        return {
        "Id_Region": self.Id_Region,
        "Id_Commune":self.Id_Commune
        }
