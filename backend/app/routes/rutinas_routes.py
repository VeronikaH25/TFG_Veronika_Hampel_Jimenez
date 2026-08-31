# app/routes/rutinas_routes.py
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_middleware import obtener_usuario_actual
from app.models.rutina import VotoRutina
from app.controllers.rutinas_controller import generar_rutina_fase2_controlador, generar_rutinas_para_usuario, registrar_voto_fase2, registrar_voto_usuario
from app.config.db import usuarios_collection 

router = APIRouter()

@router.post("/generar")
def endpoint_generar_rutinas(email: str = Depends(obtener_usuario_actual)):
    usuario = usuarios_collection.find_one({"email": email})
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    resultado = generar_rutinas_para_usuario(usuario)
    
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
        
    return resultado

@router.post("/votar")
def endpoint_votar_rutina(voto: VotoRutina, email: str = Depends(obtener_usuario_actual)):
    resultado = registrar_voto_usuario(email, voto.dict())
    return resultado

@router.post("/generar-inteligente")
def generar_rutina_inteligente(usuario_data: dict):
    try:
        # Llamamos al Bandit
        resultado = generar_rutina_fase2_controlador(usuario_data)
        
        if "error" in resultado:
            raise HTTPException(status_code=400, detail=resultado["error"])
            
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/votar-fase2")
def votar_rutina_fase2(voto_data: dict):
    try:
        email = voto_data.get("email_usuario")
        if not email:
            raise HTTPException(status_code=400, detail="Falta el email del usuario para registrar el voto de Fase 2.")
        
        return registrar_voto_fase2(email, voto_data)
    except Exception as e:
        import traceback
        print("\n ¡ERROR CRÍTICO EN VOTAR FASE 2! ")
        traceback.print_exc()  # Esto obligará a la terminal a mostrar el Traceback rojo entero
        raise HTTPException(status_code=500, detail=str(e))