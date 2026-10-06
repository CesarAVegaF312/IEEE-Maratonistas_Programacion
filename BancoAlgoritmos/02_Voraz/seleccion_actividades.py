"""
Voraz — Selección de actividades («Activity selection / interval scheduling»)
Nivel: Básico
Ejecutar: python seleccion_actividades.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Dado un conjunto de intervalos [inicio, fin), elegir la MAYOR cantidad
    posible que no se solapen entre sí (una sola sala, un solo cine, una
    sola máquina).
    Señales en el enunciado: «máximo número de películas / charlas /
    reservas que se pueden atender», «sin que se crucen», un solo recurso,
    N hasta 10^5–10^6 (descarta cualquier DP cuadrática).

FUNCIÓN
    seleccion_actividades(intervalos) -> list[int]
        intervalos: lista de pares (inicio, fin) con inicio < fin, SEMIABIERTOS
        [inicio, fin): un intervalo que termina en 5 y otro que empieza en 5
        NO se solapan. Devuelve los ÍNDICES elegidos (en orden de fin); su
        cantidad es el máximo.
    Si el enunciado usa intervalos cerrados [a, b] (tocarse en un punto ya
    es choque), cambiar la condición `ini >= ultimo_fin` por `ini > ultimo_fin`.

IDEA Y ALGORITMO
    Regla voraz: ordenar por FIN creciente y tomar cada intervalo que empiece
    después (o justo cuando) termina el último tomado.
    Por qué es óptima (argumento «el voraz siempre va adelante»):
    sea g1, g2, …, gk lo que elige el voraz y o1, o2, …, om una solución
    óptima, ambas ordenadas por fin. Afirmación: fin(g_i) <= fin(o_i) para
    todo i <= k.
      - i = 1: g1 es el intervalo con menor fin de TODOS, así que
        fin(g1) <= fin(o1).
      - Paso: si fin(g_i) <= fin(o_i), entonces o_{i+1} empieza después de
        fin(o_i) >= fin(g_i); es decir, o_{i+1} era compatible con lo que el
        voraz llevaba, y el voraz eligió el compatible de menor fin, así que
        fin(g_{i+1}) <= fin(o_{i+1}).
    Si fuera m > k, o_{k+1} sería compatible con g_k (empieza después de
    fin(o_k) >= fin(g_k)) y el voraz lo habría tomado: contradicción. Luego
    k = m.
    Por qué otras reglas fallan: «el más corto primero» falla con
    [0,5) [4,6) [5,10) (toma [4,6) y bloquea los otros dos); «el que empieza
    primero» falla con [0,100) [1,2) [2,3).
    El ingenuo (probar todos los subconjuntos) es O(2^N); la DP con
    búsqueda binaria es O(N log N) pero solo hace falta si cada intervalo
    tiene PESO (ver variantes).

MACROALGORITMO
    1. Ordenar los índices por fin (desempate cualquiera).
    2. ultimo_fin = -infinito.
    3. Para cada intervalo en ese orden: si inicio >= ultimo_fin, tomarlo y
       hacer ultimo_fin = su fin.
    4. Devolver los tomados.

COMPLEJIDAD
    O(N log N) por el ordenamiento; el barrido es O(N). Memoria O(N).
    En Python, N = 10^6 en ~1 s (el sort con key está en C).

EJEMPLO A MANO
    intervalos = [(1,4) (3,5) (0,6) (5,7) (3,9) (5,9) (6,10) (8,11)]
    ordenados por fin: (1,4) (3,5) (0,6) (5,7) (3,9) (5,9) (6,10) (8,11)
      (1,4): 1 >= -inf  → tomar, ultimo_fin = 4
      (3,5): 3 < 4 no;  (0,6): no
      (5,7): 5 >= 4     → tomar, ultimo_fin = 7
      (3,9) (5,9) (6,10): empiezan antes de 7, no
      (8,11): 8 >= 7    → tomar.            Respuesta: 3 intervalos.

ERRORES TÍPICOS
    - Ordenar por inicio o por duración (ver contraejemplos arriba).
    - Confundir intervalos abiertos y cerrados: con [a, b] cerrados que se
      tocan en b hay que usar `>` en vez de `>=`.
    - Inicializar ultimo_fin en 0 cuando hay inicios negativos.
    - Usar este voraz cuando los intervalos tienen PESO: ahí se necesita DP
      (máximo peso de intervalos disjuntos) — el voraz da mal resultado.

VARIANTES Y RELACIONADOS
    - Intervalos con peso: DP dp[i] = max(dp[i-1], w_i + dp[p(i)]) con p(i)
      hallado por búsqueda binaria (ver 00_Base/busqueda_binaria.py).
    - K salas (máximo de intervalos con K recursos): ordenar por fin y
      asignar a la sala libre de fin más tardío (multiset).
    - Mínimo número de salas para TODOS los intervalos: barrido de eventos
      (máxima superposición).
    - El mínimo de puntos que tocan todos los intervalos usa el mismo orden
      por fin y da el mismo número (dualidad): ver 02_Voraz/intervalos.py.
    - Técnica general de prueba: 02_Voraz/argumento_intercambio.py.

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que usen exactamente esta técnica.)
    - CSES «Movie Festival»; CSES «Movie Festival II» (variante con K personas).
    - LeetCode 435 «Non-overlapping Intervals» (mínimo a borrar = N - máximo).

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todos los subconjuntos) en 1500 casos
      aleatorios con N <= 10, más validez de cada selección y casos borde
      (python seleccion_actividades.py)
"""
import random


def seleccion_actividades(intervalos):
    """Índices de un máximo conjunto de intervalos [ini, fin) disjuntos."""
    # Orden por fin: el que termina antes deja más espacio para el resto.
    orden = sorted(range(len(intervalos)), key=lambda i: intervalos[i][1])
    elegidos = []
    ultimo_fin = float("-inf")
    for i in orden:
        ini, fin = intervalos[i]
        if ini >= ultimo_fin:       # compatible con todo lo elegido (semiabiertos)
            elegidos.append(i)
            ultimo_fin = fin
    return elegidos


def demo():
    intervalos = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
    elegidos = seleccion_actividades(intervalos)
    print("intervalos =", intervalos)
    print("elegidos   =", [intervalos[i] for i in elegidos])   # (1,4) (5,7) (8,11)
    print("máximo     =", len(elegidos))                       # 3


def _disjuntos(lista):
    """Verdadero si los intervalos [a, b) de la lista no se solapan."""
    lista = sorted(lista)
    return all(lista[i][1] <= lista[i + 1][0] for i in range(len(lista) - 1))


def _fuerza_bruta(intervalos):
    n = len(intervalos)
    mejor = 0
    for mascara in range(1 << n):
        sub = [intervalos[i] for i in range(n) if mascara >> i & 1]
        if len(sub) > mejor and _disjuntos(sub):
            mejor = len(sub)
    return mejor


def pruebas():
    random.seed(2024)

    # Casos borde
    assert seleccion_actividades([]) == []
    assert seleccion_actividades([(3, 4)]) == [0]
    assert len(seleccion_actividades([(0, 5)] * 4)) == 1           # todos iguales
    assert len(seleccion_actividades([(0, 1), (1, 2), (2, 3)])) == 3  # se tocan: valen
    # Contraejemplos de otras reglas voraces
    assert len(seleccion_actividades([(0, 5), (4, 6), (5, 10)])) == 2
    assert len(seleccion_actividades([(0, 100), (1, 2), (2, 3)])) == 2
    assert len(seleccion_actividades([(-10, -5), (-5, 0)])) == 2   # inicios negativos

    # Aleatorios contra fuerza bruta
    for _ in range(1500):
        n = random.randint(0, 10)
        intervalos = []
        for _ in range(n):
            a = random.randint(-5, 15)
            intervalos.append((a, a + random.randint(1, 8)))
        elegidos = seleccion_actividades(intervalos)
        assert _disjuntos([intervalos[i] for i in elegidos])
        assert len(set(elegidos)) == len(elegidos)
        assert len(elegidos) == _fuerza_bruta(intervalos)

    # Rendimiento: N = 2·10^5
    grande = [(a, a + random.randint(1, 1000)) for a in
              (random.randint(0, 10**6) for _ in range(200000))]
    assert len(seleccion_actividades(grande)) > 0


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
