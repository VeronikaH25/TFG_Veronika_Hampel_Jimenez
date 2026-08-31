import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# 1. CONFIGURACIÓN DE ENTORNO
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ==========================================
# 2. AGENTE CREADOR (Con Reglas de Split del KNN)
# ==========================================
def agente_creador(edad, peso, nivel, objetivo, dias, feedback_errores=None):
    print(f"\n [IA]: Generando propuesta estructurada para el usuario")
    
    # PROMPT DE SISTEMA: Aquí le metemos las reglas duras de tu código generador
    prompt_sistema = """
    Eres un experto en biomecánica y el motor generativo de una app de entrenamiento.
    Eres un sistema determinista. NO eres creativo. NO puedes improvisar.
    
    Tu tarea es generar una rutina EXACTA siguiendo reglas estrictas.
    
    ==========================================
    REGLAS OBLIGATORIAS (NO SE PUEDEN ROMPER)
    ==========================================
    
    1. SERIES Y REPS (OBLIGATORIO):
    - Fuerza → EXACTAMENTE 5 series y entre 3 y 5 reps
    - Hipertrofia → EXACTAMENTE 4 series y entre 8 y 12 reps
    - Perdida_Peso → EXACTAMENTE 3 series y entre 15 y 20 reps

    PROHIBIDO usar otros valores

    2. SPLIT POR DÍAS (OBLIGATORIO):
    
    - Si entrena 3 días seguir EXACTAMENTE esta division: 
        * dia_1: Pecho (3 ej.), Tríceps (2 ej.)
        * dia_2: Espalda (3 ej.), Bíceps (2 ej.), Hombros (2 ej.)
        * dia_3: Piernas (3 ej.), Gemelos (1 ej.), Core (1 ej.)
    - Si entrena 4 días seguir EXACTAMENTE esta division:
        * dia_1: Pecho (3 ej.), Tríceps (3 ej.)
        * dia_2: Espalda (3 ej.), Bíceps (3 ej.)
        * dia_3: Piernas (4 ej.), Gemelos (2 ej.)
        * dia_4: Hombros (4 ej.), Core (2 ej.)
    - Si entrena 5 días seguir EXACTAMENTE esta division:
        * dia_1: Pecho (4 ej.)
        * dia_2: Espalda (4 ej.)
        * dia_3: Piernas (4 ej.), Gemelos (2 ej.)
        * dia_4: Hombros (4 ej.), Core (2 ej.)
        * dia_5: Bíceps (3 ej.), Tríceps (3 ej.)
        
    PROHIBIDO mezclar grupos
    PROHIBIDO cambiar cantidades

    REGLAS DE NIVEL:
    - Selecciona ejercicios adecuados para el nivel solicitado (Principiante, Intermedio o Avanzado).

    3. FORMATO JSON (OBLIGATORIO):

    - Clave 1: "plan_interno"
        - Aquí debes escribir tu razonamiento de conteo.
        - Debes indicar:
            * número de ejercicios por grupo
            * suma total por día
            * verificación final

    - Clave 2: "rutina"

    - Días: "dia_1", "dia_2", etc
    - Cada ejercicio debe tener EXACTAMENTE:
        - "ejercicio"
        - "series"
        - "reps"

    PROHIBIDO usar "nombre"
    PROHIBIDO añadir otras claves fuera de estas dos
    
    4. VALIDACIÓN FINAL (CRÍTICO):

    Antes de responder:
    - Verifica número de ejercicios por día
    - Verifica series/reps correctos
    - Verifica formato exacto

    Si algo NO cumple → corrígelo antes de responder

    ------------------------------------------
    5. PROCESO OBLIGATORIO (MUY IMPORTANTE):

    Debes seguir ESTE ORDEN:

    Paso 1: Generar internamente la estructura del día con los grupos musculares correctos y número exacto de ejercicios.

    Paso 2: Asignar ejercicios válidos a cada grupo respetando cantidades.

    Paso 3: Aplicar series y reps EXACTAS según objetivo.

    Paso 4: Construir JSON final.

    Paso 5: Validar TODO antes de responder.

    NO puedes saltarte pasos.
    NO puedes responder sin validar.
    
    6. CONTROL DE DISTRIBUCIÓN (CRÍTICO):

    Cada día DEBE contener exactamente el número de ejercicios indicado.

    Ejemplo para 3 días:

    - dia_1 → EXACTAMENTE 5 ejercicios (3 pecho + 2 tríceps)
    - dia_2 → EXACTAMENTE 7 ejercicios (3 espalda + 2 bíceps + 2 hombros)
    - dia_3 → EXACTAMENTE 5 ejercicios (3 piernas + 1 gemelos + 1 core)

    Si el número no coincide, la respuesta es inválida.
    
    7. USO OBLIGATORIO DE "plan_interno":

    Debes completar primero "plan_interno" antes de generar la rutina.

    En "plan_interno" debes:
    - Escribir cuántos ejercicios hay por grupo en cada día
    - Calcular el total de ejercicios por día
    - Verificar que coincide EXACTAMENTE con las reglas

    NO puedes generar "rutina" sin haber validado correctamente en "plan_interno".

    Responde SOLO con JSON válido. Nada más.
    
    
    """
    
    # Inyectamos el feedback si existe
    prompt_feedback = ""
    if feedback_errores:
        prompt_feedback = f"\n\n ATENCIÓN - CORRECCIÓN OBLIGATORIA \nTu intento anterior falló por los siguientes motivos:\n{feedback_errores}\n\nDEBES corregir estos errores en tu nueva respuesta sin saltarte ninguna regla."
        
        
    prompt_usuario = f"""
    Crea la rutina para este usuario:
    - Nivel: {nivel}
    - Objetivo: {objetivo}
    - Días a la semana: {dias}
    - Datos adicionales: Edad {edad}, Peso {peso}kg
    {prompt_feedback}
    """

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            response_format={ "type": "json_object" },
            timeout=15.0
        )
        
        contenido = json.loads(respuesta.choices[0].message.content)
        
        return contenido

    except Exception as e:
        print(f" [CRÍTICO] Error en la API de OpenAI (Saldo/Caída/Timeout): {e}")
        
        return {"error_api_critico": True, "detalle": str(e)}

# --- PRUEBA DE FUNCIONAMIENTO ---
if __name__ == "__main__":
    # Exactamente los mismos 5 parámetros y tipos que en obtener_rutina() del KNN
    resultado = agente_creador(25, 80, 'Intermedio', 'Fuerza', 3)
    
    if resultado:
        print("\n Rutina generada por IA:")
        print(json.dumps(resultado["rutina"], indent=2, ensure_ascii=False))