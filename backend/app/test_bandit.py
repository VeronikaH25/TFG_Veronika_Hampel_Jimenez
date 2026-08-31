import os
import sys

# Ajuste de rutas para que encuentre tu app
ruta_backend = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ruta_backend)

from analytics.bandit import seleccionar_modelo_bandit

def probar_bandit(tiradas=20):
    print(f" Tirando de la palanca del Bandit {tiradas} veces...\n")
    
    resultados = {"knn": 0, "ia": 0, "exploracion": 0, "explotacion": 0}
    
    for i in range(tiradas):
        print(f"--- Tirada {i+1} ---")
        # Simulamos que un usuario pide una rutina
        modelo, estrategia = seleccionar_modelo_bandit(f"test_usuario_{i}@tfg.com")
        
        # Contabilizamos
        resultados[modelo] += 1
        resultados[estrategia] += 1
        print("-" * 30)
        
    print("\n RESULTADOS FINALES DEL TEST:")
    print(f"Estrategias usadas -> Explotación (Lógica): {resultados['explotacion']} | Exploración (Azar): {resultados['exploracion']}")
    print(f"Modelos elegidos   -> k-NN: {resultados['knn']} | IA: {resultados['ia']}")

if __name__ == "__main__":
    probar_bandit(20)