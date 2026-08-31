# app/routes/perfil_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_middleware import obtener_usuario_actual
from app.controllers.perfil_controller import obtener_datos_usuario
from app.controllers.perfil_controller import actualizar_datos_usuario
from app.models.usuario import UsuarioUpdate # Importa el nuevo modelo

router = APIRouter(prefix="/api/usuarios", tags=["Perfil de Usuario"])

@router.get("/me")
def mi_perfil(email: str = Depends(obtener_usuario_actual)):
    # Si el código llega a esta línea, significa que (obtener_usuario_actual)
    # ha validado el token con éxito y nos ha devuelto el email.
    
    datos = obtener_datos_usuario(email)
    
    if "error" in datos:
        raise HTTPException(status_code=404, detail=datos["error"])
    
    return datos


@router.put("/actualizar")
def actualizar_perfil(datos: UsuarioUpdate, email: str = Depends(obtener_usuario_actual)):
    resultado = actualizar_datos_usuario(email, datos.dict())
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return {"mensaje": "Perfil actualizado correctamente"}