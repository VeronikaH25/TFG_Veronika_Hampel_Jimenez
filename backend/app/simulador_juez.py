import os
import sys
import json
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
from openai import OpenAI

# EL TRUCO DEFINITIVO: Calculamos la ruta de la carpeta padre ('backend') 
# para que Python entienda todos los 'from app.loquesea...'
ruta_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ruta_backend)

# Ahora sí, importamos con 'app.' delante, igual que en el resto de tu backend
from app.CHATGPT.orquestador import generar_opciones_fase1
from app.config.db import votos_collection

# Cargamos entorno y cliente de OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generar_perfil_aleatorio():
    """Crea un usuario distinto cada vez que se le llama con datos biomecánicos coherentes"""
    niveles = ["Principiante", "Intermedio", "Avanzado"]
    objetivos = ["Hipertrofia", "Fuerza", "Perdida_Peso"]
    
    return {
        "edad": random.randint(18, 65), # Edades entre 18 y 65 años
        "peso": round(random.uniform(50.0, 110.0), 1), # Pesos entre 50kg y 110kg (con 1 decimal)
        "nivel": random.choice(niveles),
        "objetivo": random.choice(objetivos),
        "dias_entreno": random.randint(3, 5) # Entre 3 y 5 días a la semana
    }

def evaluar_con_juez_ia(perfil, opcion_1, opcion_2):
    """Llama a GPT-4o-mini (o el modelo que uses) para que actúe de juez ciego"""
    
    prompt_sistema = """Eres un juez experto en ciencias del deporte, biomecánica y entrenamiento de fuerza.
    Tu objetivo es evaluar dos rutinas de gimnasio generadas por diferentes algoritmos para un usuario específico.
    Debes puntuar cada opción del 1 al 5 basándote ESTRICTAMENTE en:
    1. Volumen de entrenamiento razonable (ni muy poco, ni sobreentrenamiento).
    2. Equilibrio muscular y selección coherente de ejercicios.
    3. Adaptación al nivel y objetivo del usuario.
    
    Devuelve ÚNICAMENTE un JSON con este formato exacto, sin markdown ni explicaciones:
    {"puntuacion_1": nota_del_1_al_5, "puntuacion_2": nota_del_1_al_5}
    """
    
    prompt_usuario = f"""
    Perfil del usuario: {json.dumps(perfil)}
    
    RUTINA OPCIÓN 1 ({opcion_1['origen']}): 
    {json.dumps(opcion_1['rutina'])}
    
    RUTINA OPCIÓN 2 ({opcion_2['origen']}): 
    {json.dumps(opcion_2['rutina'])}
    """
    
    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini", # Usamos el modelo rápido/barato para no fundir saldo
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.3
        )
        # Limpiamos posibles formatos raros y convertimos a diccionario
        texto_limpio = respuesta.choices[0].message.content.strip().replace("```json", "").replace("```", "")
        return json.loads(texto_limpio)
    except Exception as e:
        print(f" Error del Juez IA: {e}")
        return {"puntuacion_1": 3, "puntuacion_2": 3} # En caso de error, empate neutro

def ejecutar_simulacion(numero_pruebas=10):
    print(f" Iniciando simulación MLOps: Generando {numero_pruebas} evaluaciones...\n")
    
    for i in range(numero_pruebas):
        perfil = generar_perfil_aleatorio()
        print(f"--- Prueba {i+1}/{numero_pruebas} | Perfil: {perfil['nivel']}, {perfil['objetivo']}, {perfil['dias_entreno']} días ---")
        
        print("    Generando rutinas con el Orquestador...")
        opciones = generar_opciones_fase1(perfil)
        
        op1 = opciones["opcion_1"]
        op2 = opciones["opcion_2"]
        
        # EL CORTAFUEGOS DEL JUEZ: Si son idénticas, ha habido Fallback
        if op1["rutina"] == op2["rutina"]:
            print("   ⚠️ Fallback detectado: La IA fracasó los 3 intentos. Evaluando automáticamente sin OpenAI.")
            veredicto = {
                "puntuacion_1": 1 if op1["origen"] == "ia" else 4,
                "puntuacion_2": 1 if op2["origen"] == "ia" else 4
            }
        else:
            print("   ⚖️  El Juez IA está evaluando las propuestas...")
            veredicto = evaluar_con_juez_ia(perfil, op1, op2)
            
        print(f"    Veredicto -> Opción 1 ({op1['origen']}): {veredicto['puntuacion_1']} ⭐ | Opción 2 ({op2['origen']}): {veredicto['puntuacion_2']} ⭐")
        
        # Determinamos el ganador simulado
        ganador = op1["origen"] if veredicto["puntuacion_1"] >= veredicto["puntuacion_2"] else op2["origen"]
        
        fecha_actual = datetime.now(timezone.utc)
        email_falso = f"simulador_juez_{int(fecha_actual.timestamp())}@tfg.com"
        
        doc_op1 = {
            "email_usuario": email_falso,
            "origen": op1["origen"],
            "puntuacion": veredicto["puntuacion_1"],
            "elegido": ganador == op1["origen"],
            "fecha_voto": fecha_actual
        }
        
        doc_op2 = {
            "email_usuario": email_falso,
            "origen": op2["origen"],
            "puntuacion": veredicto["puntuacion_2"],
            "elegido": ganador == op2["origen"],
            "fecha_voto": fecha_actual
        }
        
        votos_collection.insert_many([doc_op1, doc_op2])
        print("    Votos guardados en MongoDB.\n")

if __name__ == "__main__":
    # Ejecutamos una tanda pequeña por defecto
    ejecutar_simulacion(numero_pruebas=200)