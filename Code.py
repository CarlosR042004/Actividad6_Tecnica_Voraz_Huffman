import heapq

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def calcular_frecuencia(archivo):
    frecuencia = {}
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        for caracter in contenido:
            if caracter in frecuencia:
                frecuencia[caracter] += 1
            else:
                frecuencia[caracter] = 1
    return frecuencia

def construir_arbol_huffman(frecuencias):
    heap = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        izquierdo = heapq.heappop(heap)
        derecho = heapq.heappop(heap)
        nodo_padre = NodoHuffman(None, izquierdo.frecuencia + derecho.frecuencia)
        nodo_padre.izquierda = izquierdo
        nodo_padre.derecha = derecho
        heapq.heappush(heap, nodo_padre)

    return heap[0]

def imprimir_arbol_huffman(nodo, prefijo=""):
    if nodo is not None:
        if nodo.caracter is not None:
            caracter_mostrado = repr(nodo.caracter)  
            print(f"Caracter: {caracter_mostrado}, Frecuencia: {nodo.frecuencia}, Código: {prefijo}")
        imprimir_arbol_huffman(nodo.izquierda, prefijo + "0")
        imprimir_arbol_huffman(nodo.derecha, prefijo + "1")


def main():
    nombre_archivo = 'C:/Users/Carlo/Desktop/Libro.txt'  
    frecuencias = calcular_frecuencia(nombre_archivo)
    raiz = construir_arbol_huffman(frecuencias)
    imprimir_arbol_huffman(raiz)

if __name__ == "__main__":
    main()

