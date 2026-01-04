
from flask import Flask, jsonify, request
from utils import validar_json, validar_email, validar_fecha
from flask_cors import CORS
from services import registrar_persona_service, listar_personas_service, buscar_persona_service, eliminar_persona_service, actualizar_persona_service
from werkzeug.exceptions import HTTPException
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

import db
import logging
import os

# Cargar .env
load_dotenv()

# ------------------------------------------------
# APP INIT
# ------------------------------------------------
app = Flask(__name__)
CORS(app)

# ------------------------------------------------
# LOGGING CONFIG (DEV / PROD + ROTACION DIARIA)
# ------------------------------------------------
"""
Para registrar absolutamente todo, el nivel debe ser DEBUG
Se define el nivel de loggin y se registran desde ese nivel y todos los que esten por debajo.
Niveles de logging:
    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL
"""
ENV = os.getenv("FLASK_ENV", "production")
IS_DEV = ENV == "development"

log_level = logging.DEBUG if IS_DEV else logging.INFO

logger = logging.getLogger("api_logger")
logger.setLevel(log_level)
logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Rotating file handler: un archivo por día, 7 días
log_file = "app.log"
file_handler = TimedRotatingFileHandler(
    log_file, 
    when="midnight", 
    interval=1, 
    backupCount=7,
    encoding="utf-8"
)
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler solo en DEV
if IS_DEV:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Silenciar logs internos de Flask/Werkzeug
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# -----------------------------------------------


# Middleware para registrar la informacion antes de cada endpoint
@app.before_request
def log_request_info():
    ip = request.remote_addr
    method = request.method
    path = request.path
    data = None
    if request.is_json:
        data = request.get_json(silent=True)
    logger.info(
        f"IP: {ip} | METHOD: {method} | PATH: {path} | DATA: {data}"
    )

# -----------------------------------------------
# Handlers de errores globales
# -----------------------------------------------

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 NOT FOUND | PATH: {request.path}")
    return jsonify({
        "status_code": 404,
        "message": "Not Found",
        "data": "La ruta solicitada no existe"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    logger.warning(
        f"405 METHOD NOT ALLOWED | PATH: {request.path} | METHOD: {request.method}"
    )
    return jsonify({
        "status_code": 405,
        "message": "Method Not Allowed",
        "data": f"El método {request.method} no está permitido para esta ruta"
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    logger.exception("500 INTERNAL SERVER ERROR")
    return jsonify({
        "status_code": 500,
        "message": "Internal Server Error",
        "data": None
    }), 500

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    logger.warning(
        f"{error.code} HTTP ERROR | PATH: {request.path} | DESC: {error.description}"
    )
    return jsonify({
        "status_code": error.code,
        "message": error.name,
        "data": error.description
    }), error.code

# -----------------------------------------------
# Endpoints de la API
# -----------------------------------------------
@app.route('/personas', methods=["GET"])
def inicio():
    try:
        listado_personas = listar_personas_service()
        personas_json = [persona.to_json() for persona in listado_personas]        
        return jsonify({
            "status_code": 200,
            "message": "OK",
            "data": personas_json
        }), 200
    except Exception as error:
        logger.exception(f"EXCEPTION en {request.path}")
        return jsonify({
            "status_code": 500,
            "message": "Internal Server Error",
            "data": None
        }), 500
    
@app.route("/personas/buscar/<string:cedula>", methods=["GET"])
def buscar_persona(cedula):
    try:
        persona_buscada = buscar_persona_service(cedula)
        if persona_buscada is None:
            return jsonify({
                "status_code": 404,
                "message": "Not Found",
                "data": None
            }), 404
        else:
            return jsonify({
                "status_code": 200,
                "message": "OK",
                "data": persona_buscada.to_json()
            }), 200        
    except Exception as error:
        logger.exception(f"EXCEPTION en {request.path}")
        return jsonify({
            "status_code": 500,
            "message": "Internal Server Error",
            "data": None
        }), 500

@app.route("/personas/registrar", methods=["POST"])
def registrar():
    try:
        datos = request.get_json()
        campos_obligatorios = ["nombre_completo", "fecha_de_nacimiento", "email", "pais", "cedula"]

        # Validamos si los datos JSON son válidos
        datos, error_response = validar_json(campos_obligatorios)
        if error_response:
            return error_response
        
        # Validamos el formato del email
        if not validar_email(datos["email"]):
            return jsonify({
                "status_code": 422,
                "message": "Unprocessable Entity",
                "data": "El formato del email es inválido"
            }), 422

        # Validamos el formato de la fecha de nacimiento
        if not validar_fecha(datos["fecha_de_nacimiento"]):
            return jsonify({
                "status_code": 422,
                "message": "Unprocessable Entity",
                "data": "El formato de la fecha de nacimiento debe ser YYYY-MM-DD"
            }), 422
        
        # Creamos el objeto Persona atraves del servicio
        persona = registrar_persona_service(datos)
        db.session.add(persona)
        db.session.commit()

        return jsonify({    
            "status_code": 201,
            "message": "Created",
            "data": persona.to_json()
        }), 201
    except Exception as error:
        logger.exception(f"EXCEPTION en {request.path}")
        return jsonify({
            "status_code": 500,
            "message": "Internal Server Error",
            "data": None
        }), 500

@app.route("/personas/eliminar/<string:cedula>", methods=["DELETE"])
def eliminar(cedula):
    try:        
        persona_a_eliminar = eliminar_persona_service(cedula)
        if persona_a_eliminar:
            db.session.delete(persona_a_eliminar)
            db.session.commit()
            return jsonify({    
                "status_code": 200,
                "message": "OK",
                "data": f"La persona de cédula {cedula} fue eliminada"
            }), 200
        else:
            return jsonify({
                "status_code": 404,
                "message": "Not Found",
                "data": f"No existe persona con CI: {cedula}"
            }), 404
    except Exception as error:
        logger.exception(f"EXCEPTION en {request.path}")
        return jsonify({
            "status_code": 500,
            "message": "Internal Server Error",
            "data": None
        }), 500   

@app.route("/personas/actualizar", methods=["PUT"])
def actualizar_persona():
    try:
        datos = request.get_json()
        campos_obligatorios = ["nombre_completo", "fecha_de_nacimiento", "email", "pais", "cedula"]

        # Validamos los datos JSON
        datos, error_response = validar_json(campos_obligatorios)
        if error_response:
            return error_response

        # Validamos el formato del email
        if not validar_email(datos["email"]):
            return jsonify({
                "status_code": 422,
                "message": "Unprocessable Entity",
                "data": "El formato del email es inválido"
            }), 422

        # Validamos el formato de la fecha de nacimiento
        if not validar_fecha(datos["fecha_de_nacimiento"]):
            return jsonify({
                "status_code": 422,
                "message": "Unprocessable Entity",
                "data": "El formato de la fecha de nacimiento debe ser YYYY-MM-DD"
            }), 422

        # Actualizamos la persona a través del servicio
        persona = actualizar_persona_service(datos)
        if persona:
            return jsonify({
                "status_code": 200,
                "message": "OK",
                "data": persona.to_json()
            }), 200
        else:
            return jsonify({
                "status_code": 400,
                "message": "Bad Request",
                "data": "Datos no actualizados"
            }), 400        
    except Exception as error:
        logger.exception(f"EXCEPTION en {request.path}")
        return jsonify({
            "status_code": 500,
            "message": "Internal Server Error",
            "data": None
        }), 500   
    

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)    
    app.run(host="0.0.0.0", port=3000, debug=True)
