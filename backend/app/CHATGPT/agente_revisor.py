import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# CONFIGURACIÓN
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# ==========================================
# MAPA DE GRUPOS MUSCULARES
# ==========================================
def cargar_mapa_grupos():
    try:
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        # Subimos una carpeta (..) y entramos a OPCION_2
        ruta_json = os.path.abspath(os.path.join(dir_actual, '..', 'OPCION_2', 'ejercicios.json'))
        
        with open(ruta_json, 'r', encoding='utf-8') as f:
            ejercicios = json.load(f)
            return {ej["nombre"].lower(): ej["grupo"] for ej in ejercicios}
    except FileNotFoundError as e:
        print(f" No se encontró ejercicios.json. Ruta buscada: {e.filename}")
        return {}

MAPA_GRUPOS = cargar_mapa_grupos()

# ==========================================
# NORMALIZAR Y VALIDAR REPS (FLEXIBLE)
# ==========================================
def validar_repeticiones(reps_knn_str, reps_ia):
    try:
        if "-" in str(reps_knn_str):
            min_k, max_k = map(int, str(reps_knn_str).split("-"))
        else:
            min_k = max_k = int(reps_knn_str)

        if isinstance(reps_ia, int):
            return min_k <= reps_ia <= max_k
        elif "-" in str(reps_ia):
            return str(reps_knn_str) == str(reps_ia)
        return str(reps_knn_str) == str(reps_ia)
    except:
        return False

# ==========================================
# VALIDADOR PYTHON (EL JUEZ JUSTO PERO LETAL)
# ==========================================
def validar_rutina_python(rutina_knn, rutina_ia):
    errores = []
    alertas = []

    # 1. Los días tienen que ser exactamente los mismos
    if set(rutina_knn.keys()) != set(rutina_ia.keys()):
        return False, ["Días distintos"], []

    for dia in rutina_knn:
        ejs_knn = rutina_knn[dia]
        ejs_ia = rutina_ia.get(dia, [])

        # 2. Tolerancia en el número de ejercicios (+/- 2 de margen)
        # Si la diferencia es absurda (ej. KNN pide 6 y la IA pone 2), lo fulminamos.
        if abs(len(ejs_knn) - len(ejs_ia)) > 2:
            errores.append(f"[{dia}] Diferencia absurda de ejercicios (KNN:{len(ejs_knn)}, IA:{len(ejs_ia)})")
            continue

        # Extraemos las "normas" del día según el KNN (usamos el primer ejercicio como guía)
        series_objetivo = ejs_knn[0]["series"] if ejs_knn else 4
        reps_objetivo = ejs_knn[0]["reps"] if ejs_knn else "8-12"
        
        # Sacamos qué músculos toca entrenar este día según el KNN
        grupos_esperados = set([MAPA_GRUPOS.get(e["ejercicio"].lower()) for e in ejs_knn if MAPA_GRUPOS.get(e["ejercicio"].lower())])

        ejercicios_desconocidos = []

        # 3. Inspección exhaustiva de la IA (Ejercicio por Ejercicio)
        for e_ia in ejs_ia:
            
            # --- FILTRO DE MATEMÁTICAS ---
            if str(e_ia.get("series", "")) != str(series_objetivo):
                errores.append(f"[{dia}] '{e_ia['ejercicio']}': Series mal (IA puso {e_ia.get('series')}, KNN exigía {series_objetivo})")
            
            if not validar_repeticiones(reps_objetivo, e_ia.get("reps")):
                errores.append(f"[{dia}] '{e_ia['ejercicio']}': Reps mal (IA puso {e_ia.get('reps')}, KNN exigía {reps_objetivo})")

            # --- FILTRO DE ALUCINACIONES MUSCULARES ---
            nombre = e_ia["ejercicio"].lower()
            grupo = MAPA_GRUPOS.get(nombre)

            if grupo:
                # El ejercicio existe. ¿Toca entrenarlo hoy?
                if grupo not in grupos_esperados:
                    errores.append(f"[{dia}] Alucinación muscular: Hoy tocaba {list(grupos_esperados)} pero IA metió '{grupo}' ({e_ia['ejercicio']})")
            else:
                # El ejercicio NO existe en nuestro JSON. Alerta para el Jefe (LLM).
                ejercicios_desconocidos.append(e_ia["ejercicio"])

        # Si hubo ejercicios inventados/sinónimos, preparamos la alerta
        if ejercicios_desconocidos:
            alertas.append({
                "dia": dia,
                "ejercicios_desconocidos": ejercicios_desconocidos,
                "grupos_que_deberian_ser": list(grupos_esperados)
            })

    return len(errores) == 0, errores, alertas

# ==========================================
# AUDITOR LLM (JUEZ BIOMECÁNICO)
# ==========================================
def auditor_llm(rutina_ia, nivel, alertas):
    prompt_sistema = """
    Eres un auditor experto en entrenamiento.
    El sistema Python ha detectado ejercicios que no están en su base de datos o que usan sinónimos.
    
    Tu tarea:
    Revisa las 'ALERTAS'. Cada alerta indica los ejercicios que Python no entendió y los grupos musculares que se DEBEN entrenar ese día.
    1. ¿Los ejercicios desconocidos actúan como SINÓNIMOS válidos o trabajan los grupos musculares exigidos?
    2. ¿Tienen sentido para un nivel intermedio/avanzado/principiante?
    
    Si los ejercicios cubren correctamente los grupos y no son peligrosos, aprueba.
    Si la IA se inventó algo que no trabaja NINGUNO de los músculos esperados (alucinación grave), rechaza.

    Responde ÚNICAMENTE con este JSON:
    {
        "aprobado": true o false,
        "motivos": ["Explicación del motivo"]
    }
    """

    prompt_usuario = f"Nivel: {nivel}\n\nALERTAS:\n{json.dumps(alertas, ensure_ascii=False)}\n\nRUTINA COMPLETA:\n{json.dumps(rutina_ia, ensure_ascii=False)}"

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            response_format={ "type": "json_object" },
            temperature=0.0
        )
        return json.loads(res.choices[0].message.content)
    except Exception as e:
        return {"aprobado": False, "motivos": [f"Error de conexión: {str(e)}"]}

# ==========================================
# ORQUESTADOR HÍBRIDO
# ==========================================
def revisar_hibrido(rutina_knn, rutina_ia, nivel):
    es_valida, errores, alertas = validar_rutina_python(rutina_knn, rutina_ia)

    if not es_valida:
        return {"aprobado": False, "fase": "python", "errores": errores}

    if alertas:
        resultado_llm = auditor_llm(rutina_ia, nivel, alertas)
        if not resultado_llm.get("aprobado", False):
            return {"aprobado": False, "fase": "llm", "detalle": resultado_llm.get("motivos", [])}

    return {"aprobado": True, "detalle": "Todo correcto, grupos y estructura validados."}