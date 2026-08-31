from pydantic import BaseModel

class VotoRutina(BaseModel):
    origen_elegido: str        # Algoritmo seleccionado por el orquestador ("knn" o "ia")
    rutina_json: dict          # Estructura completa de la rutina para persistencia
    origen_opcion_1: str       # Identificador del algoritmo de la primera opción
    puntuacion_opcion_1: int   # Valoración cuantitativa asignada (1-5)
    origen_opcion_2: str       # Identificador del algoritmo de la segunda opción
    puntuacion_opcion_2: int   # Valoración cuantitativa asignada (1-5)