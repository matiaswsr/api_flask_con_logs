from flask import request, jsonify
from typing import List, Tuple
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def validar_json(campos_obligatorios: List[str]) -> Tuple[dict, object]:
    """
    Valida que request.get_json() exista y contenga los campos obligatorios.
    
    Retorna:
        datos (dict): JSON seguro
        response (jsonify/None): Si hay error, devuelve respuesta lista para return
    """
    datos = request.get_json(silent=True)
    
    if datos is None:
        return None, jsonify({
            "status_code": 400,
            "message": "Bad Request",
            "data": "El cuerpo debe ser JSON"
        }), 400
    
    faltantes = [campo for campo in campos_obligatorios if campo not in datos]
    
    if faltantes:
        return None, jsonify({
            "status_code": 422,
            "message": "Unprocessable Entity",
            "data": f"Faltan campos obligatorios: {faltantes}"
        }), 422    
    return datos, None

def validar_email(email: str) -> bool:
    # Valida si el correo electrónico tiene el formato correcto.
    return bool(EMAIL_REGEX.fullmatch(email))

def validar_fecha(fecha: str) -> bool:
    # Valida que la fecha tenga el formato YYYY-MM-DD
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False