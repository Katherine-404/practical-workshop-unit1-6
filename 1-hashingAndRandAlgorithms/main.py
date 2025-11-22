import random
import json
import os
from datetime import datetime

class LibrarySystem:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(size)] 
        self.genre_index = {} 
        self.all_books_ref = [] 

    def _hash_function(self, key):
        return hash(key) % self.size

    def insert_book(self, book):

        index = self._hash_function(book['_id'])
        self.table[index].append(book)
        
        genre = book['genre'].lower()
        if genre not in self.genre_index:
            self.genre_index[genre] = []
        self.genre_index[genre].append(book)

        self.all_books_ref.append(book)

    def search_by_id(self, book_id):
        index = self._hash_function(book_id)
        for book in self.table[index]:
            if book['_id'] == book_id:
                return book
        return None

    def search_flexible(self, query, filter_type):

        results = []
        query = query.lower()
        
        for book in self.all_books_ref:
            if query in book[filter_type].lower():
                results.append(book)
        return results

    def get_books_by_genre(self, genre):
        return self.genre_index.get(genre.lower(), [])

    def recommend_books(self, genre_preference=None, k=3):
        candidates = []
        
        if genre_preference:
            candidates = self.get_books_by_genre(genre_preference)
            if len(candidates) < k:
                candidates.extend(self.all_books_ref)
        else:
            candidates = self.all_books_ref

        candidates = list({v['_id']:v for v in candidates}.values())

        if not candidates:
            return []

        recommendations = []
        max_attempts = k * 5
        attempts = 0
        
        total_views = sum(b['views'] for b in candidates)

        while len(recommendations) < k and attempts < max_attempts:
            attempts += 1
            chosen = None

            if total_views == 0:
                chosen = random.choice(candidates)
            else:
                pick = random.uniform(0, total_views)
                current = 0
                for book in candidates:
                    current += book['views']
                    if current > pick:
                        chosen = book
                        break
            
            if chosen and chosen not in recommendations:
                recommendations.append(chosen)
                
        return recommendations

    def register_interaction(self, book_id):
        book = self.search_by_id(book_id)
        if book:
            book['views'] += 1
            book['lastAccessed'] = datetime.now().isoformat()
            return book
        return None

def cargar_datos(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def mostrar_libros(lista_libros):
    if not lista_libros:
        print("\n>> No se encontraron resultados.")
        return False
    
    print(f"\n{'ID':<6} | {'VISTAS':<8} | {'GÉNERO':<10} | {'TÍTULO Y AUTOR'}")
    print("-" * 60)
    for b in lista_libros:
        print(f"{b['_id']:<6} | {b['views']:<8} | {b['genre']:<10} | {b['title']} por {b['author']}")
    
    input("\nPresiona Enter para continuar...")
    return True

def main():
    archivo = "biblioteca.json"
    datos = cargar_datos(archivo)

    sistema = LibrarySystem()
    for d in datos:
        sistema.insert_book(d)

    while True:
        print("\n" + "="*40)
        print("   MOTOR DE BÚSQUEDA DE BIBLIOTECA DIGITAL")
        print("="*40)
        print("1. Buscar por Título")
        print("2. Buscar por Autor")
        print("3. Buscar por Género")
        print("4. Obtener Recomendaciones (Algoritmo Aleatorio)")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ")

        if opcion == '1':
            q = input("Ingresa parte del título: ")
            resultados = sistema.search_flexible(q, 'title')
            mostrar_libros(resultados)

        elif opcion == '2':
            q = input("Ingresa nombre del autor: ")
            resultados = sistema.search_flexible(q, 'author')
            mostrar_libros(resultados)

        elif opcion == '3':
            q = input("Ingresa género (ej. ciencia, ficcion): ")
            resultados = sistema.get_books_by_genre(q)
            mostrar_libros(resultados)

        elif opcion == '4':
            print("\nGenerando recomendaciones personalizadas...")
            print("Presiona Enter para recomendaciones generales o escribe un género preferido.")
            pref = input("Género preferido (opcional): ").strip()
            
            recs = sistema.recommend_books(genre_preference=pref if pref else None, k=3)
            print("\n--- TE RECOMENDAMOS LEER: ---")
            mostrar_libros(recs)

        elif opcion == '5':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()