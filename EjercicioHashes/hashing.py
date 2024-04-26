import hashlib

# Función para calcular el hash SHA-1 de una cadena

def calculate_sha1(text):

    return hashlib.sha1(text.encode()).hexdigest()

def main():

    lista_hashes_a_encontrar = []

    lista_hashes_encontrados = []

    with open('target_hashes.txt', 'r') as file:

        for line in file:

            line = line.strip()

            if line:

                lista_hashes_a_encontrar.append(line)

    with open('realhuman_phill.txt', 'r', encoding='latin-1') as file:

        for line in file:

            line = line.strip()

            if line:

                line_hash = calculate_sha1(line)


                hash_encontrado = True if line_hash in lista_hashes_a_encontrar else False

                if hash_encontrado:

                    print(f"[{hash_encontrado}] {line} => {line_hash}")

                    lista_hashes_encontrados.append({line: line_hash})
    

    print(lista_hashes_encontrados)


if __name__ == '__main__':

    main()