"""
Voraz — Cruzar el puente de noche («Bridge and torch problem»)
Nivel: Intermedio
Ejecutar: python bridge_and_torch.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    N personas deben cruzar un puente de noche. Cruzan como máximo DOS a la
    vez, hay UNA sola lámpara (alguien tiene que devolverla) y una pareja
    camina al ritmo del más lento. Minimizar el tiempo total.
    Señales en el enunciado: «puente / río / túnel», «a lo sumo dos a la
    vez», «una linterna / antorcha / lámpara», «van a la velocidad del más
    lento». Aparece tal cual en competencias (ICPC Colombia 2024 B, UVa
    10037) y también disfrazado (balsa, ascensor con llave…).

FUNCIÓN
    tiempo_puente(tiempos) -> int
        tiempos: lista de tiempos individuales (>= 0). Devuelve el tiempo
        mínimo para que todos crucen (0 si no hay nadie).
    plan_puente(tiempos) -> list[tuple]
        Una secuencia óptima de movimientos: ('va', a, b) o ('va', a) hacia
        el otro lado y ('vuelve', a) con la lámpara; a, b son tiempos.

IDEA Y ALGORITMO
    Ordenar t1 <= t2 <= … <= tn. Mientras queden más de 3 personas, mandar
    al otro lado a las DOS MÁS LENTAS (t_{n-1}, t_n) y devolver la lámpara;
    solo hay dos formas que valen la pena:
      (a) los dos más rápidos escoltan:
          t1,t2 van (t2); t1 vuelve (t1); t_{n-1},t_n van (t_n); t2 vuelve (t2)
          costo = t1 + 2·t2 + t_n
      (b) el más rápido acompaña a cada uno:
          t1,t_n van (t_n); t1 vuelve (t1); t1,t_{n-1} van (t_{n-1}); t1 vuelve (t1)
          costo = 2·t1 + t_{n-1} + t_n
    Se suma el mínimo de las dos y el problema queda igual con n-2 personas
    (t1 y t2 siguen en el lado inicial con la lámpara). Casos base:
    n = 1 → t1;  n = 2 → t2;  n = 3 → t1 + t2 + t3 (t1 acompaña a los otros).
    (a) conviene si 2·t2 < t1 + t_{n-1}: cuando hay dos lentos parecidos,
    pagar el lento una sola vez compensa el viaje extra de t2.
    Por qué es óptimo (Rote, 2002): en una solución óptima los dos más
    lentos o cruzan JUNTOS (y entonces lo mejor es que la lámpara la traigan
    y la devuelvan los dos más rápidos: estrategia a) o cruzan por
    SEPARADO, cada uno pagando su propio viaje (y lo más barato es que los
    acompañe y vuelva el más rápido: estrategia b); un argumento de
    intercambio muestra que cualquier otra combinación no es mejor.
    El ingenuo (Dijkstra/BFS sobre los 2^N · 2 estados «quién está de cada
    lado + dónde está la lámpara») solo sirve para N <= ~15; el voraz es
    O(N log N).

MACROALGORITMO
    1. Ordenar los tiempos.
    2. total = 0; n = número de personas.
    3. Mientras n > 3: total += min(t1 + 2·t2 + t_n, 2·t1 + t_{n-1} + t_n);
       n -= 2.
    4. Sumar el caso base de n ∈ {0, 1, 2, 3}.
    5. Devolver total.

COMPLEJIDAD
    O(N log N) por el ordenamiento; el ciclo es O(N). Memoria O(N).
    Instantáneo para cualquier N razonable.

EJEMPLO A MANO
    tiempos 1, 2, 5, 10:
      n = 4: (a) 1 + 2·2 + 10 = 15;  (b) 2·1 + 5 + 10 = 17 → 15, n = 2
      n = 2: + t2 = 2                              → total 17.
    Plan: 1,2 van (2); 1 vuelve (1); 5,10 van (10); 2 vuelve (2); 1,2 van (2).
    tiempos 1, 2, 5 (ejemplo de Colombia 2024 B): n = 3 → 1 + 2 + 5 = 8.

ERRORES TÍPICOS
    - Usar siempre la estrategia (b) («el más rápido acompaña a todos»):
      con 1, 2, 5, 10 da 19 en vez de 17.
    - Usar siempre la (a): con 1, 20, 21, 22 da (1+2·20+22) + 20 = 83
      contra 65 de la (b).
    - Olvidar n = 0 (si el enunciado lo permite) o tratar n = 3 con la
      fórmula general (daría índices negativos).
    - No ordenar los tiempos antes.

VARIANTES Y RELACIONADOS
    - Capacidad del puente mayor que 2: el voraz deja de ser tan simple
      (hay DP específicas); con N pequeño, Dijkstra sobre estados.
    - 02_Voraz/argumento_intercambio.py (técnica de la demostración).

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/B - The Bridge at Night
    - UVa 10037 «Bridge» (pide además imprimir los movimientos: plan_puente).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (Dijkstra sobre todos los estados
      «subconjunto en la otra orilla + lado de la lámpara» con todos los
      movimientos de 1 o 2 personas) en 600 casos aleatorios con N <= 7;
      el plan se simula y se comprueba que es válido y suma lo mismo
      (python bridge_and_torch.py)
"""
import heapq
import random


def tiempo_puente(tiempos):
    """Tiempo mínimo para que todos crucen (de a dos, una lámpara)."""
    t = sorted(tiempos)
    n = len(t)
    total = 0
    while n > 3:
        # Llevar a los dos más lentos t[n-2], t[n-1] y dejar la lámpara de vuelta.
        escoltas = t[0] + 2 * t[1] + t[n - 1]           # (a) cruzan juntos
        acompanados = 2 * t[0] + t[n - 2] + t[n - 1]    # (b) cada uno con t[0]
        total += min(escoltas, acompanados)
        n -= 2
    if n == 3:
        total += t[0] + t[1] + t[2]
    elif n == 2:
        total += t[1]
    elif n == 1:
        total += t[0]
    return total


def plan_puente(tiempos):
    """Movimientos de una solución óptima: ('va', a[, b]) y ('vuelve', a)."""
    t = sorted(tiempos)
    n = len(t)
    plan = []
    while n > 3:
        a, b, y, z = t[0], t[1], t[n - 2], t[n - 1]
        if a + 2 * b + z <= 2 * a + y + z:
            plan += [("va", a, b), ("vuelve", a), ("va", y, z), ("vuelve", b)]
        else:
            plan += [("va", a, z), ("vuelve", a), ("va", a, y), ("vuelve", a)]
        n -= 2
    if n == 3:
        plan += [("va", t[0], t[2]), ("vuelve", t[0]), ("va", t[0], t[1])]
    elif n == 2:
        plan += [("va", t[0], t[1])]
    elif n == 1:
        plan += [("va", t[0])]
    return plan


def demo():
    for tiempos in ([1, 2, 5, 10], [1, 2, 5], [1, 20, 21, 22]):
        print("tiempos", tiempos, "-> mínimo", tiempo_puente(tiempos))   # 17, 8, 65
    print("plan para [1, 2, 5, 10]:", plan_puente([1, 2, 5, 10]))


def _dijkstra(tiempos):
    """Fuerza bruta: estado (máscara de los que ya cruzaron, lámpara al otro lado?)."""
    n = len(tiempos)
    if n == 0:
        return 0
    todos = (1 << n) - 1
    dist = {(0, 0): 0}
    pq = [(0, 0, 0)]
    while pq:
        d, m, lado = heapq.heappop(pq)
        if d > dist[(m, lado)]:
            continue
        if m == todos:
            return d
        # Quienes están con la lámpara pueden moverse (1 o 2 de ellos).
        aqui = [i for i in range(n) if (m >> i & 1) == lado]
        grupos = [(i,) for i in aqui] + [(i, j) for k, i in enumerate(aqui) for j in aqui[k + 1:]]
        for g in grupos:
            nm = m
            for i in g:
                nm ^= 1 << i
            nd = d + max(tiempos[i] for i in g)
            if nd < dist.get((nm, 1 - lado), float("inf")):
                dist[(nm, 1 - lado)] = nd
                heapq.heappush(pq, (nd, nm, 1 - lado))


def _simular(tiempos, plan):
    """Valida el plan (reglas del puente) y devuelve su tiempo total."""
    inicio, otro = sorted(tiempos), []
    lampara_inicio, total = True, 0
    for mov in plan:
        tipo, quienes = mov[0], list(mov[1:])
        assert 1 <= len(quienes) <= 2
        origen, destino = (inicio, otro) if tipo == "va" else (otro, inicio)
        assert (tipo == "va") == lampara_inicio      # la lámpara viaja con ellos
        for q in quienes:
            origen.remove(q)                          # falla si no está de ese lado
            destino.append(q)
        lampara_inicio = not lampara_inicio
        total += max(quienes)
    assert not inicio
    return total


def pruebas():
    random.seed(2024)

    # Casos borde y conocidos
    assert tiempo_puente([]) == 0 and plan_puente([]) == []
    assert tiempo_puente([7]) == 7
    assert tiempo_puente([3, 9]) == 9
    assert tiempo_puente([1, 2, 5]) == 8
    assert tiempo_puente([1, 2, 5, 10]) == 17
    assert tiempo_puente([1, 20, 21, 22]) == 65
    assert tiempo_puente([4, 4, 4, 4, 4]) == 4 * 7       # todos iguales: 2n-3 viajes

    for _ in range(600):
        n = random.randint(0, 7)
        tiempos = [random.randint(1, 20) for _ in range(n)]
        r = tiempo_puente(tiempos)
        assert r == _dijkstra(tiempos)
        assert _simular(tiempos, plan_puente(tiempos)) == r


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
