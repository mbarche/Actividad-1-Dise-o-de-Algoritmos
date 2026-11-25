
def lcs_recursivo(a, b):

    def resolver(i, j):
        # Caso base: alguna cadena se ha agotado
        if i == len(a) or j == len(b):
            return ""

        # Si los caracteres coinciden
        if a[i] == b[j]:
            return a[i] + resolver(i + 1, j + 1)

        # Si no coinciden, probamos las dos posibilidades
        opcion1 = resolver(i + 1, j)
        opcion2 = resolver(i, j + 1)

        # Devolvemos la subsecuencia más larga
        if len(opcion1) >= len(opcion2):
            return opcion1
        else:
            return opcion2

    return resolver(0, 0)

