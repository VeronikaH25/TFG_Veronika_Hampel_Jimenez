# app/controllers/perfil_controller.py
from app.config.db import usuarios_collection

def obtener_datos_usuario(email: str):
    """Busca al usuario pero filtra la contraseña para que no se envíe al frontend"""
    # Le pedimos a Mongo que  "Devuélveme todo menos estos dos campos"-> { "_id": 0, "password": 0 }
    usuario = usuarios_collection.find_one({"email": email}, {"_id": 0, "password": 0})
    
    if not usuario:
        return {"error": "Usuario no encontrado"}
    
    return usuario


def actualizar_datos_usuario(email: str, nuevos_datos: dict):
    # Filtramos los datos para no borrar lo que ya existe con valores nulos
    datos_a_actualizar = {k: v for k, v in nuevos_datos.items() if v is not None}
    
    if not datos_a_actualizar:
        return {"error": "No se han proporcionado datos para actualizar"}

    resultado = usuarios_collection.update_one(
        {"email": email},
        {"$set": datos_a_actualizar}
    )
    
    return {"exito": True, "cambios": resultado.modified_count}