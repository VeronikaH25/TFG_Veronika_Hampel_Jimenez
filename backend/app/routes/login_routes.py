# app/routes/login_routes.py
from fastapi import APIRouter, HTTPException
from app.models.usuario import UsuarioLogin
from app.controllers.login_controller import procesar_login

router = APIRouter(prefix="/api/login", tags=["Login"])

@router.post("/")
def login(credenciales: UsuarioLogin):
    resultado = procesar_login(credenciales)
    if "error" in resultado:
        raise HTTPException(status_code=401, detail=resultado["error"])
    
    return {
        "mensaje": "Login exitoso",
        "access_token": resultado["token"],
        "token_type": "bearer",
        "usuario_nombre": resultado["nombre"]
    }