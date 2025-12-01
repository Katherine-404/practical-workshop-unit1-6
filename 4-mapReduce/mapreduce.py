import json
import random
from collections import defaultdict


# UNIDAD 4 - MAPREDUCE
# sigo trabajando con la misma biblioteca del W3,
# pero ahora le metemos la parte de MapReduce.



# 0. Cargo la data del W3 (biblioteca3.json) y le agrego
#    los campos nuevos que pide el W4:
#    - mapReducePartition
#    - processingNode
#    - batchId
#    - aggregationKey = genre_contentCategory
# Después guardo todo en biblioteca4.json para que quede listo.

with open("biblioteca4.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Registros originales (U3):", len(data))

for libro in data:
    # Simulo en qué partición del cluster cae cada registro
    libro["mapReducePartition"] = random.randint(1, 24)
    # Simulo en qué nodo se procesa
    libro["processingNode"] = f"node_{random.randint(1, 12)}"
    # Simulo un id de batch
    libro["batchId"] = f"batch_{random.randint(1000, 9999)}"

    genero = libro.get("genre", "unknown")
    categoria = libro.get("contentCategory", "unknown")
    # Esta llave sirve para agrupar cosas por género + categoría
    libro["aggregationKey"] = f"{genero}_{categoria}"

# Guardo el JSON ya actualizado con la info de MapReduce
with open("biblioteca4.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Se creó biblioteca4.json con los campos de MapReduce.\n")

# A partir de aquí ya uso "data" que tiene todo lo del W3 + W4.



# ALGORITMO 1: Library Book Counter 
# Idea: hacer un "word count" pero con títulos de libros.
# Map:   (title, 1)
# Reduce: sumar todos los 1 por cada título.
# Objetivo: ver cuáles libros son los más "prestados".


print("Algoritmo 1: Contador de libros")

book_counts = defaultdict(int)

# Aqui hago el Map + Reduce  en Python
for registro in data:
    titulo = registro.get("title", "sin_titulo")
    book_counts[titulo] += 1  # es como emitir (title,1) y luego agrupar

# Ordeno de mayor a menor para ver los mas populares
libros_populares = sorted(book_counts.items(), key=lambda x: x[1], reverse=True)

print("Top 5 libros más 'prestados' según los registros:\n")
for titulo, conteo in libros_populares[:5]:
    print(f"- {titulo} -> {conteo} checkouts aprox.")

print("\n")



# ALGORITMO 2: Average Reading Time Calculator
# Idea: ver qué tipo de usuario lee más tiempo en promedio.
# Acá uso:
#   - user_category = userInterestState (casual, focused, etc)
#   - reading_time = expectedReadingTime
# Map:   (user_category, reading_time)
# Reduce: sacar el promedio por categoría.


print("Algoritmo 2: Promedio de tiempo de lectura por tipo de usuario")

tiempos_por_categoria = defaultdict(list)

for registro in data:
    categoria = registro.get("userInterestState", "desconocido")
    tiempo = registro.get("expectedReadingTime", 0)
    tiempos_por_categoria[categoria].append(tiempo)

print("Promedio de tiempo de lectura  por categoría:\n")
for categoria, tiempos in tiempos_por_categoria.items():
    if not tiempos:
        continue
    promedio = sum(tiempos) / len(tiempos)
    print(f"- {categoria}: {promedio:.2f} minutos")

print("\n")

# ALGORITMO 3: Library Report Generator (Basic Join)
# Idea: simular un JOIN sencillo:
#   - "Tabla" de libros: (book_id, title, author)
#   - "Tabla" de checkouts: (book_id, cantidad de veces que aparece)
# En la vida real serían dos archivos y se haría un MapReduce join.
# Aquí lo hago sencillo con dos diccionarios y luego los uno.


print("Algoritmo 3: Reporte de autores y popularidad")

# Esta parte simula la tabla de libros
books_info = {}
for registro in data:
    book_id = registro.get("_id")
    books_info[book_id] = {
        "title": registro.get("title", "sin_titulo"),
        "author": registro.get("author", "sin_autor")
    }

# Esta parte simula la tabla de checkouts
checkout_counts = defaultdict(int)
for registro in data:
    book_id = registro.get("_id")
    checkout_counts[book_id] += 1

# Aqu ya seria como el "reduce": junto toda la info por book_id
reporte = []
for book_id, info in books_info.items():
    total_checkouts = checkout_counts[book_id]
    reporte.append({
        "author": info["author"],
        "title": info["title"],
        "totalCheckouts": total_checkouts
    })

# Ordeno por núimero de checkouts para ver lo más popular
reporte_ordenado = sorted(reporte, key=lambda x: x["totalCheckouts"], reverse=True)

print("Top 5 libros con su autor y número de checkouts:\n")
for item in reporte_ordenado[:5]:
    print(f"- {item['author']} – {item['title']} -> {item['totalCheckouts']} checkouts")

print("\n")


# ALGORITMO 4: Library System Costs
# estimación simple de costos.
# Suposiciones :
#   - 1 libro de texto ~ 1 MB
#   - 1 recurso multimedia (video/audio) ~ 50 MB
#   - 70% de los registros son texto, 30% multimedia
#   - costo almacenamiento ~ 0.02 USD por GB al mes 
# Esto es  para mostrar que también se pueden hacer análisis de costos.


print("Algoritmo 4: Costos del sistema de biblioteca ")

total_registros = len(data)
texto = int(total_registros * 0.7)
multimedia = total_registros - texto

mb_texto = texto * 1              # 1 MB por libro de texto
mb_multimedia = multimedia * 50   # 50 MB por recurso multimedia

mb_total = mb_texto + mb_multimedia
gb_total = mb_total / 1024.0

costo_por_gb = 0.02  # USD/GB/mes 
costo_mensual = gb_total * costo_por_gb

print(f"Registros totales: {total_registros}")
print(f"Libros tipo texto aprox.: {texto}")
print(f"Recursos multimedia aprox.: {multimedia}")
print(f"Almacenamiento total estimado: {gb_total:.2f} GB")
print(f"Costo mensual estimado (solo storage): ${costo_mensual:.2f} USD\n")



# ALGORITMO 5: Library Data Processing Performance
# Aquí es ver "cómo se comporta" el sistema con:
#   - distintos tamaños de biblioteca
#   - distintos tamaños de cluster (número de nodos)
#  formula sencilla:
#   tiempo ~ num_registros / (nodos * factor)
# Mientras más nodos tenga el cluster, menos tiempo.


print("Algoritmo 5: Rendimiento del procesamiento de datos")

def tiempo_procesamiento(num_registros, nodos_cluster, factor=100000):
    """
    Función mega simple para simular el tiempo de análisis.
    Entre más nodos tenga el cluster, más rápido debería ir.
    """
    return num_registros / (nodos_cluster * factor)


tamanos_biblioteca = [len(data), 100000, 1000000]  # tamaño actual, 100k y 1M
nodos_posibles = [1, 4, 8, 16]

for size in tamanos_biblioteca:
    print(f"\nSimulación para biblioteca con {size} registros:")
    for nodos in nodos_posibles:
        t = tiempo_procesamiento(size, nodos)
        print(f"- Cluster con {nodos} nodos -> tiempo aprox.: {t:.4f} unidades")

