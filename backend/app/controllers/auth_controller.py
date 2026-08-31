# app/controllers/auth_controller.py
from passlib.context import CryptContext
from app.config.db import usuarios_collection

# Configuramos el encriptador de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_hash_password(password: str):
    """Convierte la contraseña en texto ilegible"""
    return pwd_context.hash(password)

def registrar_nuevo_usuario(usuario_data):
    """Lógica principal de registro"""
    
    # 1. Comprobar si el email ya existe en la base de datos
    usuario_existente = usuarios_collection.find_one({"email": usuario_data.email})
    if usuario_existente:
        return {"error": "Este email ya está registrado"}

    # 2. Encriptar la contraseña
    password_encriptada = crear_hash_password(usuario_data.password)

    # 3. Preparar el documento final para la base de datos
    nuevo_usuario = usuario_data.dict()
    nuevo_usuario["password"] = password_encriptada # Sobrescribimos la original por el hash
    nuevo_usuario["rutina_asignada"] = None         # Hueco vacío para el futuro Orquestador

    # 4. Guardar en Mongo 
    resultado = usuarios_collection.insert_one(nuevo_usuario)
    
    return {"exito": True, "id_mongo": str(resultado.inserted_id)}