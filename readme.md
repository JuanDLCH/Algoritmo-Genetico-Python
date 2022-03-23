# <strong>Algoritmo genético</strong>
Lenguaje de programación: Python


## <strong>Descripción:</strong>
El programa recibe como parámetros una cantidad de generaciones y sus probabilidades tanto de cruce como de mutación.

Teniendo como cromosomas iniciales cadenas de bits al azar (Caso por default: 16)

El algoritmo cruzará estos cromosomas obteniendo al término de cada generación el cromosoma más "fuerte" o "apto".

Finalmente nos arrojará el cromosoma más cercano a nuestro resultado esperado

## <strong>Detalles:</strong>
- Cada cruce nos deja únicamente 2 cromosomas, con el número de alelos de padre y madre trocado para cada uno.

- El punto donde los alelos de padre y madre se cruzan es aleatorio

- Los padres de la primera población son [-1, -1] y se genera completamente al azar

# Librerías
```
python -m pip install -U prettytable 
```