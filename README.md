Actividad 1 - Diseño avanzado de algoritmos

Descripción

Implementación y comparación de tres algoritmos para resolver el problema de la subsecuencia común más larga (LCS):

Recursivo: recursividad directa sin memorización.

Hirschberg: divide y conquista con espacio auxiliar lineal.

Dinámico: programación dinámica mediante una tabla.

Requisitos

Python 3.15 o compatible.

Matplotlib para generar las gráficas.

Instalación

Instalar las dependencias con:

pip install -r requirements.txt

Ejecución

Desde la carpeta principal del proyecto:

python ejecutar.py

Este comando realiza la comprobación de los algoritmos, ejecuta los experimentos y genera las gráficas.

Nota: ejecutar este comando vuelve a generar los datos y resultados. Para conservar los resultados actuales, no es necesario ejecutarlo.

Experimentos

Se comparan cinco tamaños de cadenas: 10, 20, 50, 100 y 1000 caracteres.

Se miden el tiempo de CPU y el consumo máximo de memoria. Las cadenas se generan utilizando un alfabeto de cuatro caracteres y una semilla fija.

Las mediciones se guardan en resultados/mediciones.csv y los datos utilizados en datasets/cadenas.csv.

Estructura

main.py: comprobación de los algoritmos.

recursivo.py: implementación recursiva.

hirschberg.py: implementación de Hirschberg.

dinamico.py: implementación dinámica.

experimentos.py: ejecución y medición de experimentos.

graficas.py: generación de gráficas.

ejecutar.py: ejecución completa del proyecto.

datasets/: cadenas utilizadas.

resultados/: mediciones y gráficas.

Autor

Actividad académica de Diseño avanzado de algoritmos.