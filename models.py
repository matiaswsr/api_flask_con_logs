import db
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

class Persona(db.Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String, nullable=False)
    fecha_de_nacimiento = Column(Date, nullable=False)
    email = Column(String, nullable=False, unique=True)
    pais = Column(String, nullable=False)
    cedula = Column(String, nullable=False, unique=True) 

    def __init__(self, nombre, fecha, email, pais, cedula):
        self.nombre_completo = nombre
        self.fecha_de_nacimiento = datetime.strptime(fecha, "%Y-%m-%d").date()
        self.email = email
        self.pais = pais
        self.cedula = cedula

    def to_json(self):
        return {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "fecha_de_nacimiento": self.fecha_de_nacimiento.strftime("%Y-%m-%d"),
            "email": self.email,
            "pais": self.pais,
            "cedula": self.cedula
        }
    
