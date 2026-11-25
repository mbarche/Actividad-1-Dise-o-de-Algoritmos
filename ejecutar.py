from pathlib import Path
import subprocess
import sys


# Carpeta donde se encuentra este archivo
CARPETA_PROYECTO = Path(__file__).resolve().parent


# Orden de ejecución de los programas
PASOS = [
    ("Comprobación de los algoritmos", "main.py"),
    ("Ejecución de los experimentos", "experimentos.py"),
    ("Generación de las gráficas", "graficas.py"),
]


def main():
    print("======================================")
    print("       EJECUCIÓN DEL PROYECTO LCS")
    print("======================================")

    for descripcion, archivo in PASOS:
        ruta = CARPETA_PROYECTO / archivo

        if not ruta.is_file():
            print(f"\nERROR: No se encuentra el archivo {archivo}")
            return 1

        print(f"\n>>> {descripcion}")
        print(f"Ejecutando: {archivo}\n")

        try:
            subprocess.run(
                [sys.executable, str(ruta)],
                cwd=CARPETA_PROYECTO,
                check=True
            )

        except subprocess.CalledProcessError as error:
            print(f"\nERROR al ejecutar {archivo}.")
            print(f"Código de salida: {error.returncode}")
            print("Se detiene la ejecución del proyecto.")
            return 1

    print("\n======================================")
    print("  PROYECTO EJECUTADO CORRECTAMENTE")
    print("======================================")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())