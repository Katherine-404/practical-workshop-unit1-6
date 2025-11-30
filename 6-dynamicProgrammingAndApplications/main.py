import json
import math
import time
from datetime import datetime

class LibraryRecommender:
    def __init__(self, json_file):
        self.json_file = json_file
        self.books = self._load_data()

    def _load_data(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Base de datos cargada: {len(data)} libros procesados.")
                
                if data and '_id' not in data[0]:
                    print("ALERTA: No se detectó el campo '_id'. Verifica tu JSON.")
                return data
        except FileNotFoundError:
            print(f"Error Crítico: No se encuentra el archivo '{self.json_file}'")
            return []
        except json.JSONDecodeError:
            print(f"Error Crítico: El archivo '{self.json_file}' no es un JSON válido.")
            return []
    
    def _euclidean_distance(self, v1, v2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

    def _get_features(self, book):
        try:
            lib_sim = book['librarySimilarity']
            ratings = lib_sim['userRatings']
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            difficulty = lib_sim['difficultyLevel']
            return [avg_rating, difficulty]
        except KeyError:
            return [0, 0] 

    # ALGORITMO 1: Similitud básica (KNN en Calificación y Dificultad)
    def find_similar_books(self, target_id, k=5):
        target_book = next((b for b in self.books if b['_id'] == target_id), None)
        
        if not target_book:
            print(f"Libro con _id '{target_id}' no encontrado.")
            return []

        target_vector = self._get_features(target_book)
        candidates = []

        for book in self.books:
            if book['_id'] == target_id: continue

            current_vector = self._get_features(book)
            dist = self._euclidean_distance(target_vector, current_vector)
            candidates.append((book, dist))

        candidates.sort(key=lambda x: x[1])
        return candidates[:k]

    # ALGORITMO 2: Emparejamiento por Género (Filtro + KNN)
    def recommend_by_genre(self, target_id, k=5):
        target_book = next((b for b in self.books if b['_id'] == target_id), None)
        if not target_book: return []

        target_genre = target_book['librarySimilarity']['genre']
        target_vector = self._get_features(target_book)
        
        candidates = []
        for book in self.books:
            if book['_id'] == target_id: continue

            if book['librarySimilarity']['genre'] != target_genre:
                continue

            current_vector = self._get_features(book)
            dist = self._euclidean_distance(target_vector, current_vector)
            candidates.append((book, dist))

        candidates.sort(key=lambda x: x[1])
        return candidates[:k]

    # ALGORITMO 3: Nivel de Lectura (User-based filtering)
    def recommend_by_user_type(self, target_user, available_time_mins, k=5):
        candidates = []
        
        for book in self.books:
            lib_data = book['librarySimilarity']

            if lib_data['targetUser'] != target_user:
                continue

            time_diff = abs(lib_data['readingTime'] - available_time_mins)
            candidates.append((book, time_diff))
            
        candidates.sort(key=lambda x: x[1])
        return candidates[:k]

    # ALGORITMO 4: Benchmark de Rendimiento
    def run_performance_test(self):
        if not self.books: return
        test_id = self.books[0]['_id']
        
        print(f"\nINICIANDO BENCHMARK (Test ID: {test_id})")
        print("-" * 50)

        start = time.time()
        self.find_similar_books(test_id, k=10)
        dur_a = (time.time() - start) * 1000
        print(f"1. KNN Global (Espacio completo): {dur_a:.4f} ms")

        start = time.time()
        self.recommend_by_genre(test_id, k=10)
        dur_b = (time.time() - start) * 1000
        print(f"2. KNN por Género (Espacio reducido): {dur_b:.4f} ms")
        
        improvement = ((dur_a - dur_b) / dur_a) * 100
        print(f"Mejora de velocidad por reducción de dimensionalidad: {improvement:.2f}%")

    # ALGORITMO 5: Agrupación (Clustering simple)
    def analyze_clusters(self):
        clusters = {}
        
        for book in self.books:
            genre = book['librarySimilarity']['genre']
            if genre not in clusters: 
                clusters[genre] = {'count': 0, 'total_diff': 0, 'total_rating': 0}
            
            features = self._get_features(book)
            clusters[genre]['count'] += 1
            clusters[genre]['total_rating'] += features[0]
            clusters[genre]['total_diff'] += features[1]

        print("\nANÁLISIS DE CLÚSTERES (Centroides por Género)")
        print(f"{'GÉNERO':<15} | {'LIBROS':<8} | {'DIFICULTAD MEDIA':<18} | {'RATING MEDIO':<15}")
        print("-" * 65)
        
        for genre, data in clusters.items():
            avg_diff = data['total_diff'] / data['count']
            avg_rate = data['total_rating'] / data['count']
            print(f"{genre:<15} | {data['count']:<8} | {avg_diff:<18.2f} | {avg_rate:<15.2f}")

if __name__ == "__main__":
    engine = LibraryRecommender('biblioteca6.json')

    if engine.books:
        sample_book = engine.books[0]
        sample_id = sample_book['_id']
        sample_title = sample_book['title']
        
        print(f"\nLIBRO BASE: '{sample_title}'")
        print(f"   (ID: {sample_id})")
        print(f"   (Datos: {sample_book['librarySimilarity']})")

        print("\n--- 1. Libros Similares (Rating & Dificultad) ---")
        recs = engine.find_similar_books(sample_id, k=3)
        for book, dist in recs:
            stats = engine._get_features(book)
            print(f" » Dist: {dist:.3f} | {book['title'][:40]}... (Diff: {stats[1]}, Rating: {stats[0]:.1f})")

        print(f"\n--- 2. Recomendaciones en '{sample_book['librarySimilarity']['genre']}' ---")
        recs_genre = engine.recommend_by_genre(sample_id, k=3)
        for book, dist in recs_genre:
             print(f" » Dist: {dist:.3f} | {book['title'][:40]}...")

        print("\n--- 3. Para Estudiantes (Tiempo ~120 min) ---")
        recs_user = engine.recommend_by_user_type("student", 120, k=3)
        for book, diff in recs_user:
            print(f" » Desviación: {diff}m | {book['title'][:40]}... ({book['librarySimilarity']['readingTime']} min)")

        engine.run_performance_test()
        engine.analyze_clusters()