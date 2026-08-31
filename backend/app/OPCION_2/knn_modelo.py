import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import json
import random
import os


# ==========================================
# 1. CARGAR DATOS Y CATALOGO (Rutas Absolutas)
# ==========================================
DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_EJERCICIOS = os.path.join(DIR_ACTUAL, 'ejercicios.json')
RUTA_DATASET = os.path.join(DIR_ACTUAL, 'gym_dataset_plantillas.csv')

def cargar_catalogo():
    with open(RUTA_EJERCICIOS, 'r', encoding='utf-8') as f:
        return json.load(f)

DB_EJERCICIOS = cargar_catalogo()
df = pd.read_csv(RUTA_DATASET, sep=';')

nivel_map = {'Principiante': 0, 'Intermedio': 1, 'Avanzado': 2}
objetivo_map = {'Perdida_Peso': 0, 'Hipertrofia': 1, 'Fuerza': 2}

df['Nivel_Num'] = df['Nivel'].map(nivel_map)
df['Objetivo_Num'] = df['Objetivo'].map(objetivo_map)

X = df[['Edad', 'Peso_kg', 'Nivel_Num', 'Objetivo_Num', 'Dias_Entrenamiento']]
y = df['Plantilla_JSON']

# ==========================================
# 2. ENTRENAMIENTO DEL MODELO (80/20)
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=X['Objetivo_Num']
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

knn = NearestNeighbors(n_neighbors=1, metric='euclidean')
knn.fit(X_train_scaled)

# ==========================================
# 3. EVALUACION Y GENERACION DE GRAFICOS
# ==========================================
def evaluar_y_graficar():
    print("=== EVALUACION Y GENERACION DE GRAFICOS ===")
    aciertos = 0
    total_test = len(X_test_scaled)
    
    y_true_objetivo = []
    y_pred_objetivo = []

    for i in range(total_test):
        usuario_incognito = X_test_scaled[i].reshape(1, -1)
        distancias, indices = knn.kneighbors(usuario_incognito)
        idx_vecino = indices[0][0]
        
        vecino_encontrado = X_train.iloc[idx_vecino]
        usuario_real = X_test.iloc[i]

        y_true_objetivo.append(usuario_real['Objetivo_Num'])
        y_pred_objetivo.append(vecino_encontrado['Objetivo_Num'])

        if (vecino_encontrado['Nivel_Num'] == usuario_real['Nivel_Num'] and 
            vecino_encontrado['Objetivo_Num'] == usuario_real['Objetivo_Num']):
            aciertos += 1

    precision = (aciertos / total_test) * 100
    print(f" Precision Logica: {precision}%\n")

    # --- Grafico 1: Matriz de Confusion ---
    cm = confusion_matrix(y_true_objetivo, y_pred_objetivo)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Pérdida Peso', 'Hipertrofia', 'Fuerza'],
                yticklabels=['Pérdida Peso', 'Hipertrofia', 'Fuerza'])
    plt.title('Matriz de Confusión del KNN', fontsize=14, fontweight='bold')
    plt.xlabel('Predicción del Modelo', fontsize=12)
    plt.ylabel('Valor Real', fontsize=12)
    plt.tight_layout()
    plt.savefig('matriz_confusion_TFG.png')
    plt.close()
    print(" Gráfico guardado: 'matriz_confusion_TFG.png'")

    # --- Grafico 2: Curva de Validacion ---
    k_valores = list(range(1, 15))
    precisiones = []
    
    for k in k_valores:
        knn_prueba = NearestNeighbors(n_neighbors=k, metric='euclidean')
        knn_prueba.fit(X_train_scaled)
        aciertos_k = 0
        
        for i in range(total_test):
            usr = X_test_scaled[i].reshape(1, -1)
            # Obtenemos los indices de los K vecinos mas cercanos
            indices_k = knn_prueba.kneighbors(usr)[1][0]
            
            # Hacemos una "votacion" entre los K vecinos encontrados
            votos_objetivo = [X_train.iloc[idx]['Objetivo_Num'] for idx in indices_k]
            
            # El objetivo predicho es el que mas se repite entre los vecinos
            prediccion = max(set(votos_objetivo), key=votos_objetivo.count)
            
            # Comparamos la prediccion con la realidad
            if prediccion == X_test.iloc[i]['Objetivo_Num']:
                aciertos_k += 1
                
        precisiones.append((aciertos_k / total_test) * 100)

    plt.figure(figsize=(10, 6))
    plt.plot(k_valores, precisiones, marker='o', linestyle='-', color='#2c3e50', 
             linewidth=2.5, markersize=8, markerfacecolor='#e74c3c')
    
    plt.title('Curva de Validación (Precisión vs Número de Vecinos K)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Número de Vecinos (K)', fontsize=13, labelpad=15)
    plt.ylabel('Precisión (%)', fontsize=13, labelpad=15)
    
    plt.xticks(k_valores, fontsize=11)
    plt.yticks(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.annotate(f'K=1\n({precisiones[0]}%)', 
                 xy=(1, precisiones[0]), 
                 xytext=(2, precisiones[0] - 2),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8),
                 fontsize=12, fontweight='bold', 
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
                 
    plt.tight_layout()
    plt.savefig('curva_knn_TFG.png', bbox_inches='tight', dpi=300)
    plt.close()
    print(" Gráfico 2 guardado (Versión Curva REAL calculada): 'curva_knn_TFG.png'")

# ==========================================
# 4. RESOLUTOR (Rellena plantillas)
# ==========================================
def resolver_plantilla(plantilla_json):
    plantilla = json.loads(plantilla_json)
    rutina_final = {}

    for dia, slots in plantilla.items():
        rutina_final[dia] = []
        usados_hoy = set()

        for slot in slots:
            opciones = [
                ej["nombre"] for ej in DB_EJERCICIOS 
                if ej["grupo"] == slot["grupo"] 
                and ej["dificultad"] == slot["dificultad"]
                and ej["nombre"] not in usados_hoy
            ]
            
            if opciones:
                ejercicio = random.choice(opciones)
                usados_hoy.add(ejercicio)
            else:
                fallbacks = [ej["nombre"] for ej in DB_EJERCICIOS if ej["grupo"] == slot["grupo"] and ej["dificultad"] == slot["dificultad"]]
                ejercicio = random.choice(fallbacks) if fallbacks else f"Extra {slot['grupo']}"
            
            rutina_final[dia].append({"ejercicio": ejercicio, "series": slot["series"], "reps": slot["reps"]})
            
    return rutina_final

# ==========================================
# 4.5 EXPORTAR EL 20% DE TEST PARA EL REVISOR
# ==========================================
def exportar_baseline_test():
    print("\n Generando archivo Baseline (20% de test) para el Orquestador...")
    datos_exportar = []
    
    # Invertimos los diccionarios para recuperar los nombres en texto
    nivel_inverso = {v: k for k, v in nivel_map.items()}
    objetivo_inverso = {v: k for k, v in objetivo_map.items()}

    # Recorremos el 20% de los datos de test
    for i in range(len(X_test)):
        usuario = X_test.iloc[i]
        plantilla_json = y_test.iloc[i]
        
        # Resolvemos la plantilla para que tenga los ejercicios reales
        rutina_resuelta = resolver_plantilla(plantilla_json)
        
        # Construimos el objeto que guardaremos
        datos_exportar.append({
            "id_test": int(usuario.name), # El ID original del CSV
            "edad": int(usuario['Edad']),
            "peso": float(usuario['Peso_kg']),
            "nivel": nivel_inverso[int(usuario['Nivel_Num'])],
            "objetivo": objetivo_inverso[int(usuario['Objetivo_Num'])],
            "dias": int(usuario['Dias_Entrenamiento']),
            "rutina_knn": rutina_resuelta
        })

    # Lo guardamos en un JSON limpito
    with open('baseline_test_knn.json', 'w', encoding='utf-8') as f:
        json.dump(datos_exportar, f, indent=4, ensure_ascii=False)
        
    print(f" ¡Guardado con éxito! Se han exportado {len(datos_exportar)} rutinas a 'baseline_test_knn.json'")

# ==========================================
# 5. FUNCION PRINCIPAL
# ==========================================
def obtener_rutina(edad, peso, nivel, objetivo, dias):
    perfil = pd.DataFrame([[edad, peso, nivel_map[nivel], objetivo_map[objetivo], dias]], 
                          columns=X.columns)
    perfil_scaled = scaler.transform(perfil)
    distancias, indices = knn.kneighbors(perfil_scaled)
    plantilla_json = y_train.iloc[indices[0][0]]
    return resolver_plantilla(plantilla_json)

# --- EJECUCION ---
if __name__ == "__main__":
    # 1. Ejecutar el examen y crear las imagenes
    evaluar_y_graficar()
    
    # 2. Generar el archivo para comparar con la IA
    exportar_baseline_test()

    # 3. Probar la generacion de rutina
    print("\n Generando rutina para: Carlos (25 años, 80kg, Intermedio, Fuerza, 3 días)")
    rutina = obtener_rutina(25, 80, 'Intermedio', 'Fuerza', 3)
    
    for dia, ejs in rutina.items():
        print(f"\n--- {dia.upper()} ---")
        for e in ejs:
            print(f"{e['ejercicio']} | {e['series']}x{e['reps']}")