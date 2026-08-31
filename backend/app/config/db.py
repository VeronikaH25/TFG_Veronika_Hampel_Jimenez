import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargamos las variables del .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    # Conectamos con Atlas
    cliente_mongo = MongoClient(MONGO_URI)
    db = cliente_mongo['gym_tfg']
    
    # Exportamos las colecciones para usarlas en otros archivos
    usuarios_collection = db['usuarios']
    # La de los votos
    votos_collection = db['votos_rutinas']
    
    auditoria_collection = db["auditoria_ia"]
    
    decisiones_bandit_collection = db["decisiones_bandit"]
    
    print("✅ Base de datos conectada correctamente.")
except Exception as e:
    print(f"❌ Error al conectar a la base de datos: {e}")