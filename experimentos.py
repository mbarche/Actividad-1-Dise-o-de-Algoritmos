
import csv
import json
import os
import random
import subprocess
import sys
import time
import tracemalloc

from recursivo import lcs_recursivo
from hirschberg import hirschberg
from dinamico import lcs_dinamico


# Configuración de los experimentos
LONGITUDES = [10, 20, 50, 100, 1000]
SEMILLA = 42
TIEMPO_MAXIMO = 5  # Segundos por ejecución


ALGORITMOS = {
    "Recursivo": lcs_recursivo,
    "Hirschberg": hirschberg,
    "Dinamico": lcs_dinamico
}


def generar_cadenas(longitud, generador):
    """Genera dos cadenas aleatorias reproducibles."""
    alfabeto = "ABCD"

    cadena_a = "".join(
        generador.choices(alfabeto, k=longitud)
    )

    cadena_b = "".join(
        generador.choices(alfabeto, k=longitud)
    )

    return cadena_a, cadena_b


def es_subsecuencia(subsecuencia, cadena):
    """Comprueba si una cadena es subsecuencia de otra."""
    posicion = 0

    for caracter in cadena:
        if posicion < len(subsecuencia):
            if subsecuencia[posicion] == caracter:
                posicion += 1

    return posicion == len(subsecuencia)


def ejecutar_worker(nombre, a, b):
    funcion = ALGORITMOS[nombre]

    # 1. Medir el tiempo de CPU sin activar tracemalloc.
    # Repetimos la ejecución hasta acumular al menos 0,1 segundos,
    # para obtener una medición más precisa.
    repeticiones = 1
    inicio = time.process_time_ns()

    resultado = funcion(a, b)

    tiempo_total_ns = time.process_time_ns() - inicio

    duracion_minima_ns = 100_000_000  # 0,1 segundos
    max_repeticiones = 10000

    while (
        tiempo_total_ns < duracion_minima_ns
        and repeticiones < max_repeticiones
    ):
        resultado = funcion(a, b)
        repeticiones += 1
        tiempo_total_ns = time.process_time_ns() - inicio

    tiempo_medio = (tiempo_total_ns / repeticiones) / 1_000_000_000

    # 2. Medir la memoria en una ejecución independiente.
    # Así tracemalloc no afecta a la medición del tiempo.
    tracemalloc.start()

    try:
        resultado_memoria = funcion(a, b)
        _, pico_memoria = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return {
        "resultado": resultado,
        "tiempo_cpu": tiempo_medio,
        "memoria_bytes": pico_memoria
    }


def ejecutar_aislado(nombre, a, b):
    """
    Ejecuta el algoritmo en otro proceso para poder
    establecer un tiempo máximo de ejecución.
    """

    comando = [
        sys.executable,
        os.path.abspath(__file__),
        "--worker",
        nombre,
        a,
        b
    ]

    inicio = time.perf_counter()

    try:
        proceso = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=TIEMPO_MAXIMO,
            encoding="utf-8"
        )

        tiempo_total = time.perf_counter() - inicio

        if proceso.returncode != 0:
            return {
                "estado": "ERROR",
                "tiempo_cpu": None,
                "memoria_mb": None,
                "longitud_lcs": None,
                "valido": False
            }

        datos = json.loads(proceso.stdout)

        resultado = datos["resultado"]

        valido = (
            es_subsecuencia(resultado, a)
            and es_subsecuencia(resultado, b)
        )

        return {
            "estado": "COMPLETADO",
            "tiempo_cpu": datos["tiempo_cpu"],
            "memoria_mb": datos["memoria_bytes"] / (1024 * 1024),
            "longitud_lcs": len(resultado),
            "valido": valido
        }

    except subprocess.TimeoutExpired:
        return {
            "estado": "TIMEOUT",
            "tiempo_cpu": None,
            "memoria_mb": None,
            "longitud_lcs": None,
            "valido": False
        }


def guardar_datasets(datasets):
    """Guarda las cadenas utilizadas para reproducir las pruebas."""

    os.makedirs("datasets", exist_ok=True)

    with open(
        "datasets/cadenas.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow([
            "Experimento",
            "Longitud",
            "Cadena_A",
            "Cadena_B"
        ])

        for numero, longitud, a, b in datasets:
            escritor.writerow([numero, longitud, a, b])


def guardar_resultados(resultados):
    """Guarda las mediciones en un archivo CSV."""

    os.makedirs("resultados", exist_ok=True)

    campos = [
        "Experimento",
        "Longitud",
        "Algoritmo",
        "Estado",
        "Tiempo_CPU_segundos",
        "Memoria_pico_MB",
        "Longitud_LCS",
        "Solucion_valida"
    ]

    with open(
        "resultados/mediciones.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=campos
        )

        escritor.writeheader()
        escritor.writerows(resultados)


def realizar_experimentos():
    """Genera las entradas, ejecuta los algoritmos y guarda resultados."""

    generador = random.Random(SEMILLA)

    datasets = []
    resultados = []

    print("\n========================================")
    print("       EXPERIMENTOS DE ALGORITMOS LCS")
    print("========================================")

    # Generar todas las parejas de cadenas
    for numero, longitud in enumerate(LONGITUDES, start=1):
        a, b = generar_cadenas(longitud, generador)
        datasets.append((numero, longitud, a, b))

    guardar_datasets(datasets)

    # Ejecutar cada algoritmo con cada pareja
    for numero, longitud, a, b in datasets:

        print(f"\nExperimento {numero}: cadenas de {longitud} caracteres")
        print("-" * 55)

        resultados_prueba = {}

        # Ejecutamos primero los algoritmos polinómicos
        orden = ["Dinamico", "Hirschberg", "Recursivo"]

        for nombre in orden:

            print(f"Ejecutando {nombre}...", end=" ", flush=True)

            medicion = ejecutar_aislado(nombre, a, b)

            resultados_prueba[nombre] = medicion

            if medicion["estado"] == "COMPLETADO":
                print(
                    f"OK | CPU: {medicion['tiempo_cpu']:.6f} s "
                    f"| Memoria: {medicion['memoria_mb']:.4f} MB "
                    f"| LCS: {medicion['longitud_lcs']}"
                )
            elif medicion["estado"] == "TIMEOUT":
                print(f"TIMEOUT (más de {TIEMPO_MAXIMO} segundos)")
            else:
                print("ERROR")

        # Longitud de referencia obtenida mediante programación dinámica
        longitud_referencia = resultados_prueba["Dinamico"]["longitud_lcs"]

        # Guardar todas las mediciones
        for nombre, medicion in resultados_prueba.items():

            correcta = medicion["valido"]

            if (
                medicion["estado"] == "COMPLETADO"
                and longitud_referencia is not None
            ):
                correcta = (
                    correcta
                    and medicion["longitud_lcs"] == longitud_referencia
                )

            resultados.append({
                "Experimento": numero,
                "Longitud": longitud,
                "Algoritmo": nombre,
                "Estado": medicion["estado"],
                "Tiempo_CPU_segundos": medicion["tiempo_cpu"],
                "Memoria_pico_MB": medicion["memoria_mb"],
                "Longitud_LCS": medicion["longitud_lcs"],
                "Solucion_valida": correcta
            })

    guardar_resultados(resultados)

    print("\n========================================")
    print("EXPERIMENTOS FINALIZADOS")
    print("========================================")
    print("Datasets: datasets/cadenas.csv")
    print("Resultados: resultados/mediciones.csv")


if __name__ == "__main__":

    # Modo de ejecución interna de cada proceso
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":

        sys.setrecursionlimit(10000)

        nombre = sys.argv[2]
        cadena_a = sys.argv[3]
        cadena_b = sys.argv[4]

        datos = ejecutar_worker(nombre, cadena_a, cadena_b)

        print(json.dumps(datos))

    else:
        realizar_experimentos()
