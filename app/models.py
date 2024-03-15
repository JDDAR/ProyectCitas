## importamos sqlALchemy --> para efinir los atributos de los objetos 
## Pero con tipos trsducibles a sql y mysql 

from app import db
from datetime import datetime

class Medico(db.Model):
    __tablename__='medicos'
    id = db.Column(db.Integer, primary_key = True ) 
    nombres = db.Column(db.String(120), nullable = True )
    apellidos = db.Column(db.String(120), nullable = True)
    tipo_identificacion = db.Column(db.String(4), nullable = True)
    numero_identificacion = db.Column(db.Integer)
    registro_medico = db.Column(db.Integer)
    especialidad = db.Column(db.String(50))
    
    citas = db.relationship("Cita" , backref = "medico" )

class Paciente(db.Model):
    __tablename__ ='pacientes'
    id = db.Column(db.Integer, primary_key = True ) 
    nombres = db.Column(db.String(120), nullable = True )
    apellidos = db.Column(db.String(120), nullable = True)
    tipo_identificacion = db.Column(db.String(4), nullable = True)
    numero_identificacion = db.Column(db.Integer)
    altura = db.Column(db.Integer)
    tipo_sangre = db.Column(db.String(2))
    
    citas = db.relationship("Cita" , backref = "paciente" )
    
class Consultorio(db.Model):
    
    __tablename__ = 'consultorios'
    id= db.Column(db.Integer, primary_key = True)
    numero = db.Column(db.Integer)

    citas = db.relationship("Cita" , backref = "consultorio" )


class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime, default = datetime.utcnow)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'))
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorios.id')) 












