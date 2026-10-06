"""
Voraz — Código de Huffman («Huffman coding»)
Nivel: Intermedio
Ejecutar: python huffman.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dadas las frecuencias f_i de N símbolos, construir un código binario
    LIBRE DE PREFIJOS (ninguna palabra es prefijo de otra) que minimice la
    longitud total Σ f_i · |código_i|. El mismo algoritmo resuelve
    «juntar montones de a dos pagando la suma, con costo total mínimo».
    Señales en el enunciado: «codificación / compresión óptima», «código
    libre de prefijos», «unir cuerdas / montones / archivos de a dos y cada
    unión cuesta la suma», N hasta 10^5–10^6.

FUNCIÓN
    costo_huffman(frecuencias) -> int
        Costo mínimo Σ f_i · longitud_i (= suma de los pesos de todas las
        uniones). Con N <= 1 devuelve 0 (no hay uniones).
    codigos_huffman(frecuencias) -> list[str]
        Una palabra de código óptima por símbolo (en el orden de entrada).
        Con N = 1 devuelve ["0"] (longitud 1, la convención usual).

IDEA Y ALGORITMO
    Mientras quede más de un peso, sacar los DOS MENORES, unirlos en un nodo
    con peso = suma y volver a meterlo. Cada unión baja un nivel a todos los
    símbolos que contiene, así que el costo total es la suma de los pesos
    de los nodos creados.
    Por qué es óptimo:
      - En un árbol óptimo, los dos símbolos de MENOR frecuencia pueden
        ponerse como hermanos en el nivel más profundo: si no lo están,
        intercambiarlos con los dos hermanos más profundos no aumenta el
        costo (argumento de intercambio: se mueve lo menos frecuente a lo
        más largo).
      - Fusionados en un solo símbolo de peso x + y, el problema es igual
        con N - 1 símbolos y costo menor exactamente en x + y. Por
        inducción, el voraz es óptimo.
    El montículo (heapq) da los dos menores en O(log N). Ordenar una sola
    vez no basta, porque los nodos nuevos se intercalan (aunque si las
    frecuencias ya vienen ordenadas hay una versión O(N) con dos colas).

MACROALGORITMO
    1. Meter todas las frecuencias en un montículo de mínimos.
    2. Mientras haya más de un elemento:
       a. x = sacar mínimo, y = sacar mínimo.
       b. costo += x + y; meter x + y (recordando sus hijos si se quieren
          los códigos).
    3. Para los códigos: recorrer el árbol desde la raíz agregando '0' al
       ir al hijo izquierdo y '1' al derecho; la hoja i recibe su palabra.

COMPLEJIDAD
    O(N log N) tiempo, O(N) memoria. En Python, N = 10^6 en ~1,5 s.

EJEMPLO A MANO
    frecuencias: a=5, b=9, c=12, d=13, e=16, f=45
      5+9 = 14     → {12, 13, 14, 16, 45}
      12+13 = 25   → {14, 16, 25, 45}
      14+16 = 30   → {25, 30, 45}
      25+30 = 55   → {45, 55}
      45+55 = 100  → {100}
    costo = 14 + 25 + 30 + 55 + 100 = 224
    longitudes: f = 1, c = d = e = 3, a = b = 4 → 45 + 3·41 + 4·14 = 224.

ERRORES TÍPICOS
    - N = 1: según el enunciado el costo es 0 (no hay uniones) o f_1
      (palabra de longitud 1). Revisarlo con el ejemplo.
    - Meter nodos al heap como tuplas (peso, nodo) cuando el nodo no es
      comparable: en empates Python intenta comparar los nodos y falla.
      Usar (peso, contador, nodo) o índices enteros.
    - Usar recursión para asignar códigos en árboles muy profundos
      (frecuencias tipo Fibonacci dan profundidad N): usar una pila.
    - Confundir con «unir montones ADYACENTES» (solo vecinos): eso es DP de
      intervalos (o Garsia–Wachs), no Huffman.

VARIANTES Y RELACIONADOS
    - Huffman k-ario: rellenar con ceros hasta que (N - 1) % (k - 1) == 0 y
      unir de a k.
    - Frecuencias ya ordenadas: dos colas (deque) en O(N).
    - 06_EstructurasDatos/monticulo_heapq.py, 02_Voraz/argumento_intercambio.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2025/E - Efficient Encoding (costo de Huffman evaluado
      en varios instantes)
    - UVa 10954 «Add All» (exactamente costo_huffman).

VERIFICACIÓN
    - Pruebas (python huffman.py): costo contra fuerza bruta en 500 casos
      aleatorios (N <= 5, y 40 con N = 6): se prueban todas las asignaciones
      de longitudes que cumplen la desigualdad de Kraft Σ 2^-l_i <= 1 (que
      es justo la condición para que exista un código libre de prefijos con
      esas longitudes). Los códigos se validan: libres de prefijos y con
      Σ f·|código| igual al costo. Más casos borde y N = 10^5.
"""
import heapq
import random
from itertools import product


def costo_huffman(frecuencias):
    """Costo mínimo de un código libre de prefijos (= suma de las uniones)."""
    heap = list(frecuencias)
    heapq.heapify(heap)
    costo = 0
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        costo += x + y              # cada unión baja un nivel a todo lo que contiene
        heapq.heappush(heap, x + y)
    return costo


def codigos_huffman(frecuencias):
    """Palabras de un código de Huffman, en el orden de entrada."""
    n = len(frecuencias)
    if n == 0:
        return []
    if n == 1:
        return ["0"]
    # Nodos 0..n-1 son hojas; los nuevos se numeran n, n+1, … (índices enteros:
    # en empates de peso el heap compara índices, nunca objetos raros).
    hijos = [None] * n
    heap = [(f, i) for i, f in enumerate(frecuencias)]
    heapq.heapify(heap)
    while len(heap) > 1:
        fx, x = heapq.heappop(heap)
        fy, y = heapq.heappop(heap)
        hijos.append((x, y))
        heapq.heappush(heap, (fx + fy, len(hijos) - 1))
    # Asignar códigos con pila explícita (el árbol puede tener profundidad N).
    codigos = [""] * n
    pila = [(len(hijos) - 1, "")]
    while pila:
        v, pref = pila.pop()
        if v < n:
            codigos[v] = pref
        else:
            izq, der = hijos[v]
            pila.append((izq, pref + "0"))
            pila.append((der, pref + "1"))
    return codigos


def demo():
    frec = [5, 9, 12, 13, 16, 45]
    cod = codigos_huffman(frec)
    print("frecuencias =", frec)
    print("códigos     =", cod)
    print("costo       =", costo_huffman(frec))                        # 224
    print("Σ f·|cód|   =", sum(f * len(c) for f, c in zip(frec, cod)))  # 224


def _bruta(frec):
    """Mínimo de Σ f_i·l_i sobre longitudes que cumplen Kraft: Σ 2^(L-l_i) <= 2^L."""
    n = len(frec)
    if n <= 1:
        return 0
    L = n - 1                       # ninguna palabra óptima es más larga que n-1
    mejor = None
    for longs in product(range(1, L + 1), repeat=n):
        if sum(1 << (L - l) for l in longs) <= 1 << L:
            c = sum(f * l for f, l in zip(frec, longs))
            if mejor is None or c < mejor:
                mejor = c
    return mejor


def _libre_de_prefijos(codigos):
    return not any(i != j and b.startswith(a)
                   for i, a in enumerate(codigos) for j, b in enumerate(codigos))


def pruebas():
    random.seed(10954)

    # Casos borde
    assert costo_huffman([]) == 0 and codigos_huffman([]) == []
    assert costo_huffman([7]) == 0 and codigos_huffman([7]) == ["0"]
    assert costo_huffman([1, 2, 3]) == 9           # UVa 10954: (1+2) + (3+3)
    assert costo_huffman([1, 2, 3, 4]) == 19
    assert costo_huffman([5, 5, 5, 5]) == 40       # todos iguales: árbol balanceado
    assert costo_huffman([0, 0, 0]) == 0

    casos = [random.randint(1, 5) for _ in range(500)] + [6] * 40
    for n in casos:
        frec = [random.randint(0, 30) for _ in range(n)]
        costo = costo_huffman(frec)
        assert costo == _bruta(frec)
        cod = codigos_huffman(frec)
        assert _libre_de_prefijos(cod) and all(set(c) <= {"0", "1"} for c in cod)
        if n >= 2:
            assert sum(f * len(c) for f, c in zip(frec, cod)) == costo

    # Profundidad grande (frecuencias tipo potencias de 2) y N grande
    frec = [1 << i for i in range(60)]
    cod = codigos_huffman(frec)
    assert max(len(c) for c in cod) == 59 and _libre_de_prefijos(cod)
    grande = [random.randint(1, 10**9) for _ in range(100000)]
    assert costo_huffman(grande) == sum(f * len(c) for f, c in zip(grande, codigos_huffman(grande)))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
