"""
Voraz — Problemas clásicos de intervalos («Merge intervals, interval stabbing, interval covering»)
Nivel: Intermedio
Ejecutar: python intervalos.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Tres problemas de intervalos CERRADOS [a, b] que salen muchísimo y se
    resuelven ordenando y barriendo una vez:
      1. Unir intervalos: la unión como lista de intervalos disjuntos
         («tramos de carretera pintados», «horas ocupadas en total»).
      2. Mínimo de puntos que tocan todos los intervalos («mínimo de
         flechas para reventar globos», «mínimo de visitas/radares para
         atender a todos»).
      3. Cubrir el segmento [L, R] con el mínimo de intervalos («mínimo de
         aspersores/guardias para cubrir el campo»).
    Señales: N intervalos hasta 10^5–10^6, «mínimo de…», «unión», «cubrir».

FUNCIÓN
    unir_intervalos(intervalos) -> list[(a, b)]
        Unión ordenada; dos intervalos que se TOCAN ([1,3] y [3,5]) se unen.
    minimo_puntos(intervalos) -> list[x]
        Conjunto mínimo de puntos tal que cada intervalo contiene alguno.
    cubrir_segmento(intervalos, L, R) -> int
        Mínimo de intervalos cuya unión contiene [L, R]; -1 si es imposible.

IDEA Y ALGORITMO
    1. Unir: ordenar por inicio. El intervalo actual [a, b] absorbe al
       siguiente [c, d] si c <= b (se solapan o se tocan): b = max(b, d).
       Si c > b, entre b y c hay un hueco que ningún intervalo posterior
       puede llenar (todos empiezan en >= c), así que [a, b] queda cerrado.
    2. Puntos: ordenar por FIN. Al primer intervalo sin pinchar hay que
       ponerle un punto en algún lugar de [a, b]; ponerlo lo más a la
       DERECHA posible (en b) pincha todo lo que cualquier otra elección
       pincharía entre los que quedan: todos los intervalos restantes
       terminan en >= b, así que si contienen algún x <= b también
       contienen b. Repetir con el siguiente intervalo no pinchado.
       Además: el número mínimo de puntos es IGUAL al máximo de intervalos
       disjuntos (02_Voraz/seleccion_actividades.py): cada punto pincha a lo
       sumo uno de un conjunto disjunto, y el voraz coloca exactamente un
       punto por intervalo de un conjunto disjunto.
    3. Cubrir [L, R]: ordenar por inicio. Mantener cubierto = el punto
       hasta donde ya está cubierto [L, cubierto]. Entre todos los
       intervalos que empiezan en <= cubierto (los que pueden «empalmar»),
       elegir el que llega más LEJOS. Es correcto porque cualquier
       solución tiene que usar alguno de esos para seguir y el que llega
       más lejos deja un subproblema que contiene al de cualquier otro.
       Si ninguno avanza, hay un hueco: -1.

MACROALGORITMO
    Unir:   ordenar por inicio; para cada [c, d]: si c <= b_actual,
            b_actual = max(b_actual, d); si no, cerrar y abrir uno nuevo.
    Puntos: ordenar por fin; ultimo = -inf; para cada [a, b]: si a > ultimo
            (no está pinchado), poner punto en b y ultimo = b.
    Cubrir: ordenar por inicio; cubierto = L; repetir:
            1. de los intervalos con inicio <= cubierto, tomar el mayor fin;
            2. si no hay o no avanza, -1;
            3. contar uno, cubierto = ese fin; si cubierto >= R, terminar.

COMPLEJIDAD
    Los tres: O(N log N) por el ordenamiento y O(N) el barrido (en cubrir,
    cada intervalo se mira una sola vez). Memoria O(N).
    En Python, N = 10^6 en ~1–2 s.

EJEMPLO A MANO
    intervalos = [1,3] [2,6] [8,10] [10,12] [15,18]
      unir:   [1,3]+[2,6] → [1,6]; [8,10]+[10,12] → [8,12]; [15,18]
      puntos (por fin): [1,3] → punto 3; [2,6] ya tiene 3;
              [8,10] → punto 10; [10,12] ya tiene 10; [15,18] → punto 18
              → 3 puntos {3, 10, 18}
    cubrir [0, 10] con [0,3] [2,6] [3,4] [5,10] [6,9]:
      cubierto 0: empiezan <= 0 → [0,3]          → cubierto 3 (1)
      cubierto 3: [2,6] [3,4] → mayor fin 6      → cubierto 6 (2)
      cubierto 6: [5,10] [6,9] → mayor fin 10    → cubierto 10 (3) → 3.

ERRORES TÍPICOS
    - Mezclar convenciones: con [a, b) semiabiertos, [1,3) y [3,5) no se
      solapan pero SÍ se unen en la unión; con puntos enteros a veces se
      unen [1,3] y [4,5] (c <= b + 1). Leer bien el enunciado.
    - En puntos, ordenar por inicio en vez de por fin (falla con un
      intervalo largo que contiene a otros cortos).
    - En cubrir, olvidar el caso «no avanza» (ciclo infinito) o no revisar
      que el primer intervalo empiece en <= L.
    - Cubrir con intervalos de puntos ENTEROS (casillas): ahí basta que el
      siguiente empiece en <= cubierto + 1, no en <= cubierto.

VARIANTES Y RELACIONADOS
    - Longitud total de la unión: sumar b - a de los intervalos unidos.
    - Máxima superposición / mínimo de salas: barrido de eventos (+1 al
      inicio, -1 al fin).
    - Cubrir un círculo: fijar el intervalo inicial y desenrollar, o
      duplicar el arreglo.
    - 02_Voraz/seleccion_actividades.py (máximo de disjuntos, el dual de
      minimo_puntos).

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que usen exactamente estas técnicas.)
    - UVa 10020 «Minimal coverage» (cubrir un segmento).
    - LeetCode 56 «Merge Intervals»; LeetCode 452 «Minimum Number of Arrows
      to Burst Balloons» (mínimo de puntos).

VERIFICACIÓN
    - Pruebas (python intervalos.py): en 600 casos aleatorios con extremos
      enteros pequeños, contra fuerzas brutas independientes:
      unir y cubrir marcando los puntos enteros y medios (coordenadas
      duplicadas) que quedan cubiertos; minimo_puntos probando conjuntos de
      puntos enteros de tamaño creciente, y comparando con el máximo de
      intervalos disjuntos (dualidad). Más casos borde.
"""
import random
from itertools import combinations


def unir_intervalos(intervalos):
    """Unión de intervalos cerrados como lista ordenada de intervalos disjuntos."""
    res = []
    for a, b in sorted(intervalos):
        if res and a <= res[-1][1]:             # se solapa o toca al último: extenderlo
            if b > res[-1][1]:
                res[-1][1] = b
        else:                                   # hay hueco: nuevo intervalo
            res.append([a, b])
    return [tuple(x) for x in res]


def minimo_puntos(intervalos):
    """Mínimo conjunto de puntos que pincha todos los intervalos cerrados."""
    puntos = []
    ultimo = float("-inf")
    for a, b in sorted(intervalos, key=lambda x: x[1]):
        if a > ultimo:          # aún no pinchado: el punto más a la derecha posible
            ultimo = b
            puntos.append(b)
    return puntos


def cubrir_segmento(intervalos, L, R):
    """Mínimo de intervalos cerrados cuya unión contiene [L, R]; -1 si no se puede."""
    iv = sorted(intervalos)
    n, i = len(iv), 0
    cubierto, usados = L, 0     # invariante: [L, cubierto] ya está cubierto
    while True:
        mejor = None
        # Candidatos: los que empiezan dentro de lo ya cubierto (pueden empalmar).
        while i < n and iv[i][0] <= cubierto:
            if mejor is None or iv[i][1] > mejor:
                mejor = iv[i][1]
            i += 1
        if mejor is None or mejor < cubierto or (usados and mejor == cubierto):
            return -1           # hueco: nadie empalma o nadie avanza
        usados += 1
        cubierto = mejor
        if cubierto >= R:
            return usados


def demo():
    iv = [(1, 3), (2, 6), (8, 10), (10, 12), (15, 18)]
    print("intervalos     =", iv)
    print("unión          =", unir_intervalos(iv))        # [(1,6), (8,12), (15,18)]
    print("mínimo puntos  =", minimo_puntos(iv))          # [3, 10, 18]
    cub = [(0, 3), (2, 6), (3, 4), (5, 10), (6, 9)]
    print("cubrir [0,10] con", cub, "->", cubrir_segmento(cub, 0, 10))   # 3


# ---------------- Fuerzas brutas (coordenadas duplicadas: enteros y medios) ----

def _cubiertos2(intervalos):
    """Conjunto de puntos 2x (x entero o medio) cubiertos por algún intervalo."""
    s = set()
    for a, b in intervalos:
        s.update(range(2 * a, 2 * b + 1))
    return s


def _unir_bruta(intervalos):
    s = sorted(_cubiertos2(intervalos))
    res = []
    for p in s:                 # tramos maximales de puntos 2x consecutivos
        if res and p == res[-1][1] + 1:
            res[-1][1] = p
        else:
            res.append([p, p])
    return [(a // 2, b // 2) for a, b in res]


def _cubrir_bruta(intervalos, L, R):
    necesarios = set(range(2 * L, 2 * R + 1))
    for k in range(1, len(intervalos) + 1):
        for sub in combinations(intervalos, k):
            if necesarios <= _cubiertos2(sub):
                return k
    return -1


def _puntos_bruta(intervalos):
    if not intervalos:
        return 0
    lo = min(a for a, b in intervalos)
    hi = max(b for a, b in intervalos)
    for k in range(1, len(intervalos) + 1):
        for pts in combinations(range(lo, hi + 1), k):
            if all(any(a <= p <= b for p in pts) for a, b in intervalos):
                return k


def _max_disjuntos_cerrados(intervalos):
    n, mejor = len(intervalos), 0
    for m in range(1 << n):
        sub = sorted(intervalos[i] for i in range(n) if m >> i & 1)
        if all(sub[i][1] < sub[i + 1][0] for i in range(len(sub) - 1)):
            mejor = max(mejor, len(sub))
    return mejor


def pruebas():
    random.seed(31)

    # Casos borde
    assert unir_intervalos([]) == [] and minimo_puntos([]) == []
    assert cubrir_segmento([], 0, 5) == -1
    assert unir_intervalos([(1, 3), (3, 5)]) == [(1, 5)]           # se tocan: se unen
    assert unir_intervalos([(1, 2), (3, 4)]) == [(1, 2), (3, 4)]
    assert unir_intervalos([(1, 10), (2, 3)]) == [(1, 10)]          # contenido
    assert minimo_puntos([(0, 10), (1, 2), (8, 9)]) == [2, 9]
    assert cubrir_segmento([(2, 2)], 2, 2) == 1                     # segmento de un punto
    assert cubrir_segmento([(0, 4), (5, 9)], 0, 9) == -1            # hueco (4, 5)
    assert cubrir_segmento([(1, 9)], 0, 5) == -1                    # no llega a L
    assert cubrir_segmento([(0, 3), (3, 3), (3, 7)], 0, 7) == 2
    assert cubrir_segmento([(0, 3), (3, 3)], 0, 7) == -1            # no avanza

    for _ in range(600):
        n = random.randint(0, 7)
        iv = []
        for _ in range(n):
            a = random.randint(0, 12)
            iv.append((a, a + random.randint(0, 5)))
        assert unir_intervalos(iv) == _unir_bruta(iv)
        pts = minimo_puntos(iv)
        assert all(any(a <= p <= b for p in pts) for a, b in iv)   # pincha a todos
        assert len(pts) == _puntos_bruta(iv) == _max_disjuntos_cerrados(iv)
        L = random.randint(0, 10)
        R = L + random.randint(0, 6)
        assert cubrir_segmento(iv, L, R) == _cubrir_bruta(iv, L, R)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
