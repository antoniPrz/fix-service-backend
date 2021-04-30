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
    Pregunta = db.Column(db.String(100), nullable=True)
    Respuesta = db.Column(db.String(200), nullable=True)
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
        "Respuesta":self.Respuesta,
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



class Solicitudes(db.Model):
    Id_Solicitud = db.Column(db.Integer, primary_key=True)
    Id_Servicio = db.Column(db.Integer, primary_key=True)
    Id_Perfil = db.Column(db.Integer, primary_key=True)
    id_Comuna = db.Column(db.Integer, primary_key=True)
    Estado_Solicitud = db.Column(db.String(10), nullable=False)
    Nombres = db.Column(db.String(60), nullable=False)
    Apellidos = db.Column(db.String(90), nullable=False)
    Telefono_Contacto = db.Column(db.Integer, nullable=False)
    Direccion = db.Column(db.String(150), nullable=False)
    Calificacion = db.Column(db.Integer, nullable=True)
    Fecha = db.Column(db.Date)
    Hora = db.Column(db.Date)


    def __repr__(self):
        return "<Solicitudes %r>" % self.Id_Solicitud

    def serialize_all_fields(self):
        return {
        "Id_Solicitud": self.Id_Solicitud,
        "Id_Servicio":self.Id_Servicio,  
        "Id_Perfil": self.Id_Perfil,
        "id_Comuna": self.id_Comuna,
        "Estado_Solicitud" : self.Estado_Solicitud,
        "Nombres":self.Nombres,  
        "Apellidos": self.Apellidos,
        "Telefono_Contacto":self.Telefono_Contacto,  
        "Direccion": self.Direccion,
        "Calificacion":self.Calificacion,  
        "Fecha":self.Fecha,
        "Hora": self.Hora                           
        }

    def serialize_strict(self):
        return {
        "Id_Solicitud": self.Id_Solicitud,
        "Id_Perfil":self.Id_Perfil
        }        

class Comunas(db.Model):
    Id_Region = db.Column(db.Integer, nullable=False)
    Id_Comuna = db.Column(db.Integer, primary_key=True)
    Nombre_Comuna = db.Column(db.String(150), nullable=False)


    def __repr__(self):
        return "<Comunas %r>" % self.Id_Comuna

    def serialize_all_fields(self):
        return {
        "Id_Region": self.Id_Region,
        "Id_Comuna":self.Id_Comuna,
        "Nombre_Comuna":self.Nombre_Comuna  
        }

    def serialize_strict(self):
        return {
        "Id_Region": self.Id_Region,
        "Id_Comuna":self.Id_Comuna
        }
