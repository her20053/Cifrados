import hashlib
import threading
from queue import Queue
from itertools import permutations, product

variants_dict = {
    'prefixes': [
        '', 'my', 'the', 'super', 'ultra', 'mega', 
        'best', 'pro', 'top', 'new'
    ],
    'suffixes': [
        '', '2023', '123', 'online', 'x', '101', 
        'now', '247', 'hq', 'inc'
    ]
}


# Función para calcular el hash SHA-1 de una cadena
def calculate_sha1(text):
    return hashlib.sha1(text.encode()).hexdigest()

def generate_variants(word):
    variants = [word, word.lower(), word.upper(), word.title()]

    # Permutaciones de la palabra si no es muy larga para evitar demasiadas permutaciones
    if len(word) <= 5:
        permuted = [''.join(p) for p in permutations(word)]
        variants.extend(permuted)

    # Utilizar el diccionario de variantes
    prefixes = variants_dict['prefixes']
    suffixes = variants_dict['suffixes']

    # Productos de prefijos y sufijos
    for pre, suf in product(prefixes, suffixes):
        variant = f"{pre}{word}{suf}"
        variants.append(variant)

    return set(variants)  # Usar set para eliminar duplicados


class Worker(threading.Thread):
    def __init__(self, queue, hashes_to_find, found_hashes, lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.hashes_to_find = hashes_to_find
        self.found_hashes = found_hashes
        self.lock = lock

    def run(self):
        while not self.queue.empty():
            word = self.queue.get()
            variants = generate_variants(word)
            for variant in variants:
                variant_hash = calculate_sha1(variant)
                if variant_hash in self.hashes_to_find:
                    with self.lock:
                        self.found_hashes.append({variant: variant_hash})
                        print(f"[Found] {variant} => {variant_hash}")
            self.queue.task_done()

def main():
    hashes_to_find = []
    found_hashes = []
    lock = threading.Lock()
    queue = Queue()

    # Cargar hashes objetivo
    with open('target_hashes.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                hashes_to_find.append(line)
    print("Lista de hashes objetivo cargada.")

    # Leer líneas y ponerlas en la cola
    with open('realhuman_phill.txt', 'r', encoding='latin-1') as file:
        for line in file:
            line = line.strip()
            if line:
                queue.put(line)
    print("Lista de palabras cargada.")

    # Crear y empezar los hilos
    threads = []
    for i in range(10):  # Número de hilos
        worker = Worker(queue, hashes_to_find, found_hashes, lock)
        worker.start()
        threads.append(worker)
        print(f"Hilo {i} creado.")

    # Esperar que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Imprimir los resultados finales
    print(found_hashes)

if __name__ == '__main__':
    main()
