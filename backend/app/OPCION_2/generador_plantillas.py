import csv
import random
import json

def generar_plantilla_logica(nivel, objetivo, dias):
    rutina_plantilla = {}
    
    # Parametros de series/reps segun objetivo
    if objetivo == "Fuerza": reps = "3-5"; series = 5
    elif objetivo == "Hipertrofia": reps = "8-12"; series = 4
    else: reps = "15-20"; series = 3
    
    # DEFINICION DE SPLITS SEGUN DIAS
    if dias == 3:
        # Split: Empuje / Tiron + Hombro / Pierna + Core
        config = {
            "dia_1": [("Pecho", 3), ("Triceps", 2)],
            "dia_2": [("Espalda", 3), ("Biceps", 2), ("Hombros", 2)],
            "dia_3": [("Piernas", 3), ("Gemelos", 1), ("Core", 1)]
        }
    elif dias == 4:
        # Split: Pecho+Triceps / Espalda+Biceps / Piernas+Gemelos / Hombros+Core
        config = {
            "dia_1": [("Pecho", 3), ("Triceps", 3)],
            "dia_2": [("Espalda", 3), ("Biceps", 3)],
            "dia_3": [("Piernas", 4), ("Gemelos", 2)],
            "dia_4": [("Hombros", 4), ("Core", 2)]
        }
    else: # 5 dias
        # Split: Un dia por grupo principal 
        config = {
            "dia_1": [("Pecho", 4)],
            "dia_2": [("Espalda", 4)],
            "dia_3": [("Piernas", 4), ("Gemelos", 2)],
            "dia_4": [("Hombros", 4), ("Core", 2)],
            "dia_5": [("Biceps", 3), ("Triceps", 3)]
        }

    for dia, grupos in config.items():
        rutina_plantilla[dia] = []
        for grupo, cantidad in grupos:
            for _ in range(cantidad):
                rutina_plantilla[dia].append({
                    "grupo": grupo,
                    "dificultad": nivel,
                    "series": series,
                    "reps": reps
                })
            
    return json.dumps(rutina_plantilla)

# Generacion del archivo
data = []
for i in range(1, 501):
    edad = random.randint(18, 65); peso = random.randint(50, 120)
    nivel = random.choices(['Principiante', 'Intermedio', 'Avanzado'], weights=[50, 35, 15])[0]
    objetivo = random.choices(['Hipertrofia', 'Fuerza', 'Perdida_Peso'], weights=[45, 20, 35])[0]
    dias = random.choices([3, 4, 5], weights=[50, 30, 20])[0]
    
    plantilla = generar_plantilla_logica(nivel, objetivo, dias)
    data.append([i, edad, peso, nivel, objetivo, dias, plantilla])

with open('gym_dataset_plantillas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['ID', 'Edad', 'Peso_kg', 'Nivel', 'Objetivo', 'Dias_Entrenamiento', 'Plantilla_JSON'])
    writer.writerows(data)

print(" Dataset de Plantillas LÓGICAS creado con éxito.")