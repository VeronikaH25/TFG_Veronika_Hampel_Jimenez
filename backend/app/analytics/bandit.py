import random
from datetime import datetime, timezone
from app.config.db import votos_collection, decisiones_bandit_collection

EPSILON = 0.20  # 20% Exploración, 80% Explotación

def calcular_medias_modelos():
    """Consulta MongoDB usando agregación para obtener estadísticas históricas"""
    pipeline = [
        {
            "$group": {
                "_id": "$origen",
                "nota_media": {"$avg": "$puntuacion"},
                "votos_totales": {"$sum": 1}
            }
        }
    ]
    
    resultados = list(votos_collection.aggregate(pipeline))
    
    stats = {
        "knn": {"nota_media": 3.0, "votos_totales": 0},
        "ia": {"nota_media": 3.0, "votos_totales": 0}
    }
    
    for res in resultados:
        origen = res["_id"]
        if origen in stats:
            stats[origen]["nota_media"] = round(res["nota_media"], 2)
            stats[origen]["votos_totales"] = res["votos_totales"]
            
    return stats

def seleccionar_modelo_bandit(email_usuario: str):
    """Aplica Epsilon-Greedy con Fase de Calentamiento y registra la decisión."""
    stats = calcular_medias_modelos()
    nota_knn = stats["knn"]["nota_media"]
    nota_ia = stats["ia"]["nota_media"]
    votos_totales = stats["knn"]["votos_totales"] + stats["ia"]["votos_totales"]
    
    # 1. FASE DE CALENTAMIENTO: Si no hay significancia estadística, asegurar el tiro
    UMBRAL_MINIMO_VOTOS = 10
    if votos_totales < UMBRAL_MINIMO_VOTOS:
        estrategia = "calentamiento"
        modelo_elegido = "knn"  # Forzamos el modelo matemático seguro
        print(f" [BANDIT] Modo: CALENTAMIENTO (Votos: {votos_totales}/{UMBRAL_MINIMO_VOTOS}) | Elegido por seguridad: KNN")
    
    # 2. FASE OPERATIVA: Epsilon-Greedy clásico
    else:
        dado = random.random()
        if dado < EPSILON:
            estrategia = "exploracion"
            modelo_elegido = random.choice(["knn", "ia"])
        else:
            estrategia = "explotacion"
            if nota_knn == nota_ia:
                modelo_elegido = random.choice(["knn", "ia"])
            else:
                modelo_elegido = "knn" if nota_knn > nota_ia else "ia"
                
        print(f" [BANDIT] Modo: {estrategia.upper()} | Medias -> KNN: {nota_knn}, IA: {nota_ia} | Elegido: {modelo_elegido.upper()}")
    
    # REGISTRO DE AUDITORÍA MLOps
    documento_decision = {
        "email_usuario": email_usuario,
        "estrategia": estrategia,
        "modelo_elegido": modelo_elegido,
        "historico_medias": {
            "knn": nota_knn,
            "ia": nota_ia
        },
        "historico_votos": {
            "knn": stats["knn"]["votos_totales"],
            "ia": stats["ia"]["votos_totales"]
        },
        "fecha_decision": datetime.now(timezone.utc)
    }
    decisiones_bandit_collection.insert_one(documento_decision)
    
    return modelo_elegido, estrategia