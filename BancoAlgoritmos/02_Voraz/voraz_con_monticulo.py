"""
Voraz — Voraz con montículo y «arrepentimiento» («Greedy with a heap / regret greedy»)
Nivel: Intermedio
Ejecutar: python voraz_con_monticulo.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Elegir el mejor subconjunto de tareas con PLAZOS recorriéndolas en
    orden y, cuando el conjunto deja de ser válido, «arrepentirse» sacando
    la PEOR tarea elegida hasta ahora (la tiene a mano un montículo).
    Dos problemas clásicos:
      1. Tareas de duración 1 con plazo d_i y ganancia g_i: maximizar la
         ganancia de las que se terminan a tiempo.
      2. Tareas de duración t_i con plazo d_i: maximizar CUÁNTAS se terminan
         a tiempo, es decir, minimizar las retrasadas (Moore–Hodgson).
    Señales: «plazo / fecha límite / deadline», «máximo de tareas a tiempo»,
    «presupuesto que no puede quedar negativo» recorriendo en orden,
    N hasta 2·10^5 (descarta la DP sobre tiempo).

FUNCIÓN
    tareas_con_plazo(tareas) -> (int, list[int])
        tareas: lista de (plazo, ganancia), duración 1, el tiempo empieza en
        0 y una tarea con plazo d debe ocupar una de las casillas 1..d.
        Devuelve la ganancia máxima y los índices elegidos.
    min_retrasos(tareas) -> (int, list[int])
        tareas: lista de (duracion, plazo). Devuelve el máximo número de
        tareas terminadas a tiempo (las demás se retrasan) y sus índices.
        Las elegidas se ejecutan en orden de plazo.

IDEA Y ALGORITMO
    Hecho base (orden por plazo, «EDD»): un conjunto de tareas se puede
    cumplir si y solo si ejecutándolas en orden de plazo creciente todas
    llegan a tiempo. (Si en un orden cualquiera hay dos consecutivas con
    plazos invertidos, intercambiarlas no retrasa a ninguna de las dos más
    allá del plazo mayor: argumento de intercambio.)
    Entonces se recorren las tareas por plazo y se mantiene el MEJOR
    conjunto válido del prefijo:
      1. Ganancias: se agrega la tarea; si ahora hay más tareas que el plazo
         actual (len > d), sobra exactamente una: se saca la de MENOR
         ganancia (montículo de mínimos). Invariante: el conjunto es el de
         mayor ganancia entre los válidos del prefijo (es un matroide: el
         voraz por peso es óptimo y el montículo lo implementa en orden de
         plazos).
      2. Retrasos: se agrega la tarea y se suma su duración; si el tiempo
         total supera el plazo actual, se saca la de MAYOR duración
         (montículo de máximos). Invariante: el conjunto tiene el máximo
         tamaño posible del prefijo y, entre esos, la menor duración total
         (deja más holgura para el futuro). Si no cupo, ningún conjunto del
         prefijo con un elemento más es válido, y cambiar la más larga por
         la nueva conserva el tamaño con duración total mínima.
    El ingenuo prueba los 2^N subconjuntos; la DP sobre el tiempo es
    O(N · max plazo), impracticable con plazos de 10^9.

MACROALGORITMO
    1. Ordenar índices por plazo creciente.
    2. Montículo vacío (mín por ganancia, o máx por duración vía negativos).
    3. Para cada tarea: meterla al montículo (y sumar su duración).
    4. Si el conjunto quedó inválido (len > plazo, o total > plazo),
       sacar la raíz del montículo (la peor) y descontarla.
    5. Al final, el montículo contiene las tareas elegidas.

COMPLEJIDAD
    O(N log N) tiempo, O(N) memoria. En Python, N = 2·10^5 en ~0,3 s.

EJEMPLO A MANO
    tareas_con_plazo: (plazo, ganancia) = (2,100) (1,19) (2,27) (1,25) (3,15)
    por plazo: (1,19) (1,25) (2,100) (2,27) (3,15)
      + 19        heap {19}             ok (1 <= 1)
      + 25        heap {19,25}          2 > 1 → sacar 19   → {25}
      + 100       heap {25,100}         ok (2 <= 2)
      + 27        heap {25,27,100}      3 > 2 → sacar 25   → {27,100}
      + 15        heap {15,27,100}      ok (3 <= 3)
      ganancia = 142.
    min_retrasos: (duración, plazo) = (2,3) (3,4) (1,5) (4,6)
      + (2,3): total 2 <= 3; + (3,4): total 5 > 4 → sacar dur 3, total 2;
      + (1,5): total 3 <= 5; + (4,6): total 7 > 6 → sacar dur 4, total 3.
      → 2 tareas a tiempo.

ERRORES TÍPICOS
    - Ordenar por ganancia y poner cada tarea en la última casilla libre
      antes de su plazo: es correcto pero O(N·d) o requiere DSU; con
      montículo es más simple.
    - En min_retrasos, sacar la tarea recién llegada en vez de la más larga
      (falla cuando una larga anterior bloquea varias cortas).
    - heapq es de MÍNIMOS: para máximos guardar -valor.
    - Plazos «antes de d» vs «a más tardar en d»: ajustar len > d por
      len >= d según el enunciado.

VARIANTES Y RELACIONADOS
    - Minimizar el MÁXIMO retraso: basta ordenar por plazo (EDD), sin
      montículo.
    - Con ganancias y duraciones arbitrarias es NP-difícil (mochila).
    - «Pociones» / presupuesto que no puede quedar negativo: mismo
      arrepentimiento, sacando el más caro.
    - 06_EstructurasDatos/monticulo_heapq.py, 02_Voraz/argumento_intercambio.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/G - Math United FC (voraz con montículo y
      arrepentimiento sobre un presupuesto)
    - Codeforces 1526C2 «Potions (Hard Version)».
    - LeetCode 630 «Course Schedule III» (= min_retrasos).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta en 1500 casos aleatorios por problema
      (N <= 9): DP sobre subconjuntos que decide si un conjunto es
      programable eligiendo cuál tarea va al final (sin usar el orden por
      plazo); validez de lo elegido y casos borde (python voraz_con_monticulo.py)
"""
import heapq
import random


def tareas_con_plazo(tareas):
    """Máxima ganancia con tareas de duración 1: (plazo, ganancia). -> (total, índices)."""
    orden = sorted(range(len(tareas)), key=lambda i: tareas[i][0])
    heap = []           # (ganancia, índice) de las elegidas; raíz = la de menor ganancia
    for i in orden:
        plazo, ganancia = tareas[i]
        heapq.heappush(heap, (ganancia, i))
        if len(heap) > plazo:       # no caben len tareas en las casillas 1..plazo
            heapq.heappop(heap)     # arrepentirse: soltar la menos valiosa
    return sum(g for g, _ in heap), sorted(i for _, i in heap)


def min_retrasos(tareas):
    """Moore–Hodgson: máximo de tareas (duracion, plazo) a tiempo. -> (cuántas, índices)."""
    orden = sorted(range(len(tareas)), key=lambda i: tareas[i][1])
    heap = []           # (-duración, índice): raíz = la tarea MÁS LARGA elegida
    total = 0           # tiempo en que termina la última elegida (en orden de plazo)
    for i in orden:
        dur, plazo = tareas[i]
        heapq.heappush(heap, (-dur, i))
        total += dur
        if total > plazo:           # la nueva llega tarde: sacar la más larga
            d, _ = heapq.heappop(heap)
            total += d              # d es negativo
    return len(heap), sorted(i for _, i in heap)


def demo():
    t1 = [(2, 100), (1, 19), (2, 27), (1, 25), (3, 15)]
    print("(plazo, ganancia) =", t1)
    print("tareas_con_plazo ->", tareas_con_plazo(t1))      # (142, [0, 2, 4])
    t2 = [(2, 3), (3, 4), (1, 5), (4, 6)]
    print("(duración, plazo) =", t2)
    print("min_retrasos     ->", min_retrasos(t2))          # (2, [0, 2])


def _programables(tareas, cabe):
    """factible[m]: el subconjunto m se puede ordenar cumpliendo plazos.

    cabe(m, j): ¿la tarea j puede ir al FINAL del conjunto m? (fuerza bruta
    sobre quién va último, sin asumir el orden por plazo).
    """
    n = len(tareas)
    factible = [False] * (1 << n)
    factible[0] = True
    for m in range(1, 1 << n):
        factible[m] = any(m >> j & 1 and factible[m ^ (1 << j)] and cabe(m, j)
                          for j in range(n))
    return factible


def _bruta_plazo(tareas):
    n = len(tareas)
    fac = _programables(tareas, lambda m, j: tareas[j][0] >= bin(m).count("1"))
    return max(sum(tareas[j][1] for j in range(n) if m >> j & 1)
               for m in range(1 << n) if fac[m])


def _bruta_retrasos(tareas):
    n = len(tareas)
    def suma(m):
        return sum(tareas[j][0] for j in range(n) if m >> j & 1)
    fac = _programables(tareas, lambda m, j: suma(m) <= tareas[j][1])
    return max(bin(m).count("1") for m in range(1 << n) if fac[m])


def _valido_edd(durs_plazos):
    t = 0
    for d, p in sorted(durs_plazos, key=lambda x: x[1]):
        t += d
        if t > p:
            return False
    return True


def pruebas():
    random.seed(5)

    # Casos borde
    assert tareas_con_plazo([]) == (0, []) and min_retrasos([]) == (0, [])
    assert tareas_con_plazo([(0, 50)]) == (0, [])          # plazo 0: imposible
    assert tareas_con_plazo([(1, 5)] * 4)[0] == 5          # todas iguales
    assert min_retrasos([(5, 4)]) == (0, [])
    assert min_retrasos([(1, 10)] * 4)[0] == 4
    # Una larga temprana bloquea a varias cortas: hay que sacar la larga
    assert min_retrasos([(10, 10), (3, 11), (3, 12), (3, 13)])[0] == 3

    for _ in range(1500):
        n = random.randint(0, 9)
        t1 = [(random.randint(0, 5), random.randint(0, 30)) for _ in range(n)]
        total, idx = tareas_con_plazo(t1)
        assert total == sum(t1[i][1] for i in idx)
        assert _valido_edd([(1, t1[i][0]) for i in idx])
        assert total == (_bruta_plazo(t1) if n else 0)

        t2 = [(random.randint(1, 6), random.randint(0, 15)) for _ in range(n)]
        k, idx = min_retrasos(t2)
        assert k == len(idx) and _valido_edd([t2[i] for i in idx])
        assert k == (_bruta_retrasos(t2) if n else 0)

    # Rendimiento: N = 2·10^5
    grande = [(random.randint(1, 10**9), random.randint(1, 10**9)) for _ in range(200000)]
    tareas_con_plazo(grande)
    min_retrasos(grande)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
