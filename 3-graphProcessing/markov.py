import json

# Estos son los estados que vamos a usar en todo.

STATES = ["casual", "focused", "research", "browsing"]


# 1. Cargo el JSON pa' poder trabajar.

with open("biblioteca3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Registros cargados:", len(data))



# 2. Creo una matriz 4x4 llena de ceros.
# voy a ir contando cuántas veces la gente pasa de un estado a otro.
# Como: casual -> browsing, research -> focused, etc.

counts = [[0, 0, 0, 0] for _ in range(4)]


# 3. Recorro todos los libros y miro el estado anterior y el actual.
# Si algo viene raro pues lo salto y sigo normal.
# voy sumando las transiciones.

for libro in data:
    prev = libro.get("previousInterestState")
    curr = libro.get("userInterestState")

    if prev not in STATES or curr not in STATES:
        continue   # si llega algo fuera de los estados, lo ignoro y ya

    i = STATES.index(prev)
    j = STATES.index(curr)

    counts[i][j] += 1  # sumo esa transición entre estados


# 4. Ya con los conteos, paso todo a probabilidades.
# Esta ya es la matriz P de Markov. Cada fila representa un estado
# y debe sumar aprox a 1 .

P = []
for fila in counts:
    total = sum(fila)
    if total == 0:
        # Si nunca hubo transiciones desde ese estado, pues queda todo en 0.
        P.append([0, 0, 0, 0])
    else:
        P.append([c / total for c in fila])


# 5. Imprimo la matriz P para ver cómo está quedando todo.
# Esto muestra la probabilidad de pasar de un estado a otro.

print("\nMatriz de transición de estados de interés (P):\n")
for i, fila in enumerate(P):
    estado = STATES[i]
    print(f"Desde '{estado}' -> ", end="")
    print([round(x, 3) for x in fila])


# 6. Ahora saco la distribución estacionaria.
# Esto básicamente es: “si el usuario navega mucho rato,
# ¿en qué estado termina quedándose más tiempo?”.
# lo calculo repitiendo pi = pi * P varias veces,

n = len(STATES)
pi = [1.0 / n] * n  # empiezo asumiendo que todos los estados pesan igual

# Repite varias veces para que se estabilice
for _ in range(50):
    nueva = [0.0] * n
    for i in range(n):
        for j in range(n):
            nueva[j] += pi[i] * P[i][j]
    pi = nueva  # actualizo

# Normalizo por si las moscas
suma_pi = sum(pi) or 1.0
pi = [p / suma_pi for p in pi]

print("\nDistribución estacionaria aproximada:\n")
for estado, valor in zip(STATES, pi):
    print(f"{estado}: {valor:.3f}")


# 7. Recomendación sencilla basada en Markov
# Aquí lo que hago es: según el estado actual, miro la fila
# y saco a qué estado es más probable que pase el usuario.
# Y con eso, recomiendo libros de ese estado.


def recomendar_siguiente_estado(estado_actual, matriz_P, states):
    """
    Esta función es lo más simple del mundo:
    agarra la fila del estado actual y se queda con el valor más alto.
    """
    if estado_actual not in states:
        return None

    i = states.index(estado_actual)
    fila = matriz_P[i]
    j = fila.index(max(fila))  # agarro el mayor
    return states[j]


def recomendar_libros_por_estado(data, estado, k=5):
    """
    Aquí solo filtro libros que coincidan con ese estado
    y saco los más vistos. Nada fancy, pero funciona.
    """
    filtrados = [lib for lib in data if lib.get("userInterestState") == estado]
    ordenados = sorted(filtrados, key=lambda x: x.get("views", 0), reverse=True)
    return ordenados[:k]



# Pruebo todo esto con un ejemplo sencillito.

estado_actual = "casual"  

estado_predicho = recomendar_siguiente_estado(estado_actual, P, STATES)

print("\nEstado actual del usuario:", estado_actual)
print("Estado más probable al que pasará (Markov):", estado_predicho)

# Ahora sí, recomiendooo
recs = recomendar_libros_por_estado(data, estado_predicho, k=5)

print(f"\nLibros recomendados para el estado '{estado_predicho}':\n")
for r in recs:
    print(f"- {r['title']} (views: {r['views']})")

