import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Conectamos a tu base de datos
cliente = MongoClient(os.getenv("MONGO_URI"))
coleccion_votos = cliente['gym_tfg']['votos_rutinas']

# Hacemos la consulta matemática
pipeline = [
    {
        "$group": {
            "_id": "$origen",
            "nota_media": {"$avg": "$puntuacion"},
            "total_votos": {"$sum": 1}
        }
    }
]

resultados = list(coleccion_votos.aggregate(pipeline))

print("\n RESULTADOS ACTUALES DEL A/B TESTING ")
print("-" * 40)
for res in resultados:
    print(f"Modelo: {res['_id'].upper()}")
    print(f"Nota Media: {res['nota_media']:.2f} ⭐")
    print(f"Votos Totales: {res['total_votos']}")
    print("-" * 40)