import json
import pandas as pd
import time
from backend.app.CHATGPT.agente_ia import agente_creador
from backend.app.CHATGPT.agente_revisor import revisar_hibrido

# ==========================================
# SCRIPT DE BENCHMARK PARA EL TFG
# ==========================================
def ejecutar_evaluacion_masiva():
    print(" Iniciando Evaluación Masiva de Usuarios (Benchmark)...")

    start_time = time.time()

    # 1. Cargar baseline
    try:
        with open('../OPCION_2/baseline_test_knn.json', 'r', encoding='utf-8') as f:
            usuarios_test = json.load(f)
    except FileNotFoundError:
        print(" Error: No se encontró 'baseline_test_knn.json'.")
        return

    resultados_benchmark = []

    estadisticas = {
        "total": len(usuarios_test),
        "aprobados": 0,
        "rechazados_python": 0,
        "rechazados_ia": 0,
        "errores_conexion": 0
    }

    # ==========================================
    # 2. LOOP PRINCIPAL
    # ==========================================
    for i, usuario in enumerate(usuarios_test):

        print(f"\n" + "-"*40)
        print(f" Usuario {i+1}/{len(usuarios_test)} | ID: {usuario['id_test']}")
        print("-"*40)

        rutina_knn = usuario['rutina_knn']

        # --------------------------------------
        # A) GENERACIÓN IA
        # --------------------------------------
        try:
            resultado_ia = agente_creador(
                edad=usuario['edad'],
                peso=usuario['peso'],
                nivel=usuario['nivel'],
                objetivo=usuario['objetivo'],
                dias=usuario['dias']
            )

            #  CONTROL CRÍTICO
            if not resultado_ia or "rutina" not in resultado_ia:
                print("    Error: respuesta IA inválida")
                estadisticas["errores_conexion"] += 1
                continue

            rutina_ia = resultado_ia.get("rutina", {})

        except Exception as e:
            print(f"    Error conexión IA: {e}")
            estadisticas["errores_conexion"] += 1
            continue

        # --------------------------------------
        # B) VALIDACIÓN
        # --------------------------------------
        veredicto = revisar_hibrido(rutina_knn, rutina_ia, usuario['nivel'])

        aprobado = veredicto.get("aprobado", False)
        fase_rechazo = veredicto.get("fase", "N/A")

        
        if aprobado:
            estadisticas["aprobados"] += 1
            print("    RESULTADO: APROBADO")
        else:
            if fase_rechazo == "python":
                estadisticas["rechazados_python"] += 1
                print(f"    RESULTADO: RECHAZADO por Python (Estructura/Matemáticas)")
            elif fase_rechazo == "llm":
                estadisticas["rechazados_ia"] += 1
                print(f"    RESULTADO: RECHAZADO por LLM (Biomecánica/Semántica)")
            
            # Mostramos el motivo exacto del rechazo
            motivo = veredicto.get("errores", veredicto.get("detalle", "Error desconocido"))
            print(f"      Motivo: {motivo}")

        # --------------------------------------
        # C) GUARDAR RESULTADO
        # --------------------------------------
        resultados_benchmark.append({
            "ID_Usuario": usuario['id_test'],
            "Nivel": usuario['nivel'],
            "Objetivo": usuario['objetivo'],
            "Dias": usuario['dias'],
            "Aprobado": "SI" if aprobado else "NO",
            "Fase_Fallo": fase_rechazo if not aprobado else "N/A",
            "Detalles_Fallo": str(
                veredicto.get("errores",
                veredicto.get("detalle", "Correcto"))
            )
        })

        # Pausa pequeña (mejor rendimiento)
        time.sleep(0.3)

    # ==========================================
    # 3. GUARDAR CSV
    # ==========================================
    df = pd.DataFrame(resultados_benchmark)
    df.to_csv("resultados_tfg_benchmark.csv", index=False, encoding='utf-8', sep=';')

    # ==========================================
    # 4. MÉTRICAS FINALES
    # ==========================================
    total = estadisticas["total"]

    if total > 0:
        accuracy = (estadisticas["aprobados"] / total) * 100
        tasa_python = ((total - estadisticas["rechazados_python"]) / total) * 100
        tasa_llm = ((total - estadisticas["rechazados_ia"]) / total) * 100
    else:
        accuracy = tasa_python = tasa_llm = 0

    tiempo_total = time.time() - start_time

    # ==========================================
    # 5. INFORME FINAL
    # ==========================================
    print("\n" + "="*50)
    print(" INFORME FINAL DEL BENCHMARK")
    print("="*50)

    print(f" Total evaluados: {total}")
    print(f" Aprobados: {estadisticas['aprobados']} ({accuracy:.2f}%)")

    print("\n ERRORES:")
    print(f" Python (estructura): {estadisticas['rechazados_python']}")
    print(f" IA (semántica): {estadisticas['rechazados_ia']}")
    print(f" Errores de conexión: {estadisticas['errores_conexion']}")

    print("\n MÉTRICAS AVANZADAS:")
    print(f"✔ Tasa éxito estructural (Python): {tasa_python:.2f}%")
    print(f"✔ Tasa éxito semántico (LLM): {tasa_llm:.2f}%")

    print(f"\n⏱ Tiempo total: {tiempo_total:.2f} segundos")

    print("\n Resultados guardados en:")
    print(" resultados_tfg_benchmark.csv")

    print("="*50)


# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    ejecutar_evaluacion_masiva()