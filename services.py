from models import Persona
import db

def registrar_persona_service(datos):
    # Servicio para crear una persona en la base de datos
    persona = Persona(
        nombre = datos["nombre_completo"],
        fecha = datos["fecha_de_nacimiento"],
        email = datos["email"],
        pais = datos["pais"],
        cedula = datos["cedula"]
    )
    db.session.add(persona)
    db.session.commit()
    return persona

def buscar_persona_service(cedula):
    # Servicio para buscar una persona por cédula
    persona = db.session.query(Persona).filter_by(cedula=cedula).first()
    return persona

def eliminar_persona_service(cedula):
    # Servicio para eliminar una persona por cédula
    persona = db.session.query(Persona).filter_by(cedula=cedula).first()
    if persona:
        db.session.delete(persona)
        db.session.commit()
    return persona

def actualizar_persona_service(datos):
    # Servicio para actualizar los datos de una persona
    persona = db.session.query(Persona).filter_by(cedula=datos["cedula"]).first()
    if persona:
        persona.nombre_completo = datos["nombre_completo"]
        persona.fecha_de_nacimiento = datos["fecha_de_nacimiento"]
        persona.email = datos["email"]
        persona.pais = datos["pais"]
        db.session.commit()
    return persona

def listar_personas_service():
    # Servicio para listar todas las personas
    personas = db.session.query(Persona).all()
    return personas