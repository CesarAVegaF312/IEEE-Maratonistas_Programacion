"""
ACM ICPC Guangzhou Summer Series 2017 — H: Half the Polygon («La mitad del polígono»)
Ejecutar: python halfpolygon.py < halfpolygon.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Tenemos un polígono ortogonal simple (todas sus aristas horizontales o
    verticales, ángulos de 90° o 270°) con vértices enteros. Queremos saber
    si un corte recto horizontal o vertical, con extremos enteros, lo parte
    en dos polígonos IDÉNTICOS (congruentes: iguales salvo rotación,
    reflexión y traslación).

QUÉ HAY QUE HACER
    Entrada: hasta fin de archivo, casos (≤ 50): una línea con n y luego n
             líneas "x y" con los vértices en orden. [El enunciado dice "dos
             enteros n" pero solo hay uno, como muestra el ejemplo.]
    Salida:  "Yes" si existe el corte, "No" si no.
    Restricciones clave: 4 ≤ n ≤ 10^5, 0 ≤ x, y ≤ 10^9.
    Interpretación del corte: un segmento horizontal o vertical cuyos dos
    extremos (enteros) están en el borde y cuyo interior abierto está dentro
    del polígono (una "cuerda"); así el polígono queda partido en dos.

IDEA Y ALGORITMO
    Condiciones necesarias muy fuertes + verificación exacta de congruencia.
    * Perímetro: si las piezas P1, P2 son congruentes tienen igual perímetro.
      perímetro(Pk) = (camino del borde que le toca) + |cuerda|, así que los
      dos caminos del borde miden lo mismo: L/2 cada uno (L = perímetro
      total). Los extremos p, q de la cuerda son ANTÍPODAS en longitud de
      arco: si p está en la posición t, q está en t + L/2.
      (L es par en un polígono ortogonal: las aristas horizontales suman
      ida y vuelta lo mismo, igual las verticales.)
    * Parametrizamos t ∈ [0, L/2). Los vértices cortan ese rango en O(n)
      intervalos en los que p y q recorren una arista fija cada uno, es
      decir, p(t) y q(t) son lineales en t. En cada intervalo:
        - la cuerda es vertical si p.x = q.x: ecuación lineal en t → a lo
          más una raíz (o el intervalo entero si la diferencia es constante
          0); igual para horizontal con p.y = q.y;
        - si es el intervalo entero, la cuerda se desplaza paralela a sí
          misma y el área de un lado cambia linealmente: la condición
          "área = mitad" da a lo más un t.
      Además probamos cada extremo de intervalo (p o q en un vértice).
      Solo sirven t enteros (los extremos deben ser enteros, y un punto a
      distancia entera de un vértice entero es entero y viceversa).
    * Área de la pieza P1 en O(1) con sumas prefijas de la fórmula del
      zapato (shoelace): 2·área = cruz(p, V_a) + Σ cruz(V_k, V_k+1) +
      cruz(V_b, q) + cruz(q, p). Exigimos 2·área(P1) = área(P) (exacto).
    * Validez de la cuerda: (ya, yb) debe ser una componente conexa de
      "recta ∩ interior del polígono". Para una recta x = c la calculamos
      una vez (y la guardamos): el punto (c, y) es interior si y solo si
      (c-ε, y) y (c+ε, y) están dentro; cada uno se obtiene de las aristas
      horizontales que cruzan x = c-ε (x_min < c ≤ x_max) o x = c+ε
      (x_min ≤ c < x_max), ordenadas por y (paridad de cruces).
    * Dos cuerdas disjuntas no pueden ambas partir el área por la mitad (una
      pieza de la segunda quedaría estrictamente dentro de una mitad de la
      primera). Las cuerdas verticales de rectas distintas, o de la misma
      recta, son disjuntas, así que hay A LO MÁS una cuerda vertical válida
      que parte el área a la mitad y otra horizontal: la prueba cara de
      congruencia (O(n)) se hace a lo más dos veces.
    * Congruencia de polígonos ortogonales: se describe cada pieza (en
      sentido antihorario, sin vértices colineales) por la secuencia cíclica
      (largo de arista, tipo de giro convexo/reflejo, largo, giro, …). Dos
      piezas son congruentes ⇔ la secuencia de una es rotación cíclica de la
      otra (rotación+traslación) o de la otra invertida (reflexión). Se
      busca como subcadena en la secuencia duplicada (búsqueda de cadenas
      de Python, en C).

MACROALGORITMO
    1. Leer el polígono, quitar vértices repetidos/colineales y orientarlo
       antihorario. Calcular arcos s_k, perímetro L, sumas prefijas de cruces.
    2. Juntar los cortes de p (vértices con s < L/2) y de q (s - L/2):
       intervalos de t donde p y q están en aristas fijas (dos punteros).
    3. En cada intervalo generar candidatos t: el inicio, las raíces enteras
       de p.x = q.x y p.y = q.y y, si alguna diferencia es constante 0, la
       raíz de "área = mitad".
    4. Para cada candidato: p, q alineados (misma x o misma y) y distintos;
       área exacta igual a la mitad.
    5. Si pasa: verificar que la cuerda es una componente de recta∩interior.
    6. Si es válida: armar las dos piezas y comparar sus secuencias
       cíclicas (directa e invertida). Si coinciden → "Yes".
    7. Si ningún candidato sirve → "No".

COMPLEJIDAD
    O(n log n) por el ordenamiento de cortes + O(n) por cada recta distinta
    que haya que analizar (en la práctica pocas) + O(n) por cada prueba de
    congruencia (≤ 2). Memoria O(n). Con n = 10^5 un caso tarda ≈ 0,6-0,9 s
    en Python; 50 casos máximos serían ~40 s (más que el límite de 5 s).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Guangzhou 2017/H")
    - Fuerza bruta independiente (poliominós aleatorios sin huecos ni
      "pellizcos": prueba TODOS los segmentos de rejilla con extremos
      enteros, separa las celdas en dos componentes con BFS y compara las
      dos formas bajo las 8 simetrías; no usa el argumento del perímetro):
      OK en 5900 polígonos aleatorios (≈ 60 % "Yes"), incluidos espejos,
      rotaciones de 90°/180° pegadas, "casi simétricos" (una celda de más
      o de menos) y versiones estiradas ×2/×3 en cada eje (cortes que no
      caen en coordenadas de vértices).
    - Rendimiento: peine de 10^5 vértices con dientes aleatorios ≈ 0,6 s
      por caso (10 casos en un archivo ≈ 6 s); peine simétrico (Yes) ≈ 0,4 s.
"""
import sys
from bisect import bisect_left


def cruz(ax, ay, bx, by):
    return ax * by - ay * bx


def simplificar(P):
    """Quita vértices repetidos y colineales (también en la unión cíclica)."""
    res = []
    for pt in P:
        if res and res[-1] == pt:
            continue
        while len(res) >= 2 and _colineal(res[-2], res[-1], pt):
            res.pop()
        res.append(pt)
    cambio = True
    while cambio and len(res) >= 3:
        cambio = False
        if res[-1] == res[0]:
            res.pop()
            cambio = True
        elif _colineal(res[-2], res[-1], res[0]):
            res.pop()
            cambio = True
        elif _colineal(res[-1], res[0], res[1]):
            res.pop(0)
            cambio = True
    return res


def _colineal(a, b, c):
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]) == 0


def firma(W):
    """Secuencia cíclica (largo, giro, largo, giro, …) de un polígono CCW.

    Los giros se codifican como -1 (convexo) y -2 (reflejo) para no
    confundirlos con largos (positivos)."""
    k = len(W)
    tokens = []
    for i in range(k):
        ax, ay = W[i]
        bx, by = W[(i + 1) % k]
        cx, cy = W[(i + 2) % k]
        tokens.append(abs(bx - ax) + abs(by - ay))
        giro = cruz(bx - ax, by - ay, cx - bx, cy - by)
        tokens.append(-1 if giro > 0 else -2)
    return tokens


def congruentes(W1, W2):
    W1 = simplificar(W1)
    W2 = simplificar(W2)
    if len(W1) != len(W2):
        return False
    t1, t2 = firma(W1), firma(W2)
    patron = "," + ",".join(map(str, t2)) + ","
    texto = "," + ",".join(map(str, t1 + t1)) + ","
    if patron in texto:                    # rotación (+ traslación)
        return True
    r = t1[::-1]
    texto_r = "," + ",".join(map(str, r + r)) + ","
    return patron in texto_r               # reflexión


def componentes_recta(X, Y, n, vertical, c):
    """Intervalos abiertos (a, b) de la recta (x = c si vertical, y = c si
    no) que están en el interior del polígono."""
    # Para recta vertical, las aristas que la cruzan son las horizontales.
    izq, der = [], []
    for k in range(n):
        x1, y1 = X[k], Y[k]
        x2, y2 = X[k + 1], Y[k + 1]
        if vertical:
            if y1 != y2:
                continue
            lo, hi, h = min(x1, x2), max(x1, x2), y1
        else:
            if x1 != x2:
                continue
            lo, hi, h = min(y1, y2), max(y1, y2), x1
        if lo < c <= hi:
            izq.append(h)
        if lo <= c < hi:
            der.append(h)
    izq.sort()
    der.sort()
    # Intervalos "dentro" de cada recta desplazada (paridad de cruces).
    A = [(izq[i], izq[i + 1]) for i in range(0, len(izq), 2)]
    B = [(der[i], der[i + 1]) for i in range(0, len(der), 2)]
    # Intersección de dos uniones de intervalos ordenados.
    res = set()
    i = j = 0
    while i < len(A) and j < len(B):
        lo = max(A[i][0], B[j][0])
        hi = min(A[i][1], B[j][1])
        if lo < hi:
            res.add((lo, hi))
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1
    return res


def resolver(P):
    P = simplificar(P)
    n = len(P)
    if n < 4:
        return False
    # Orientación antihoraria (área con signo positiva).
    area2 = sum(cruz(P[k][0], P[k][1], P[(k + 1) % n][0], P[(k + 1) % n][1])
                for k in range(n))
    if area2 < 0:
        P.reverse()
        area2 = -area2
    X = [p[0] for p in P] + [P[0][0]]
    Y = [p[1] for p in P] + [P[0][1]]

    # Arco acumulado s[k] (posición del vértice k), direcciones unitarias y
    # sumas prefijas de productos cruz C[k] = Σ_{i<k} cruz(V_i, V_{i+1}).
    s = [0] * (n + 1)
    dx = [0] * n
    dy = [0] * n
    C = [0] * (n + 1)
    for k in range(n):
        ex, ey = X[k + 1] - X[k], Y[k + 1] - Y[k]
        largo = abs(ex) + abs(ey)
        s[k + 1] = s[k] + largo
        dx[k] = (ex > 0) - (ex < 0)
        dy[k] = (ey > 0) - (ey < 0)
        C[k + 1] = C[k] + cruz(X[k], Y[k], X[k + 1], Y[k + 1])
    L = s[n]
    mitad = L // 2

    # Cortes de t ∈ [0, mitad): vértices bajo p y vértices bajo q.
    cortes = set(v for v in s[:n] if v < mitad)
    cortes.update(v - mitad for v in s[:n] if v >= mitad)
    cortes = sorted(cortes)
    cortes.append(mitad)

    cache_rectas = {}
    probados = set()

    def area_p1(t, ip, iq):
        """2·área(P1) con p en la arista ip y q en la arista iq."""
        px = X[ip] + (t - s[ip]) * dx[ip]
        py = Y[ip] + (t - s[ip]) * dy[ip]
        tq = t + mitad
        qx = X[iq] + (tq - s[iq]) * dx[iq]
        qy = Y[iq] + (tq - s[iq]) * dy[iq]
        return (cruz(px, py, X[ip + 1], Y[ip + 1]) + C[iq] - C[ip + 1]
                + cruz(X[iq], Y[iq], qx, qy) + cruz(qx, qy, px, py))

    def probar(t, ip, iq):
        """¿El corte con p en posición t (aristas ip, iq) sirve?"""
        if t in probados:
            return False
        probados.add(t)
        px = X[ip] + (t - s[ip]) * dx[ip]
        py = Y[ip] + (t - s[ip]) * dy[ip]
        tq = t + mitad
        qx = X[iq] + (tq - s[iq]) * dx[iq]
        qy = Y[iq] + (tq - s[iq]) * dy[iq]
        if px == qx and py != qy:
            vertical, c, a, b = True, px, min(py, qy), max(py, qy)
        elif py == qy and px != qx:
            vertical, c, a, b = False, py, min(px, qx), max(px, qx)
        else:
            return False
        if 2 * area_p1(t, ip, iq) != area2:
            return False
        clave = (vertical, c)
        if clave not in cache_rectas:
            cache_rectas[clave] = componentes_recta(X, Y, n, vertical, c)
        if (a, b) not in cache_rectas[clave]:
            return False
        # Piezas: P1 = p → vértices ip+1..iq → q ; P2 = q → iq+1..ip+n → p.
        W1 = [(px, py)] + [(X[k], Y[k]) for k in range(ip + 1, iq + 1)] + [(qx, qy)]
        W2 = [(qx, qy)] + [(X[k % n], Y[k % n]) for k in range(iq + 1, ip + n + 1)] + [(px, py)]
        return congruentes(W1, W2)

    ip = 0
    iq = bisect_left(s, mitad + 1) - 1          # arista que contiene a t = mitad
    for idx in range(len(cortes) - 1):
        ta, tb = cortes[idx], cortes[idx + 1]
        while s[ip + 1] <= ta:
            ip += 1
        while s[iq + 1] <= ta + mitad:
            iq += 1
        if probar(ta, ip, iq):
            return True
        # p(t) - q(t) = c0 + pendiente·t  en cada coordenada
        for d_p, d_q, coord in ((dx[ip], dx[iq], X), (dy[ip], dy[iq], Y)):
            c0 = (coord[ip] - s[ip] * d_p) - (coord[iq] + (mitad - s[iq]) * d_q)
            pend = d_p - d_q
            if pend != 0:
                num = -c0
                if num % pend == 0:
                    t = num // pend
                    if ta < t < tb and probar(t, ip, iq):
                        return True
            elif c0 == 0 and tb - ta >= 2:
                # Alineados en todo el intervalo: la condición de área es lineal.
                g0 = 2 * area_p1(ta, ip, iq) - area2
                g1 = 2 * area_p1(ta + 1, ip, iq) - area2
                pg = g1 - g0
                if pg != 0 and (-g0) % pg == 0:
                    t = ta + (-g0) // pg
                    if ta < t < tb and probar(t, ip, iq):
                        return True
    return False


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos])
        pos += 1
        P = [(int(datos[pos + 2 * k]), int(datos[pos + 2 * k + 1])) for k in range(n)]
        pos += 2 * n
        salida.append("Yes" if resolver(P) else "No")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
