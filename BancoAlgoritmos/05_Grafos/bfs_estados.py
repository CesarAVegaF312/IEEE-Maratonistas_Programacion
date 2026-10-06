"""
Grafos — BFS sobre espacio de estados («State-space BFS»)
Nivel: Intermedio
Ejecutar: python bfs_estados.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Muchos problemas de «mínimo número de operaciones» no traen un grafo
    explícito: los VÉRTICES son las configuraciones posibles (estados) y las
    ARISTAS son las operaciones permitidas. Si cada operación cuesta 1, el
    mínimo de operaciones es una distancia BFS en ese grafo implícito.
    Señales en el enunciado: «mínimo número de movimientos para llegar a la
    configuración X», jarras de agua, rompecabezas pequeños (8-puzzle),
    «el menor número que cumple…» construido dígito a dígito, posición +
    algo más (llaves recogidas, dirección, energía restante). Clave: que el
    número de estados distintos sea manejable (≤ ~10^6 en Python).

FUNCIÓN
    bfs_estados(inicio, vecinos, es_meta) -> list | None
        Genérico: inicio = estado hashable (tupla, int, str); vecinos(e) =
        iterable de estados siguientes; es_meta(e) -> bool. Devuelve la
        lista de estados de inicio a la primera meta (largo − 1 = mínimo de
        operaciones), o None si no se alcanza ninguna meta.
    jarras(A, B, T) -> list | None
        Jarras de capacidades A y B, empezando vacías; operaciones: llenar,
        vaciar, verter una en otra. Secuencia mínima de estados (a, b) hasta
        que alguna jarra tenga exactamente T litros, o None.
    menor_multiplo_01(N) -> int
        Menor M > 0 múltiplo de N escrito solo con dígitos 0 y 1
        (ICPC Colombia 2024 H, Only1s0s): BFS sobre los restos módulo N.

IDEA Y ALGORITMO
    1) Modelar: decidir qué información MÍNIMA describe una situación (el
       estado) y cuáles son las transiciones. El BFS de siempre (bfs.py)
       funciona igual, solo que dist/padre son diccionarios indexados por
       estado y los vecinos se generan al vuelo.
    2) Reducir el estado: dos situaciones que se comportan igual en el
       FUTURO pueden ser el mismo estado. En Only1s0s, el número construido
       puede tener decenas de cifras, pero solo importa su resto módulo N:
       si dos prefijos p y q tienen el mismo resto, agregarles los mismos
       dígitos da el mismo resto ((10r + d) mod N). Entonces basta visitar
       cada resto UNA vez → ≤ N estados (y por palomar M siempre existe).
       Como el BFS va por capas (número de cifras) y genera el dígito 0
       antes que el 1, el primer prefijo que alcanza un resto es el MENOR
       con ese resto; el primero con resto 0 es M.
    3) Jarras: estado (a, b) con 0 ≤ a ≤ A, 0 ≤ b ≤ B → (A+1)(B+1) estados y
       6 operaciones por estado. «Verter a en b» mueve min(a, B − b) litros.
       Hay solución ⇔ T ≤ máx(A, B) y T es múltiplo de mcd(A, B) (Bézout).

MACROALGORITMO
    1. Definir estado, estado inicial, metas y transiciones.
    2. padre = {inicio: None}; cola = deque([inicio]).
    3. Sacar e; si es meta, reconstruir siguiendo padre y devolver.
    4. Para cada sucesor s de e que no esté en padre: padre[s] = e, encolar.
    5. Si la cola se vacía: no hay solución.

COMPLEJIDAD
    O(S · T) con S estados y T transiciones por estado; memoria O(S).
    Jarras: O(A·B). Only1s0s: O(N). En Python ~10^5–10^6 estados por
    segundo según lo que cueste generar sucesores (tuplas son más lentas
    que enteros: codificar el estado como entero si hace falta velocidad).

EJEMPLO A MANO
    Jarras A = 3, B = 5, T = 4:
      (0,0) → (0,5) llenar B → (3,2) verter B en A → (0,2) vaciar A
      → (2,0) verter B en A → (2,5) llenar B → (3,4) verter B en A: 6 pasos.
    Only1s0s N = 4: restos: «1»→1; «10»→2, «11»→3; «100»→0 ⇒ M = 100.
    N = 13: M = 1001 (= 13·77).

ERRORES TÍPICOS
    - Estado incompleto: olvidar una componente que afecta el futuro
      (dirección, llaves, turno) → respuestas incorrectas.
    - Estado redundante: guardar el número completo en vez del resto →
      explosión de estados.
    - Usar listas como estado (no son hashables): convertir a tupla.
    - Marcar visitado al sacar en vez de al meter (estados repetidos en la cola).
    - Transiciones con costos distintos: ya no es BFS (bfs_01.py / dijkstra.py).

VARIANTES Y RELACIONADOS
    - Costos 0/1 entre estados: bfs_01.py; costos arbitrarios: dijkstra.py
      sobre estados.
    - BFS bidireccional (desde inicio y meta) para espacios muy grandes.
    - Búsqueda con máscara de bits como estado (llaves recogidas, visitados).
    - BFS en grafos explícitos: bfs.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/H - Only1s0s (BFS sobre restos módulo N)
    - ICPC/Colombia 2023/G - Grain Silos (búsqueda sobre configuraciones;
      allí con A* por el tamaño del espacio)
    - UVa 571 «Jugs», UVa 10603 «Fill» (jarras; en Fill se minimiza lo
      vertido → Dijkstra sobre estados)

VERIFICACIÓN
    - Pruebas: menor_multiplo_01 contra la enumeración en orden de 1, 10, 11,
      100, … para N = 1..400 (con tope de 2^16 candidatos; en los N donde la
      bruta no termina se valida múltiplo, solo 0/1 y que es mayor que todo
      lo enumerado). Jarras: contra un punto fijo por niveles (conjuntos de
      estados alcanzables en ≤ k pasos) para A, B ≤ 7, secuencias validadas
      operación por operación y existencia contra el criterio de Bézout
      (python bfs_estados.py)
"""
import math
from collections import deque


def bfs_estados(inicio, vecinos, es_meta):
    """Camino mínimo (lista de estados) de inicio a una meta; None si no hay."""
    padre = {inicio: None}            # también sirve de «visitado»
    cola = deque([inicio])
    while cola:
        e = cola.popleft()
        if es_meta(e):
            ruta = []
            while e is not None:
                ruta.append(e)
                e = padre[e]
            return ruta[::-1]
        for s in vecinos(e):
            if s not in padre:
                padre[s] = e
                cola.append(s)
    return None


def _operaciones_jarras(A, B):
    """Función de sucesores para el estado (a, b)."""
    def vecinos(e):
        a, b = e
        x = min(a, B - b)            # cuánto cabe al verter a en b
        y = min(b, A - a)            # cuánto cabe al verter b en a
        return [(A, b), (a, B), (0, b), (a, 0), (a - x, b + x), (a + y, b - y)]
    return vecinos


def jarras(A, B, T):
    """Secuencia mínima de estados (a, b) hasta tener T litros en alguna jarra."""
    return bfs_estados((0, 0), _operaciones_jarras(A, B), lambda e: T in e)


def menor_multiplo_01(N):
    """Menor M > 0 con solo dígitos 0/1 y M % N == 0 (BFS sobre restos)."""
    inicio = 1 % N                    # el número «1»
    padre = [-1] * N                  # resto anterior; -2 marca la raíz
    digito = [0] * N                  # dígito agregado para llegar a ese resto
    padre[inicio] = -2
    digito[inicio] = 1
    cola = deque([inicio])
    while cola:
        r = cola.popleft()
        if r == 0:
            break
        for d in (0, 1):              # 0 antes que 1: orden numérico dentro de la capa
            nr = (10 * r + d) % N
            if padre[nr] == -1:
                padre[nr] = r
                digito[nr] = d
                cola.append(nr)
    cifras = []
    r = 0                             # reconstruir desde el resto 0 hasta la raíz
    while r != -2:
        cifras.append(str(digito[r]))
        r = padre[r]
    return int("".join(reversed(cifras)))


def demo():
    ruta = jarras(3, 5, 4)
    print("jarras A=3, B=5, T=4:", len(ruta) - 1, "pasos:", ruta)
    print("jarras A=2, B=4, T=3:", jarras(2, 4, 3))          # None (mcd 2)
    for N in (4, 13, 7, 99):
        M = menor_multiplo_01(N)
        print(f"menor múltiplo 0/1 de {N}: {M} = {N}·{M // N}")


def pruebas():
    casos = 0

    # --- Only1s0s
    assert menor_multiplo_01(1) == 1
    assert menor_multiplo_01(4) == 100 and menor_multiplo_01(13) == 1001
    TOPE = 1 << 16
    for N in range(1, 401):
        M = menor_multiplo_01(N)
        assert M > 0 and M % N == 0 and set(str(M)) <= {"0", "1"}
        bruta = None
        for k in range(1, TOPE + 1):             # 1, 10, 11, 100, … en orden
            x = int(bin(k)[2:])
            if x % N == 0:
                bruta = x
                break
        if bruta is not None:
            assert M == bruta
        else:
            assert M > int(bin(TOPE)[2:])        # mayor que todo lo enumerado
        casos += 1

    # --- Jarras
    assert jarras(1, 1, 0) == [(0, 0)]
    assert jarras(3, 5, 4) is not None and len(jarras(3, 5, 4)) - 1 == 6
    for A in range(1, 8):
        for B in range(1, 8):
            vec = _operaciones_jarras(A, B)
            # Bruta: conjuntos de estados alcanzables en ≤ k pasos (punto fijo)
            nivel = {(0, 0)}
            primero = {}                         # T -> mínimo k en que aparece
            k = 0
            while True:
                for a, b in nivel:
                    for t in (a, b):
                        primero.setdefault(t, k)
                nuevo = nivel | {s for e in nivel for s in vec(e)}
                if nuevo == nivel:
                    break
                nivel = nuevo
                k += 1
            for T in range(0, max(A, B) + 2):
                ruta = jarras(A, B, T)
                posible = T <= max(A, B) and T % math.gcd(A, B) == 0
                assert (ruta is not None) == (T in primero) == posible
                if ruta is not None:
                    assert len(ruta) - 1 == primero[T]
                    assert ruta[0] == (0, 0) and T in ruta[-1]
                    assert all(ruta[i + 1] in vec(ruta[i]) for i in range(len(ruta) - 1))
                casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
