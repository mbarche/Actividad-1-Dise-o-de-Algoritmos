
import csv
import os
import matplotlib.pyplot as plt


CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_CSV = os.path.join(
    CARPETA_PROYECTO, "resultados", "mediciones.csv"
)

CARPETA_GRAFICAS = os.path.join(
    CARPETA_PROYECTO, "resultados", "graficas"
)


def cargar_datos():
    """Lee las mediciones guardadas en el archivo CSV."""

    with open(ARCHIVO_CSV, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


def preparar_datos(datos, algoritmo, columna):
    """Obtiene los valores completados de un algoritmo."""

    filas = [
        fila for fila in datos
        if fila["Algoritmo"] == algoritmo
        and fila["Estado"] == "COMPLETADO"
        and fila[columna] != ""
    ]

    filas.sort(key=lambda fila: int(fila["Longitud"]))

    x = [int(fila["Longitud"]) for fila in filas]
    y = [float(fila[columna]) for fila in filas]

    return x, y


def grafica_tiempo(datos):
    """Genera la gráfica de tiempo de CPU."""

    plt.figure(figsize=(9, 5))

    algoritmos = ["Dinamico", "Hirschberg", "Recursivo"]

    for algoritmo in algoritmos:
        x, y = preparar_datos(
            datos, algoritmo, "Tiempo_CPU_segundos"
        )

        if x:
            plt.plot(x, y, marker="o", label=algoritmo)

    plt.xlabel("Longitud de las cadenas")
    plt.ylabel("Tiempo de CPU (segundos)")
    plt.title("Comparación del tiempo de ejecución")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()

    plt.figtext(
        0.5, 0.01,
        "La versión recursiva no completa los experimentos "
        "de longitud 20 o superior (timeout > 5 s).",
        ha="center",
        fontsize=8
    )

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    plt.savefig(
        os.path.join(CARPETA_GRAFICAS, "tiempo_cpu.png"),
        dpi=300
    )
    plt.close()


def grafica_memoria(datos):
    """Genera la gráfica de memoria máxima."""

    plt.figure(figsize=(9, 5))

    algoritmos = ["Dinamico", "Hirschberg", "Recursivo"]

    for algoritmo in algoritmos:
        x, y = preparar_datos(
            datos, algoritmo, "Memoria_pico_MB"
        )

        if x:
            plt.plot(x, y, marker="o", label=algoritmo)

    plt.xlabel("Longitud de las cadenas")
    plt.ylabel("Memoria máxima (MB)")
    plt.title("Comparación del consumo de memoria")
    plt.yscale("log")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.figtext(
        0.5, 0.01,
        "Solo se representan ejecuciones completadas.",
        ha="center",
        fontsize=8
    )

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(
        os.path.join(CARPETA_GRAFICAS, "memoria.png"),
        dpi=300
    )
    plt.close()


def grafica_longitud_lcs(datos):
    """Genera la gráfica de longitud de la subsecuencia común."""

    plt.figure(figsize=(9, 5))

    algoritmos = ["Dinamico", "Hirschberg", "Recursivo"]

    for algoritmo in algoritmos:
        x, y = preparar_datos(
            datos, algoritmo, "Longitud_LCS"
        )

        if x:
            plt.plot(x, y, marker="o", label=algoritmo)

    plt.xlabel("Longitud de las cadenas")
    plt.ylabel("Longitud de la LCS")
    plt.title("Longitud de la subsecuencia común más larga")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.figtext(
        0.5, 0.01,
        "Solo se representan las ejecuciones completadas.",
        ha="center",
        fontsize=8
    )

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(
        os.path.join(CARPETA_GRAFICAS, "longitud_lcs.png"),
        dpi=300
    )
    plt.close()


if __name__ == "__main__":

    os.makedirs(CARPETA_GRAFICAS, exist_ok=True)

    datos = cargar_datos()

    grafica_tiempo(datos)
    grafica_memoria(datos)
    grafica_longitud_lcs(datos)

    print("======================================")
    print("       GRÁFICAS GENERADAS")
    print("======================================")
    print("1. tiempo_cpu.png")
    print("2. memoria.png")
    print("3. longitud_lcs.png")
    print(f"\nUbicación: {CARPETA_GRAFICAS}")
