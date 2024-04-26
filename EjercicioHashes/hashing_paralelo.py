import hashlib
import threading
from queue import Queue

# Función para calcular el hash SHA-1 de una cadena

def calculate_sha1(text):

    return hashlib.sha1(text.encode()).hexdigest()

class Worker(threading.Thread):

    def __init__(self, queue, hashes_to_find, found_hashes, lock):
    
        threading.Thread.__init__(self)
    
        self.queue = queue
    
        self.hashes_to_find = hashes_to_find
    
        self.found_hashes = found_hashes
    
        self.lock = lock

    def run(self):

        while not self.queue.empty():
        
            line = self.queue.get()
        
            line_hash = calculate_sha1(line)
        
            if line_hash in self.hashes_to_find:
        
                with self.lock:
        
                    self.found_hashes.append({line: line_hash})
        
                    print(f"[Found] {line} => {line_hash}")
        
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
    
    for _ in range(10):  # Número de hilos
    
        worker = Worker(queue, hashes_to_find, found_hashes, lock)
    
        worker.start()
    
        threads.append(worker)

        print(f"Hilo {_} creado.")

    # Esperar que todos los hilos terminen
    
    for thread in threads:
    
        thread.join()

    # Imprimir los resultados finales
    
    print(found_hashes)

if __name__ == '__main__':
    main()
