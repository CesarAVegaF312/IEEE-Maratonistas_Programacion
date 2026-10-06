"""
Estructuras de datos — Montículo con heapq («Binary heap / priority queue»)
Nivel: Básico
Ejecutar: python monticulo_heapq.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Mantener una colección que cambia y responder rápido «¿cuál es el
    mínimo (o el máximo)?»: insertar y sacar el mínimo en O(log N), ver el
    mínimo en O(1). Es la cola de prioridad de Dijkstra, Prim, Huffman,
    los voraces con «arrepentimiento» y las simulaciones por eventos.
    Señales en el enunciado: «en cada paso tomar el menor/mayor», «los K
    mayores», «atender por prioridad», «el siguiente evento en el tiempo»,
    elementos que llegan y se van mientras se consulta el extremo.

FUNCIÓN
    heapq (biblioteca estándar) trabaja sobre una lista común:
        heapq.heapify(a)          O(N)       convierte a en min-heap
        heapq.heappush(a, x)      O(log N)
        heapq.heappop(a)          O(log N)   saca y devuelve el mínimo
        a[0]                      O(1)       ver el mínimo sin sacarlo
        heapq.heappushpop(a, x)   O(log N)   push y luego pop (más rápido)
        heapq.nsmallest(k, it) / nlargest(k, it)
    Funciones de este archivo:
    k_esimo_mayor(a, k) -> valor        k-ésimo mayor (k = 1 es el máximo).
    mezclar_k_listas(listas) -> list    une K listas ORDENADAS en una ordenada.
    class MonticuloBorrable             min-heap con borrado de un valor
        agregar(x), borrar(x), minimo(), sacar(), len()   (borrado perezoso)

IDEA Y ALGORITMO
    Un montículo binario es un árbol casi completo guardado en un arreglo
    (hijos de i en 2i+1 y 2i+2) donde cada padre es <= que sus hijos: el
    mínimo está en a[0]. Insertar = poner al final y «subir»; sacar = mover
    el último a la raíz y «bajar». Ambos recorren una rama: O(log N).
    MÁXIMOS: heapq solo hace mínimos; para un max-heap se guarda -x (o
    (-prioridad, dato)). Las tuplas se comparan por componentes: el primer
    campo es la prioridad y los siguientes desempatan.
    K-ÉSIMO MAYOR: mantener un min-heap con los K mayores vistos; si tiene
    más de K, sacar el mínimo. Al final la raíz es el k-ésimo mayor.
    O(N log K) en vez de O(N log N) de ordenar, y sirve en streaming.
    MEZCLA DE K LISTAS: el heap guarda el primer elemento pendiente de cada
    lista (valor, lista, posición); se saca el menor y se mete el siguiente
    de su lista. O(T log K) con T elementos en total.
    BORRADO PEREZOSO: heapq no sabe borrar un elemento arbitrario. Se anota
    en un contador «pendiente de borrar» y se ignora cuando llega a la
    raíz: antes de mirar a[0], sacar mientras la raíz esté pendiente. Cada
    elemento se saca una vez, así que el costo amortizado sigue siendo
    O(log N). Sirve para «máximo de una ventana deslizante», mediana
    dinámica con borrados, Dijkstra sin decrease-key (es lo mismo: las
    entradas viejas se ignoran).

MACROALGORITMO
    Borrado perezoso:
    1. agregar(x): heappush(x); tamaño += 1.
    2. borrar(x): pendientes[x] += 1; tamaño -= 1 (x debe estar presente).
    3. limpiar(): mientras heap[0] tenga pendientes, sacarlo y descontar.
    4. minimo(): limpiar() y devolver heap[0].
    5. sacar(): limpiar(), heappop, tamaño -= 1.

COMPLEJIDAD
    push/pop O(log N); heapify O(N); k_esimo_mayor O(N log K);
    mezclar_k_listas O(T log K); borrado perezoso O(log N) amortizado,
    memoria hasta O(total de inserciones). En Python ~10^6 push/pop por
    segundo.

EJEMPLO A MANO
    a = [5, 1, 9, 3, 7], k_esimo_mayor(a, 2) (min-heap de tamaño 2):
      5 → {5};  1 → {1,5};  9 → {1,5,9} > 2, sacar 1 → {5,9}
      3 → {3,5,9} sacar 3 → {5,9};  7 → {5,7,9} sacar 5 → {7,9}
      raíz = 7.
    MonticuloBorrable: agregar 4, 2, 8; borrar 2 (pendiente) → minimo():
      raíz 2 está pendiente → se saca → raíz 4.

ERRORES TÍPICOS
    - Olvidar que heapq es de mínimos (y negar mal: -x con tuplas hay que
      negar solo la prioridad).
    - Meter tuplas (prioridad, objeto) con objetos no comparables: en un
      empate de prioridad Python compara los objetos y lanza TypeError.
      Agregar un contador o índice como segundo campo.
    - Leer a[0] con borrado perezoso sin limpiar primero.
    - Creer que la lista del heap está ordenada: solo a[0] es el mínimo.
    - Usar heapq.heappop en una lista que no se hizo heapify.

VARIANTES Y RELACIONADOS
    - Mediana dinámica: max-heap con la mitad baja + min-heap con la alta.
    - Dos montículos «disponibles / ocupados» para simulaciones.
    - 02_Voraz/huffman.py, 02_Voraz/voraz_con_monticulo.py,
      05_Grafos/dijkstra.py, 05_Grafos/mst.py (Prim).
    - Si hacen falta sucesor/predecesor o borrar y ordenar todo, un
      segment tree o Fenwick sobre valores comprimidos
      (06_EstructurasDatos/fenwick.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/G - Math United FC (max-heap con valores negados)
    - ICPC/Colombia 2025/E - Efficient Encoding (Huffman con heapq)
    - ICPC/Colombia 2025/C - Celestial Veins (heapq.nsmallest para los K
      vecinos más cercanos)
    - ICPC/Colombia 2023/G - Grain Silos (cola de prioridad de A*)
    - CSES «Room Allocation»; LeetCode 23 «Merge k Sorted Lists»;
      LeetCode 215 «Kth Largest Element in an Array».

VERIFICACIÓN
    - Pruebas (python monticulo_heapq.py): k_esimo_mayor contra sorted en
      1000 casos; mezclar_k_listas contra sorted de la concatenación en 500
      casos; MonticuloBorrable contra una lista ordinaria (min/remove) en
      300 secuencias aleatorias de 60 operaciones; casos borde.
"""
import heapq
import random
from collections import Counter


def k_esimo_mayor(a, k):
    """k-ésimo mayor de a (1 <= k <= len(a)) con un min-heap de tamaño k."""
    heap = []
    for x in a:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)   # sale el menor de los k, entra x
    return heap[0]                       # el menor de los k mayores


def mezclar_k_listas(listas):
    """Une listas ya ordenadas en una sola lista ordenada."""
    # (valor, índice de lista, posición): el índice desempata sin comparar listas.
    heap = [(l[0], i, 0) for i, l in enumerate(listas) if l]
    heapq.heapify(heap)
    res = []
    while heap:
        v, i, p = heapq.heappop(heap)
        res.append(v)
        if p + 1 < len(listas[i]):
            heapq.heappush(heap, (listas[i][p + 1], i, p + 1))
    return res


class MonticuloBorrable:
    """Min-heap que además permite borrar un valor cualquiera (borrado perezoso)."""

    def __init__(self):
        self.heap = []
        self.pendientes = Counter()   # valor -> cuántas copias faltan por borrar
        self.tam = 0                  # elementos VIVOS

    def agregar(self, x):
        heapq.heappush(self.heap, x)
        self.tam += 1

    def borrar(self, x):
        """Borra una copia de x (debe estar presente)."""
        self.pendientes[x] += 1
        self.tam -= 1

    def _limpiar(self):
        # Sacar de la raíz los valores ya borrados: así heap[0] es un vivo.
        h, pend = self.heap, self.pendientes
        while h and pend[h[0]]:
            pend[heapq.heappop(h)] -= 1

    def minimo(self):
        self._limpiar()
        return self.heap[0]

    def sacar(self):
        self._limpiar()
        self.tam -= 1
        return heapq.heappop(self.heap)

    def __len__(self):
        return self.tam


def demo():
    a = [5, 1, 9, 3, 7]
    h = list(a)
    heapq.heapify(h)
    print("min-heap de", a, "-> mínimo", h[0])                        # 1
    hmax = [-x for x in a]
    heapq.heapify(hmax)
    print("max-heap (negados) -> máximo", -hmax[0])                    # 9
    print("2º mayor:", k_esimo_mayor(a, 2))                            # 7
    print("mezcla:", mezclar_k_listas([[1, 4, 9], [2, 3], [], [5, 10]]))
    m = MonticuloBorrable()
    for x in (4, 2, 8):
        m.agregar(x)
    m.borrar(2)
    print("borrable: agregar 4 2 8, borrar 2 -> mínimo", m.minimo(), "tamaño", len(m))  # 4, 2


def pruebas():
    random.seed(215)

    # Casos borde
    assert k_esimo_mayor([7], 1) == 7
    assert k_esimo_mayor([3, 3, 3], 2) == 3
    assert mezclar_k_listas([]) == [] and mezclar_k_listas([[], []]) == []
    m = MonticuloBorrable()
    m.agregar(5); m.agregar(5); m.borrar(5)
    assert m.minimo() == 5 and len(m) == 1
    assert m.sacar() == 5 and len(m) == 0

    for _ in range(1000):
        a = [random.randint(-20, 20) for _ in range(random.randint(1, 30))]
        k = random.randint(1, len(a))
        assert k_esimo_mayor(a, k) == sorted(a, reverse=True)[k - 1]

    for _ in range(500):
        listas = [sorted(random.randint(0, 50) for _ in range(random.randint(0, 8)))
                  for _ in range(random.randint(0, 6))]
        assert mezclar_k_listas(listas) == sorted(x for l in listas for x in l)

    # Borrado perezoso contra una lista simple
    for _ in range(300):
        m, ref = MonticuloBorrable(), []
        for _ in range(60):
            op = random.random()
            if op < 0.45 or not ref:
                x = random.randint(0, 10)
                m.agregar(x); ref.append(x)
            elif op < 0.75:
                x = random.choice(ref)
                m.borrar(x); ref.remove(x)
            elif op < 0.9:
                assert m.minimo() == min(ref)
            else:
                x = m.sacar()
                assert x == min(ref)
                ref.remove(x)
            assert len(m) == len(ref)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
