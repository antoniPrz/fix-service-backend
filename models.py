from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Servicios(db.Model):
    Id_Servicio = db.Column(db.Integer, primary_key=True)
    Nombre_Servicio = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Servicios %r>" % self.Nombre_Servicio

    def serialize_all_fields(self):
        return {
        "Id_Servicio": self.Id_Servicio,
        "Nombre_Servicio":self.Nombre_Servicio  
        }

    def serialize_strict(self):
        return {
        "Id_Servicio": self.Id_Servicio,
        "Nombre_Servicio":self.Nombre_Servicio
        }


class Perfil(db.Model):
    Id_Perfil = db.Column(db.Integer, primary_key=True)
    Rut = db.Column(db.Integer, primary_key=True)
    Rol = db.Column(db.String(15), nullable=False)
    Nombres = db.Column(db.String(60), nullable=False)
    Apellidos = db.Column(db.String(90), nullable=False)
    Telefono = db.Column(db.Integer, nullable=False)
    Direccion = db.Column(db.String(150), nullable=False)
    Pregunta = db.Column(db.String(200), nullable=True)
    Id_Comuna = db.Column(db.Integer, primary_key=True)
    Comunas_Atencion = db.Column(db.String(200), nullable=True)
    Experiencia = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        return "<Perfil %r>" % self.Rol

    def serialize_all_fields(self):
        return {
        "Id_Perfil": self.Id_Perfil,
        "Rut":self.Rut,  
        "Rol": self.Rol,
        "Nombres":self.Nombres,  
        "Apellidos": self.Apellidos,
        "Telefono":self.Telefono,  
        "Direccion": self.Direccion,
        "Pregunta":self.Pregunta,  
        "Id_Comuna": self.Id_Comuna,
        "Comunas_Atencion":self.Comunas_Atencion,  
        "Experiencia": self.Experiencia                              
        }

    def serialize_strict(self):
        return {
        "Id_Perfil": self.Id_Perfil,
        "Rut":self.Rut,  
        "Rol": self.Rol
        }