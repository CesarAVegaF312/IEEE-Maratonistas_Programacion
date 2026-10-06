"""
Colombia 2026 — I: Fair Workload Distribution («Distribución justa de la carga de trabajo»)
Ejecutar: python fairworkload.py < fairworkload.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    ByteCorp tiene N trabajadores en círculo (1..N). Cada día i llegan M_i
    tareas y se reparten en ronda (round-robin) empezando por el trabajador
    k_i: k_i, k_i+1, ..., N, 1, 2, ... hasta acabar las tareas. La gerencia
    quiere saber cuántas tareas acumuló un trabajador hasta cierto día.

QUÉ HAY QUE HACER
    Entrada: varios casos. Cada uno: "N D Q", luego D líneas "k_i M_i" y Q
             líneas "d w". Termina con "0 0 0".
    Salida:  por cada consulta, el total de tareas del trabajador w en los
             días 1..d (una línea por consulta).
    Restricciones clave: N <= 10^9 (no se puede tener un arreglo por
             trabajador), M_i <= 10^9 (no se puede simular tarea por tarea),
             suma de D <= 5·10^5 y suma de Q <= 5·10^5 sobre todos los casos.

IDEA Y ALGORITMO
    1) Un día por dentro. Con q, r = divmod(M_i, N): se dan q vueltas
       completas (todos reciben q) y sobran r < N tareas que van, una a cada
       uno, a los r trabajadores del intervalo CIRCULAR que empieza en k_i.

    2) Ese intervalo circular como "escalones". Sea p_i = ((k_i - 1 + r) mod N) + 1
       (el trabajador que recibiría la siguiente tarea) y
       c_i = 1 si el intervalo da la vuelta (k_i - 1 + r >= N), si no 0.
       Entonces, para todo trabajador w:
           extra_i(w) = [w >= k_i] - [w >= p_i] + c_i          (si r > 0)
       - Sin vuelta: p_i = k_i + r y la resta de escalones es justo [k_i, k_i+r-1].
       - Con vuelta: el intervalo es "todos menos [p_i, k_i - 1]", que es
         1 - [w >= p_i] + [w >= k_i]  (p_i <= k_i - 1 porque r < N).
       (El caso k_i - 1 + r == N cae en "vuelta" con p_i = 1: -[w>=1] + 1 = 0,
       así que también da el resultado correcto.)

    3) Respuesta a (d, w):
           sum_{i<=d} (q_i + c_i)                       -> prefijo simple
         + #{ i <= d : k_i <= w }  -  #{ i <= d : p_i <= w }
       Las dos cuentas son "conteos de dominancia" en 2D (día <= d y
       posición <= w). Se resuelven OFFLINE: se procesan los días en orden y
       se responden las consultas de cada día justo después de agregarlo, con
       un árbol de Fenwick (BIT) indexado por posición de trabajador.

    4) Compresión de coordenadas. N es enorme, pero solo importan los
       trabajadores que aparecen en consultas (ws ordenados). Un escalón
       "+1 para todo w >= k" afecta exactamente a los ws con índice >=
       bisect_left(ws, k): se suma +1 en esa posición del BIT y la consulta
       del trabajador w es la suma de prefijo hasta su índice.

    Por qué no lo ingenuo: simular cuesta O(M) por día y un arreglo por
    trabajador O(N); ambos imposibles con 10^9. Recorrer todos los días por
    consulta es O(D·Q) = 2.5·10^11.

MACROALGORITMO
    1. Leer el caso: días (k_i, M_i) y consultas (d, w, posición original).
    2. Comprimir los trabajadores consultados: ws ordenados, w -> índice.
    3. Para cada día i: q, r = divmod(M_i, N); acumular q (+1 si da la vuelta)
       en "base"; si r > 0, sumar +1 en el BIT en bisect_left(ws, k_i) y -1
       en bisect_left(ws, p_i).
    4. Tras procesar el día i, responder las consultas con d = i:
       base + prefijo_BIT(índice de w).
    5. Reordenar las respuestas al orden de entrada e imprimir.

COMPLEJIDAD
    Tiempo O((D + Q) log Q) por caso, memoria O(D + Q).
    Caso grande (un caso con D = Q = 5·10^5, N = 10^9, ~5·10^5 trabajadores
    distintos consultados): ~6 s en esta máquina (≈1 M actualizaciones y
    5·10^5 consultas al BIT en Python puro). Es el peor caso permitido y
    Python puede quedar justo frente al límite del juez. Con N = 1000
    (pocos trabajadores distintos) baja a ~2.6 s. La versión original del
    usuario (fairworkload.py en la raíz) tarda ~18 s en el mismo caso
    grande: llamaba funciones anidadas por cada actualización y hacía dos
    sumas de rango por día que da la vuelta; aquí cada día son exactamente
    dos actualizaciones en línea gracias a la fórmula de escalones.

EJEMPLO A MANO
    N=5. Día 1: k=2, M=7 -> q=1, r=2, extra a {2,3}. Día 2: k=4, M=3 -> q=0,
    r=3, extra a {4,5,1} (da la vuelta: p=2, c=1: 1 - [w>=2] + [w>=4]).
    Día 3: k=1, M=10 -> q=2, r=0.
    (d=2, w=4): base = 1 + 0 + 1(vuelta) = 2;  [4>=2]-[4>=4] + [4>=4]-[4>=2]
    = 0  -> 2.   (d=3, w=5): base = 1+1+2 = 4; escalones: 1-1+1-1 = 0 -> 4.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2026/I")
    - Fuerza bruta: OK en 600 entradas aleatorias (≈18 000 consultas, N <= 8,
      M hasta 30 para forzar varias vueltas) contra una simulación que
      reparte las tareas una por una.
    - Coincide con fairworkload.py del usuario en los casos grandes.
"""
import sys
from bisect import bisect_left


def resolver_caso(n, dias, consultas):
    """dias: lista de (k, M). consultas: lista de (d, w). Devuelve respuestas
    en el orden de las consultas."""
    # --- Compresión: trabajadores que aparecen en alguna consulta ----------
    ws = sorted(set(w for _, w in consultas))
    m = len(ws)
    indice = {w: i + 1 for i, w in enumerate(ws)}   # índice 1-based en el BIT

    # Consultas agrupadas por día: por_dia[d] = [(índice_bit, posición), ...]
    por_dia = [[] for _ in range(len(dias) + 1)]
    for pos, (d, w) in enumerate(consultas):
        por_dia[d].append((indice[w], pos))

    bit = [0] * (m + 1)       # Fenwick: bit[i] guarda sumas de "escalones"
    respuestas = [0] * len(consultas)
    base = 0                  # suma de q_i + c_i de los días ya procesados

    for dia, (k, tareas) in enumerate(dias, start=1):
        vueltas, sobran = divmod(tareas, n)
        base += vueltas
        if sobran:
            fin = k - 1 + sobran                  # 0-based: último índice +1
            if fin >= n:
                base += 1                          # c_i: el intervalo da la vuelta
            p = fin % n + 1                        # primer trabajador SIN extra
            # Escalón +1 en k: afecta a los ws >= k (índice 1-based j).
            j = bisect_left(ws, k) + 1
            while j <= m:
                bit[j] += 1
                j += j & -j
            # Escalón -1 en p: afecta a los ws >= p.
            j = bisect_left(ws, p) + 1
            while j <= m:
                bit[j] -= 1
                j += j & -j

        # Consultas cuyo día límite es este: suma de prefijo del BIT.
        for j, pos in por_dia[dia]:
            s = base
            while j:
                s += bit[j]
                j &= j - 1                         # quita el bit más bajo
            respuestas[pos] = s
    return respuestas


def main():
    datos = sys.stdin.buffer.read().split()
    idx, salida = 0, []
    while idx + 2 < len(datos):
        n, d, q = int(datos[idx]), int(datos[idx + 1]), int(datos[idx + 2])
        idx += 3
        if n == 0 and d == 0 and q == 0:          # fin de la entrada
            break
        valores = list(map(int, datos[idx: idx + 2 * d]))
        idx += 2 * d
        dias = list(zip(valores[0::2], valores[1::2]))        # (k_i, M_i)
        valores = list(map(int, datos[idx: idx + 2 * q]))
        idx += 2 * q
        consultas = list(zip(valores[0::2], valores[1::2]))   # (d, w)
        salida.extend(resolver_caso(n, dias, consultas))
    sys.stdout.write("\n".join(map(str, salida)) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
