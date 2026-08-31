from datetime import datetime, timezone
from app.CHATGPT.orquestador import generar_opciones_fase1, generar_rutina_fase2
from app.config.db import usuarios_collection, votos_collection

def generar_rutinas_para_usuario(usuario_dict: dict):
    campos_requeridos = ["edad", "peso", "nivel", "objetivo", "dias_entreno"]
    
    if not all(usuario_dict.get(campo) for campo in campos_requeridos):
        return {"error": "Faltan datos físicos. El usuario debe completar su perfil primero."}

    datos_orquestador = {
        "edad": int(usuario_dict["edad"]),
        "peso": float(usuario_dict["peso"]),
        "nivel": usuario_dict["nivel"],
        "objetivo": usuario_dict["objetivo"],
        "dias_entreno": int(usuario_dict["dias_entreno"])
    }

    opciones = generar_opciones_fase1(datos_orquestador)
    return opciones

def registrar_voto_usuario(email: str, voto_data: dict):
    fecha_actual = datetime.utcnow()
    
    # 1. Documento para la Opción 1
    registro_opcion1 = {
        "email_usuario": email,
        "origen": voto_data["origen_opcion_1"],
        "puntuacion": voto_data["puntuacion_opcion_1"],
        "elegido": voto_data["origen_elegido"] == voto_data["origen_opcion_1"],
        "fecha_voto": fecha_actual
    }
    
    # 2. Documento para la Opción 2
    registro_opcion2 = {
        "email_usuario": email,
        "origen": voto_data["origen_opcion_2"],
        "puntuacion": voto_data["puntuacion_opcion_2"],
        "elegido": voto_data["origen_elegido"] == voto_data["origen_opcion_2"],
        "fecha_voto": fecha_actual
    }
    
    # Guardamos ambos registros en la colección de votos con una sola operación
    votos_collection.insert_many([registro_opcion1, registro_opcion2])
    
    # 3. Guardamos la rutina seleccionada en el perfil del usuario para su vista activa
    usuarios_collection.update_one(
        {"email": email},
        {"$set": {"rutina_activa": voto_data["rutina_json"]}}
    )
    
    return {"exito": True, "mensaje": "Ambas puntuaciones han sido registradas con éxito."}

def generar_rutina_fase2_controlador(usuario_dict: dict):
    """Endpoint de control para la Fase 2 (Multi-Armed Bandit)"""
    campos_requeridos = ["edad", "peso", "nivel", "objetivo", "dias_entreno"]
    if not all(usuario_dict.get(campo) for campo in campos_requeridos):
        return {"error": "Faltan datos físicos. El usuario debe completar su perfil primero."}
        
    datos_orquestador = {
        "edad": int(usuario_dict["edad"]),
        "peso": float(usuario_dict["peso"]),
        "nivel": usuario_dict["nivel"],
        "objetivo": usuario_dict["objetivo"],
        "dias_entreno": int(usuario_dict["dias_entreno"])
    }
    
    email_usuario = usuario_dict.get("email", "anonimo@tfg.com")
    
    # Delegamos directamente en la nueva función del orquestador
    return generar_rutina_fase2(datos_orquestador, email_usuario)

def registrar_voto_fase2(email: str, voto_data: dict):
    """Registra el voto de la Fase 2 y activa la rutina para que el Bandit siga aprendiendo."""
    fecha_actual = datetime.now(timezone.utc)
    
    # 1. Guardamos el voto para el algoritmo que ha ganado
    registro_voto = {
        "email_usuario": email,
        "origen": voto_data["algoritmo_utilizado"], # 'knn' o 'ia'
        "puntuacion": voto_data["puntuacion"],
        "fase": 2, # Etiqueta para saber que viene del Bandit
        "fecha_voto": fecha_actual
    }
    votos_collection.insert_one(registro_voto)
    
    # 2. Guardamos la rutina en el perfil del usuario (para el Dashboard)
    usuarios_collection.update_one(
        {"email": email},
        {"$set": {"rutina_activa": voto_data["rutina_json"]}}
    )
    
    return {"exito": True, "mensaje": "Voto de Fase 2 registrado y rutina activada."}