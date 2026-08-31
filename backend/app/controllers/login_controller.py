# app/controllers/login_controller.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config.db import usuarios_collection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "mi_clave_super_secreta_para_el_tfg_cambiala_luego"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def procesar_login(credenciales):
    """Lógica exclusiva para el inicio de sesión"""
    usuario_bd = usuarios_collection.find_one({"email": credenciales.email})
    if not usuario_bd:
        return {"error": "Email o contraseña incorrectos"}

    if not pwd_context.verify(credenciales.password, usuario_bd["password"]):
        return {"error": "Email o contraseña incorrectos"}

    # Generar el Token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": usuario_bd["email"], "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "exito": True,
        "token": token,
        "nombre": usuario_bd["nombre"]
    }