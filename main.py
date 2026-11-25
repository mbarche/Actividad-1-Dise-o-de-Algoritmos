
import sys

from recursivo import lcs_recursivo
from hirschberg import hirschberg
from dinamico import lcs_dinamico

# Como anotación indicar que esto es un ejemplo para comprobar
# que las soluciones son válidas y tienen la misma longitud

# Ampliamos el límite de profundidad de recursión de Python.
# Será útil para los experimentos posteriores.
sys.setrecursionlimit(10000)


def es_subsecuencia(subsecuencia, cadena):
    """Comprueba si una cadena aparece en otra respetando el orden."""
    posicion = 0

    for caracter in cadena:
        if posicion < len(subsecuencia):
            if subsecuencia[posicion] == caracter:
                posicion += 1

    return posicion == len(subsecuencia)


def comprobar_resultado(nombre, algoritmo, a, b):
    resultado = algoritmo(a, b)

    valido = (
        es_subsecuencia(resultado, a)
        and es_subsecuencia(resultado, b)
    )

    print(f"\n{nombre}")
    print(f"Subsecuencia: {resultado}")
    print(f"Longitud: {len(resultado)}")
    print(f"Resultado válido: {valido}")

    return resultado, valido


if __name__ == "__main__":

    cadena_a = "ABCDEF"
    cadena_b = "BDEFG"

    print("COMPROBACIÓN DE LOS ALGORITMOS LCS")
    print("-----------------------------------")
    print(f"Cadena A: {cadena_a}")
    print(f"Cadena B: {cadena_b}")

    resultados = []

    resultados.append(
        comprobar_resultado(
            "A - Recursiva directa",
            lcs_recursivo,
            cadena_a,
            cadena_b
        )
    )

    resultados.append(
        comprobar_resultado(
            "B - Hirschberg",
            hirschberg,
            cadena_a,
            cadena_b
        )
    )

    resultados.append(
        comprobar_resultado(
            "C - Programación dinámica",
            lcs_dinamico,
            cadena_a,
            cadena_b
        )
    )

    longitudes = [len(resultado) for resultado, valido in resultados]

    todos_validos = all(valido for resultado, valido in resultados)

    print("\n-----------------------------------")
    print(f"Todas las soluciones son válidas: {todos_validos}")
    print(f"Longitudes obtenidas: {longitudes}")
    print(f"Las longitudes coinciden: {len(set(longitudes)) == 1}")
