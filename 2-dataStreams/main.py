import random
import json
import os
import math
from datetime import datetime

#BLOOM FILTER
class BloomFilter:
    def __init__(self, size=5000, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, item):
        """Genera múltiples hash para un item"""
        results = []
        random.seed(hash(item))
        for _ in range(self.hash_count):
            results.append(random.randint(0, self.size - 1))
        return results

    def add(self, item):
        for h in self._hashes(item):
            self.bit_array[h] = 1

    def contains(self, item):
        return all(self.bit_array[h] == 1 for h in self._hashes(item))

#HYPERLOGLOG (CONTEO APROXIMADO)
class HyperLogLog:
    def __init__(self, b=4):
        self.b = b
        self.m = 1 << b
        self.registers = [0] * self.m

    def _hash(self, value):
        return hash(value)

    def add(self, value):
        x = self._hash(value)
        j = x & (self.m - 1)
        w = x >> self.b

        rho = 1
        while w & 1 == 0 and rho <= 32:
            rho += 1
            w >>= 1

        self.registers[j] = max(self.registers[j], rho)

    def count(self):
        Z = 1.0 / sum([2 ** -r for r in self.registers])
        E = self.m ** 2 * Z * 0.7213 / (1 + 1.079 / self.m)
        return int(E)
    
#DGIM ALGORITHM  
class DGIM:
    def __init__(self, window_size=50):
        self.window = window_size
        self.buckets = []

    def add_event(self, bit):
        """Añade evento (1 = acceso de libro)"""
        if bit == 1:
            self.buckets.insert(0, [1, 1])
            self._merge_buckets()

        for b in self.buckets:
            b[1] += 1

        self.buckets = [b for b in self.buckets if b[1] <= self.window]

    def _merge_buckets(self):
        i = 0
        while i < len(self.buckets) - 2:
            if (self.buckets[i][0] == self.buckets[i+1][0] == self.buckets[i+2][0]):
                self.buckets[i+2][0] *= 2
                del self.buckets[i]
            else:
                i += 1

    def count_events(self):
        total = 0
        if not self.buckets:
            return 0

        for size, timestamp in self.buckets[:-1]:
            total += size

        last_size, _ = self.buckets[-1]
        total += last_size // 2

        return total

class LibrarySystemU2:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)]
        
        self.genre_index = {}
        self.all_books_ref = []

        self.recent_access_bloom = BloomFilter()
        self.user_counter_hll = HyperLogLog()
        self.access_stream_dgim = DGIM()

        self.genre_frequency = {}

    def _hash_function(self, key):
        return hash(key) % self.size

    def insert_book(self, book):
        index = self._hash_function(book['_id'])
        self.table[index].append(book)

        genre = book['genre'].lower()
        if genre not in self.genre_index:
            self.genre_index[genre] = []
            self.genre_frequency[genre] = 0

        self.genre_index[genre].append(book)
        self.all_books_ref.append(book)

    def search_flexible(self, query, field):
        res = []
        for b in self.all_books_ref:
            if query.lower() in b[field].lower():
                res.append(b)
        return res

    def get_books_by_genre(self, genre):
        return self.genre_index.get(genre.lower(), [])

    def register_interaction(self, book_id, user_id="anon"):
        book = self.search_by_id(book_id)
        if not book:
            return None

        book["views"] += 1
        book["lastAccessed"] = datetime.now().isoformat()

        self.recent_access_bloom.add(book_id)
        self.user_counter_hll.add(user_id)
        self.genre_frequency[book["genre"]] += 1
        self.access_stream_dgim.add_event(1)

        return book

    def search_by_id(self, book_id):
        index = self._hash_function(book_id)
        for b in self.table[index]:
            if b["_id"] == book_id:
                return b
        return None

    def recommend_books(self, genre_preference=None, pattern="frequent"):
        pool = self.get_books_by_genre(genre_preference) if genre_preference else self.all_books_ref
        if not pool:
            pool = self.all_books_ref

        k = {"frequent": 5, "occasional": 3, "rare": 2}[pattern]

        return random.sample(pool, min(len(pool), k))

def cargar_datos(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def mostrar_libros(lista):
    if not lista:
        print("\nNo hubo resultados.")
        return
    print("\nID | VISTAS | GÉNERO | TÍTULO Y AUTOR")
    print("-"*60)
    for b in lista:
        print(f"{b['_id']} | {b['views']} | {b['genre']} | {b['title']} por {b['author']}")
    input("\nPresiona Enter...")

def main():
    archivo = "biblioteca2.json"
    datos = cargar_datos(archivo)

    sistema = LibrarySystemU2()
    for d in datos:
        sistema.insert_book(d)

    while True:
        print("\n===== MOTOR DE BÚSQUEDA DE BIBLIOTECA DIGITAL =====")
        print("1. Buscar por Título")
        print("2. Buscar por Autor")
        print("3. Buscar por Género")
        print("4. Recomendaciones Avanzadas")
        print("5. Revisar si libro fue accedido (Bloom Filter)")
        print("6. Ver usuarios únicos (HyperLogLog)")
        print("7. Accesos recientes (DGIM)")
        print("8. Salir")

        op = input("\nOpción: ")

        if op == "1":
            q = input("Título: ")
            mostrar_libros(sistema.search_flexible(q, "title"))

        elif op == "2":
            q = input("Autor: ")
            mostrar_libros(sistema.search_flexible(q, "author"))

        elif op == "3":
            q = input("Género: ")
            mostrar_libros(sistema.get_books_by_genre(q))

        elif op == "4":
            g = input("¿Género preferido?: ")
            p = input("Patrón (frequent, occasional, rare): ")
            recs = sistema.recommend_books(g if g else None, p)
            mostrar_libros(recs)

        elif op == "5":
            bid = input("ID: ")
            print("Sí" if sistema.recent_access_bloom.contains(bid) else "No")

        elif op == "6":
            print("Usuarios únicos aproximados:", sistema.user_counter_hll.count())

        elif op == "7":
            print("Accesos recientes estimados:", sistema.access_stream_dgim.count_events())

        elif op == "8":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
