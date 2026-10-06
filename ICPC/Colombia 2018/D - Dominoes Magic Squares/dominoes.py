"""
Colombia 2018 — D: Dominoes Magic Squares («Cuadrados mágicos de dominó»)
Ejecutar: python dominoes.py < dominoes.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una ficha de dominó [a|b] (0 ≤ a, b ≤ 6) ocupa dos casillas unitarias.
    Con 8 fichas se cubre un tablero 4×4; la pregunta es si se pueden
    acomodar para que el tablero sea un CUADRADO MÁGICO: las 4 filas, las
    4 columnas y las 2 diagonales suman lo mismo.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta fin de archivo; cada caso son 8 líneas
             «a b» (8 fichas distintas).
    Salida:  «Y» si se puede construir el cuadrado mágico, «N» si no.
    Restricciones clave: el tablero es fijo (4×4, 8 fichas); el número de
             casos no está acotado en el enunciado.

IDEA Y ALGORITMO
    BÚSQUEDA CON RETROCESO (backtracking) casilla por casilla, con poda por
    cotas de las sumas parciales.
    - La suma mágica está forzada: las 4 filas cubren todo el tablero, así
      que S = (suma de todas las etiquetas) / 4. Si no es entera → «N».
    - El espacio completo es 36 teselaciones del 4×4 con dominós × 8!
      asignaciones × 2^8 orientaciones ≈ 3.7·10^8 tableros: demasiado para
      Python sin poda.
    - Generación de teselaciones sin repetir: se fija un ORDEN de casillas;
      la primera casilla vacía según ese orden tiene que estar cubierta por
      la ficha que se coloca ahora, junto con alguna vecina vacía (arriba,
      abajo, izquierda o derecha). Cada teselación aparece exactamente una
      vez, sea cual sea el orden. Se usa el orden «fila 0, columna 0,
      fila 1, columna 1, …» porque completa líneas lo antes posible (medido:
      ~1.6× más rápido que el orden fila por fila).
    - Poda por cotas: para una casilla, cada línea l que la contiene (fila,
      columna y, si aplica, diagonal) con suma parcial s_l y f_l casillas
      vacías impone  S − s_l − 6·(f_l − 1) ≤ valor ≤ S − s_l
      (no pasarse de S; y aun poniendo 6 en las demás casillas vacías, poder
      llegar a S). Si la casilla es la última vacía de una línea, la cota
      fija el valor exacto. En vez de probar las 8 fichas a ciegas, se
      recorren los VALORES x permitidos para la casilla y sólo las fichas
      que tienen la etiqueta x (índice «por valor»); luego la otra mitad y
      debe caer en las cotas de la casilla vecina (calculadas ya con x
      puesto). Así, toda línea queda siempre dentro de sus cotas, y al
      llenar el tablero todas suman exactamente S.
    - Los resultados se memorizan por conjunto de fichas (casos repetidos).

MACROALGORITMO
    1. Leer los casos de 8 fichas.
    2. total = suma de etiquetas; si total % 4 ≠ 0 → N. Si no, S = total/4.
    3. Índice por valor: para cada etiqueta v, las fichas (i, otra etiqueta)
       que la contienen.
    4. buscar(pos): primera casilla vacía en el orden fijado; si no hay →
       éxito.
    5. Para cada valor x dentro de las cotas de la casilla y cada ficha no
       usada con etiqueta x: poner x; para cada vecina vacía, si la otra
       etiqueta y cabe en sus cotas, ponerla y llamar buscar; deshacer.
    6. Imprimir Y si la búsqueda tuvo éxito, N si no.

COMPLEJIDAD
    Tablero fijo → tiempo acotado por una constante, pero la constante
    importa en Python: sobre 450 casos aleatorios con suma divisible por 4,
    ~30 ms por caso en promedio y ~0.16 s el peor (450 casos: ~12.7 s en
    total). Con miles de casos distintos tardaría decenas de segundos; la
    memoización sólo ayuda si se repiten conjuntos de fichas.
    Memoria O(1).

EJEMPLO A MANO
    Primer ejemplo: total = 52 → S = 13, y existe la disposición del
    enunciado (4 4 2 3 / 3 3 2 5 / 1 3 5 4 / 5 3 4 1). Segundo ejemplo:
    total = 60 → S = 15, la búsqueda agota todas las opciones → N.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/D")
    - Fuerza bruta: OK en 152 casos (el ejemplo + 150 aleatorios con suma
      divisible por 4, ~12 % con respuesta Y) contra un programa en Java que
      enumera SIN poda las 36 teselaciones × 8! asignaciones × 2^8
      orientaciones (≈ 3.7·10^8 tableros por caso). Además coincide con una
      primera versión (backtracking fila por fila probando ficha por ficha)
      en otros 300 casos aleatorios.
"""
import sys

LADO = 4
MAX_ETIQUETA = 6

# LINEAS[c]: líneas que pasan por la casilla c (0..15, fila·4 + columna):
# filas 0..3, columnas 4..7, diagonal principal 8, antidiagonal 9.
LINEAS = []
for _f in range(LADO):
    for _c in range(LADO):
        _ls = [_f, LADO + _c]
        if _f == _c:
            _ls.append(8)
        if _f + _c == LADO - 1:
            _ls.append(9)
        LINEAS.append(tuple(_ls))

# Orden de llenado: fila 0, columna 0, fila 1, columna 1, fila 2, ...
ORDEN = [0, 1, 2, 3, 4, 8, 12, 5, 6, 7, 9, 13, 10, 11, 14, 15]

# VECINAS[c]: casillas adyacentes (arriba, abajo, izquierda, derecha).
VECINAS = []
for _i in range(16):
    _f, _c = divmod(_i, LADO)
    _v = []
    if _f > 0:
        _v.append(_i - LADO)
    if _f < LADO - 1:
        _v.append(_i + LADO)
    if _c > 0:
        _v.append(_i - 1)
    if _c < LADO - 1:
        _v.append(_i + 1)
    VECINAS.append(_v)


def se_puede(fichas):
    total = sum(a + b for a, b in fichas)
    if total % LADO:
        return False
    S = total // LADO
    tablero = [-1] * 16
    suma = [0] * 10          # suma parcial de cada línea
    vacias = [LADO] * 10     # casillas vacías de cada línea
    usada = [False] * 8
    # por_valor[v] = [(índice de ficha, la otra etiqueta)] para fichas con v.
    por_valor = [[] for _ in range(MAX_ETIQUETA + 1)]
    for i, (a, b) in enumerate(fichas):
        por_valor[a].append((i, b))
        if a != b:
            por_valor[b].append((i, a))

    def cotas(c):
        """Rango [lo, hi] de valores que puede tomar la casilla vacía c."""
        lo, hi = 0, MAX_ETIQUETA
        for l in LINEAS[c]:
            resto = S - suma[l]
            if resto < hi:
                hi = resto
            minimo = resto - MAX_ETIQUETA * (vacias[l] - 1)
            if minimo > lo:
                lo = minimo
        return lo, hi

    def poner(c, v, signo):
        """signo = +1 coloca v en c; signo = −1 lo retira."""
        tablero[c] = v if signo > 0 else -1
        for l in LINEAS[c]:
            suma[l] += signo * v
            vacias[l] -= signo

    def buscar(pos):
        while pos < 16 and tablero[ORDEN[pos]] != -1:
            pos += 1
        if pos == 16:
            return True          # todas las líneas llenas y = S por las cotas
        casilla = ORDEN[pos]
        lo, hi = cotas(casilla)
        vecinas = [o for o in VECINAS[casilla] if tablero[o] == -1]
        for x in range(lo, hi + 1):
            candidatas = [(i, y) for i, y in por_valor[x] if not usada[i]]
            if not candidatas:
                continue
            poner(casilla, x, +1)
            for otra in vecinas:
                lo2, hi2 = cotas(otra)          # ya contando x
                for i, y in candidatas:
                    if lo2 <= y <= hi2:
                        usada[i] = True
                        poner(otra, y, +1)
                        if buscar(pos + 1):
                            return True
                        poner(otra, y, -1)
                        usada[i] = False
            poner(casilla, x, -1)
        return False

    return buscar(0)


def main():
    datos = list(map(int, sys.stdin.buffer.read().split()))
    salida = []
    memo = {}
    for inicio in range(0, len(datos) - 15, 16):
        fichas = [(datos[inicio + 2 * t], datos[inicio + 2 * t + 1]) for t in range(8)]
        # Clave canónica: el resultado no depende del orden ni la orientación.
        clave = tuple(sorted(tuple(sorted(f)) for f in fichas))
        if clave not in memo:
            memo[clave] = se_puede(fichas)
        salida.append("Y" if memo[clave] else "N")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
