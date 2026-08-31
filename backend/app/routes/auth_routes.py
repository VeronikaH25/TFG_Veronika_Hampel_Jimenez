# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, status
from app.models.usuario import UsuarioRegistro
from app.controllers.auth_controller import registrar_nuevo_usuario

# Creamos un "mini-servidor" de rutas solo para cosas de autenticación
router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registro(usuario: UsuarioRegistro):
    
    # Delegación de la lógica de negocio al controlador
    resultado = registrar_nuevo_usuario(usuario)

    # Si nos devuelve un error, le lanzamos un 400 a la web
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])

    # Si todo va bien, servimos la respuesta de éxito
    return {
        "mensaje": "¡Usuario registrado con éxito!", 
        "id": resultado["id_mongo"]
    }