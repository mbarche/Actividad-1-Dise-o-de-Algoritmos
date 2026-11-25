
def lcs_dinamico(a, b):

    m = len(a)
    n = len(b)

    # Crear la matriz de programación dinámica
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Rellenar la matriz
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    # Reconstruir la subsecuencia común más larga
    resultado = []
    i = m
    j = n

    while i > 0 and j > 0:

        if a[i - 1] == b[j - 1]:
            resultado.append(a[i - 1])
            i -= 1
            j -= 1

        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1

        else:
            j -= 1

    # La reconstrucción se ha realizado en orden inverso
    return "".join(reversed(resultado))
