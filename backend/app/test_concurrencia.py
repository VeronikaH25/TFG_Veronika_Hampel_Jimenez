import threading
import time
import requests

# Ajusta el puerto o la ruta si la tuya es distinta
URL_API = "http://127.0.0.1:8000/api/rutinas/generar-inteligente"

def pedir_rutina(usuario_id):
    print(f" Usuario {usuario_id} pide rutina a las {time.strftime('%H:%M:%S')}")
    inicio = time.time()
    
    try:
        # Hacemos la petición a tu servidor
        respuesta = requests.post(URL_API, json={
            "email": f"test_concurrencia_{usuario_id}@tfg.com",
            "edad": 22,
            "peso": 65,
            "nivel": "Intermedio",
            "objetivo": "Fuerza",
            "dias_entreno": 4
        })
        
        if respuesta.status_code == 200:
            fin = time.time()
            print(f" Usuario {usuario_id} recibió su rutina en {fin - inicio:.2f} segundos!")
        else:
            print(f" Usuario {usuario_id} falló con estado {respuesta.status_code}")
            
    except Exception as e:
        print(f" Usuario {usuario_id} falló de forma crítica: {e}")

if __name__ == "__main__":
    print(" Simulando 2 usuarios atacando la API AL MISMO TIEMPO...\n")
    tiempo_total_inicio = time.time()

    # Creamos dos hilos independientes (concurrencia real en el cliente)
    hilo1 = threading.Thread(target=pedir_rutina, args=(1,))
    hilo2 = threading.Thread(target=pedir_rutina, args=(2,))

    # Los disparamos a la vez
    hilo1.start()
    hilo2.start()

    # Esperamos a que los dos terminen
    hilo1.join()
    hilo2.join()

    tiempo_total_fin = time.time()
    print(f"\n TIEMPO TOTAL DE LA PRUEBA: {tiempo_total_fin - tiempo_total_inicio:.2f} segundos")