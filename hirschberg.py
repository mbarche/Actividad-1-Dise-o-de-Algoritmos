
def calcular_fila(a, b):
   
    anterior = [0] * (len(b) + 1)

    for caracter_a in a:
        actual = [0] * (len(b) + 1)

        for j, caracter_b in enumerate(b, start=1):
            if caracter_a == caracter_b:
                actual[j] = anterior[j - 1] + 1
            else:
                actual[j] = max(anterior[j], actual[j - 1])

        anterior = actual

    return anterior


def hirschberg(a, b):
    """
    Calcula una LCS mediante el algoritmo de Hirschberg.
    Devuelve una subsecuencia común, no necesariamente única.
    """

    # Mantener la segunda cadena como la más corta
    if len(b) > len(a):
        a, b = b, a

    # Casos base
    if len(a) == 0 or len(b) == 0:
        return ""

    if len(a) == 1:
        if a[0] in b:
            return a[0]
        return ""

    # Dividir la primera cadena en dos mitades
    mitad = len(a) // 2

    izquierda = a[:mitad]
    derecha = a[mitad:]

    # Calcular las longitudes desde ambos sentidos
    fila_izquierda = calcular_fila(izquierda, b)
    fila_derecha = calcular_fila(derecha[::-1], b[::-1])

    # Encontrar el punto óptimo de división
    mejor_puntuacion = -1
    mejor_corte = 0

    for j in range(len(b) + 1):
        puntuacion = fila_izquierda[j] + fila_derecha[len(b) - j]

        if puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor_corte = j

    # Resolver recursivamente ambas mitades
    return (
        hirschberg(izquierda, b[:mejor_corte])
        + hirschberg(derecha, b[mejor_corte:])
    )
