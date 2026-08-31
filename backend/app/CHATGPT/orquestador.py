# orquestador.py
import random

from datetime import datetime, timezone
# Importamos la nueva colección
from app.config.db import auditoria_collection

# Importamos a nuestros músicos
from app.OPCION_2.knn_modelo import obtener_rutina
from app.CHATGPT.agente_ia import agente_creador
from app.CHATGPT.agente_revisor import revisar_hibrido

from datetime import datetime, timezone
# Importamos la nueva colección
from app.config.db import auditoria_collection

# El cerebro del Bandit
from app.analytics.bandit import seleccionar_modelo_bandit

def generar_rutina_ia_validada(datos_usuario, rutina_knn, max_intentos=3):
    feedback_previo = None
    historial_errores = [] # Aquí guardaremos la "basura" que hace la IA
    
    for intento in range(max_intentos):
        print(f"\n [ORQUESTADOR] Generación IA - Intento {intento + 1}/{max_intentos}...")
        
        resultado_ia = agente_creador(
            edad=datos_usuario['edad'],
            peso=datos_usuario['peso'],
            nivel=datos_usuario['nivel'],
            objetivo=datos_usuario['objetivo'],
            dias=datos_usuario['dias_entreno'],
            feedback_errores=feedback_previo
        )
        
        #  (Fail-Fast) 
        if resultado_ia and resultado_ia.get("error_api_critico"):
            print(" [ORQUESTADOR] Abortando reintentos por fallo en el servidor de IA.")
            historial_errores.append({"intento": intento + 1, "error": resultado_ia["detalle"]})
            break # Salimos del bucle FOR inmediatamente y no gastamos los 3 intentos.
        
        if not resultado_ia or "rutina" not in resultado_ia:
            error_msg = "Error crítico de formato: JSON inválido o sin clave 'rutina'."
            historial_errores.append({"intento": intento + 1, "error": error_msg})
            feedback_previo = error_msg
            continue
            
        rutina_ia = resultado_ia["rutina"]
        
        print(" [ORQUESTADOR] Pasando la rutina de IA por el Agente Revisor...")
        veredicto = revisar_hibrido(rutina_knn, rutina_ia, datos_usuario['nivel'])
        
        if veredicto.get("aprobado"):
            print(" [ORQUESTADOR] ¡El Revisor ha APROBADO la rutina de la IA!")
            
            # GUARDAMOS EL LOG DE ÉXITO EN MONGODB
            auditoria_collection.insert_one({
                "perfil_usuario": datos_usuario,
                "resultado_final": "aprobado",
                "intentos_consumidos": intento + 1,
                "historial_errores": historial_errores,
                "fecha": datetime.now(timezone.utc)
            })
            
            return rutina_ia
            
        else:
            errores = veredicto.get("errores", veredicto.get("detalle", "Error estructural biomecánico."))
            print(f" [ORQUESTADOR] El Revisor RECHAZÓ la rutina. Motivos:\n{errores}")
            
            # Guardamos el error de esta ronda
            historial_errores.append({"intento": intento + 1, "error": errores})
            feedback_previo = f"- {errores}"
            
    print(" [ORQUESTADOR] Límite de intentos alcanzado. La IA no logró una rutina válida.")
    print(" [ORQUESTADOR] Devolviendo rutina k-NN como medida de seguridad extrema.")
    
    # GUARDAMOS EL LOG DE FRACASO (FALLBACK) EN MONGODB
    auditoria_collection.insert_one({
        "perfil_usuario": datos_usuario,
        "resultado_final": "fallback_knn",
        "intentos_consumidos": max_intentos,
        "historial_errores": historial_errores,
        "fecha": datetime.now(timezone.utc)
    })
    
    return rutina_knn


def generar_opciones_fase1(datos_usuario):
    """
    Función principal que llamaremos desde nuestro endpoint de FastAPI en la web.
    Orquesta la creación de las dos opciones para el A/B Testing.
    """
    print(f" [ORQUESTADOR] Iniciando Fase 1 (A/B Testing) para usuario con objetivo: {datos_usuario['objetivo']}")

    # 1. Generamos la rutina base determinista (Matemáticas puras)
    rutina_knn = obtener_rutina(
        edad=datos_usuario['edad'],
        peso=datos_usuario['peso'],
        nivel=datos_usuario['nivel'],
        objetivo=datos_usuario['objetivo'],
        dias=datos_usuario['dias_entreno']
    )
    
    # 2. Generamos la rutina IA (Probabilística) pasándola por el bucle de validación
    rutina_ia = generar_rutina_ia_validada(datos_usuario, rutina_knn)

    # 3. Mezclamos el orden para que el usuario no sepa nunca cuál es cuál
    # (Un buen A/B testing tiene que ser ciego)
    opciones = [
        {"origen": "knn", "rutina": rutina_knn},
        {"origen": "ia", "rutina": rutina_ia}
    ]
    random.shuffle(opciones)

    # 4. Empaquetamos todo para mandarlo al Frontend
    return {
        "opcion_1": opciones[0],
        "opcion_2": opciones[1]
    }
    
def generar_rutina_fase2(datos_usuario, email_usuario: str):
    """
    FASE 2: Generación Inteligente mediante Multi-Armed Bandit (Devuelve una única opción).
    """
    print(f"🔸 [ORQUESTADOR] Iniciando Fase 2 (Bandit) para objetivo: {datos_usuario['objetivo']}")
    
    # 1. El Bandit toma la decisión consultando el histórico de MongoDB
    modelo_ganador, estrategia_usada = seleccionar_modelo_bandit(email_usuario)
    
    # 2. Se ejecuta la ruta del brazo seleccionado por el algoritmo
    if modelo_ganador == "knn":
        rutina_final = obtener_rutina(
            edad=datos_usuario['edad'],
            peso=datos_usuario['peso'],
            nivel=datos_usuario['nivel'],
            objetivo=datos_usuario['objetivo'],
            dias=datos_usuario['dias_entreno']
        )
    else:
        # Si el Bandit elige IA, generamos el molde k-NN requerido por el Revisor
        rutina_base_knn = obtener_rutina(
            edad=datos_usuario['edad'],
            peso=datos_usuario['peso'],
            nivel=datos_usuario['nivel'],
            objetivo=datos_usuario['objetivo'],
            dias=datos_usuario['dias_entreno']
        )
        rutina_final = generar_rutina_ia_validada(datos_usuario, rutina_base_knn)
        
    return {
        "algoritmo_utilizado": modelo_ganador,
        "estrategia": estrategia_usada,
        "rutina": rutina_final
    }