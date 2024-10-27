import os
import heapq
import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt

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

def generar_codigos_binarios(nodo, prefijo="", codigos={}):
    if nodo is not None:
        if nodo.caracter is not None:
            codigos[nodo.caracter] = prefijo
        generar_codigos_binarios(nodo.izquierda, prefijo + "0", codigos)
        generar_codigos_binarios(nodo.derecha, prefijo + "1", codigos)
    return codigos

def codificar_contenido(contenido, codigos):
    """Codifica el contenido usando los códigos de Huffman"""
    return ''.join([codigos[caracter] for caracter in contenido])

def mostrar_codigos_y_frecuencias(codigos, frecuencias):
    ventana_codigos = tk.Toplevel()
    ventana_codigos.title("Códigos Binarios y Frecuencias")

    scrollbar = tk.Scrollbar(ventana_codigos)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    texto_codigos = tk.Text(ventana_codigos, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    
    texto_codigos.insert(tk.END, "Caracter | Frecuencia | Código\n")
    texto_codigos.insert(tk.END, "-" * 30 + "\n")
    for caracter, codigo in codigos.items():
        texto_codigos.insert(tk.END, f"{repr(caracter):>8} | {frecuencias[caracter]:>9} | {codigo}\n")
    texto_codigos.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=texto_codigos.yview)

    boton_regresar = tk.Button(ventana_codigos, text="Regresar", command=ventana_codigos.destroy)
    boton_regresar.pack()

def calcular_codigos_y_frecuencias():
    archivo = entrada_archivo.get()
    if not archivo:
        messagebox.showerror("Error", "Por favor, ingresa la ruta del archivo")
        return
    try:
        frecuencias = calcular_frecuencia(archivo)
        raiz = construir_arbol_huffman(frecuencias)
        codigos = generar_codigos_binarios(raiz)
        mostrar_codigos_y_frecuencias(codigos, frecuencias)  
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def dibujar_arbol_huffman(nodo):
    G = nx.DiGraph()  
    etiquetas = {}  

    def agregar_nodo_al_grafo(nodo, posicion, padre=None, direccion=""):
        if nodo is not None:
            etiqueta = f"{nodo.caracter}:{nodo.frecuencia}" if nodo.caracter else str(nodo.frecuencia)
            G.add_node(posicion)
            etiquetas[posicion] = etiqueta
            if padre is not None:
                G.add_edge(padre, posicion, label=direccion)  
            agregar_nodo_al_grafo(nodo.izquierda, posicion * 2, posicion, "0")
            agregar_nodo_al_grafo(nodo.derecha, posicion * 2 + 1, posicion, "1")

    agregar_nodo_al_grafo(nodo, 1) 

    pos = nx.spring_layout(G)  
    nx.draw(G, pos, labels=etiquetas, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Árbol de Huffman")
    plt.show()

def calcular_e_imprimir_arbol():
    archivo = entrada_archivo.get()
    if not archivo:
        messagebox.showerror("Error", "Por favor, ingresa la ruta del archivo")
        return
    try:
        frecuencias = calcular_frecuencia(archivo)
        raiz = construir_arbol_huffman(frecuencias)
        dibujar_arbol_huffman(raiz)  
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def codificar_archivo():
    archivo = entrada_archivo.get()
    if not archivo:
        messagebox.showerror("Error", "Por favor, ingresa la ruta del archivo")
        return
    try:
        frecuencias = calcular_frecuencia(archivo)
        raiz = construir_arbol_huffman(frecuencias)
        codigos = generar_codigos_binarios(raiz)
        
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        contenido_codificado = codificar_contenido(contenido, codigos)
        
        ruta_codificado = os.path.join(os.getcwd(), "archivo_codificado.txt")
        with open(ruta_codificado, "w") as f:
            f.write(contenido_codificado)
        
        tamano_original, tamano_codificado = comparar_tamaños(archivo, contenido_codificado)
        mostrar_resultado_comparacion(tamano_original, tamano_codificado)

        messagebox.showinfo("Éxito", f"El archivo ha sido codificado y guardado en '{ruta_codificado}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo no encontrado")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def comparar_tamaños(archivo_original, contenido_codificado):
    tamano_original = os.path.getsize(archivo_original)

    tamano_codificado = len(contenido_codificado)

    return tamano_original, tamano_codificado

def mostrar_resultado_comparacion(tamano_original, tamano_codificado):
    ventana_comparacion = tk.Toplevel()
    ventana_comparacion.title("Comparación de Tamaños")

    texto_comparacion = tk.Text(ventana_comparacion, wrap=tk.WORD)
    texto_comparacion.insert(tk.END, f"Tamaño original: {tamano_original} bytes\n")
    texto_comparacion.insert(tk.END, f"Tamaño codificado: {tamano_codificado} bits\n")
    texto_comparacion.insert(tk.END, f"Ratio de compresión: {tamano_codificado / (tamano_original * 8):.2f}\n")
    texto_comparacion.pack(fill=tk.BOTH, expand=True)

    boton_regresar = tk.Button(ventana_comparacion, text="Regresar", command=ventana_comparacion.destroy)
    boton_regresar.pack()

def decodificar_archivo():
    try:
        ruta_codificado = os.path.join(os.getcwd(), "archivo_codificado.txt")
        with open(ruta_codificado, 'r') as f:
            contenido_codificado = f.read()

        archivo_original = entrada_archivo.get()
        frecuencias = calcular_frecuencia(archivo_original)
        raiz = construir_arbol_huffman(frecuencias)
        
        contenido_decodificado = decodificar_contenido(contenido_codificado, raiz)
        
        ruta_decodificado = os.path.join(os.getcwd(), "archivo_decodificado.txt")
        with open(ruta_decodificado, "w", encoding='utf-8') as f:
            f.write(contenido_decodificado)
        
        messagebox.showinfo("Éxito", f"El archivo ha sido decodificado y guardado en '{ruta_decodificado}'.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo codificado no encontrado")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decodificar_contenido(codigo_binario, arbol_huffman):
    resultado = []
    nodo = arbol_huffman
    for bit in codigo_binario:
        nodo = nodo.izquierda if bit == '0' else nodo.derecha
        if nodo.caracter is not None:
            resultado.append(nodo.caracter)
            nodo = arbol_huffman
    return ''.join(resultado)

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(title="Selecciona un archivo de texto")
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, archivo)

ventana = tk.Tk()
ventana.title("Algoritmo de Huffman")

label_archivo = tk.Label(ventana, text="Ruta del archivo:")
label_archivo.pack()

entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack()

boton_seleccionar = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar.pack()

boton_codigos_frecuencias = tk.Button(ventana, text="Códigos Binarios y Frecuencias", command=calcular_codigos_y_frecuencias)
boton_codigos_frecuencias.pack()

boton_codificar = tk.Button(ventana, text="Codificar Archivo y Comparar Tamaños", command=codificar_archivo)
boton_codificar.pack()

boton_decodificar = tk.Button(ventana, text="Decodificar Archivo", command=decodificar_archivo)
boton_decodificar.pack()

boton_arbol = tk.Button(ventana, text="Mostrar Árbol", command=calcular_e_imprimir_arbol)
boton_arbol.pack()

ventana.mainloop()
