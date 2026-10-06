"""
Colombia 2026 — L: Don't Ask Why 2D («No preguntes por qué 2D»)
Ejecutar: python dont.py < dont.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un simulador de proteínas quedó atascado en "modo 2D": cada proteína es
    una cadena de N aminoácidos H (hidrofóbico) o P (polar) que se pliega
    como un camino autoevitante en la cuadrícula. Un contacto hidrofóbico es
    un par de H adyacentes en la cuadrícula pero NO consecutivos en la
    cadena. Hay que diseñar la secuencia y el plegamiento más estables.

QUÉ HAY QUE HACER
    Entrada: varios pedidos "N B", uno por línea, hasta "0 0" (T <= 60).
    Salida:  por pedido: "contactos secuencia plegado", donde contactos es el
             MÁXIMO alcanzable, la secuencia tiene N letras con exactamente B
             H y el plegado son N-1 letras de {R,L,U,D} que forman un camino
             autoevitante que logra ese máximo. Si N = 1 no se imprime
             plegado. Se acepta CUALQUIER respuesta óptima.
    Restricciones clave: 1 <= N <= 15, 0 <= B <= N.

IDEA Y ALGORITMO
    Búsqueda exhaustiva (backtracking) de caminos autoevitantes con
    reducción por simetría + optimización sobre el "grafo de contactos".

    1) Separar plegado y secuencia. Fijado un plegado, sus pares en contacto
       (i, j) (adyacentes en la cuadrícula, |i-j| > 1) forman un grafo G
       sobre las posiciones 0..N-1. Elegir la secuencia = elegir el conjunto
       S de posiciones H (|S| = B) y los contactos son las aristas de G con
       ambos extremos en S. Muchos plegados dan el MISMO grafo, así que se
       guardan sin repetir (12 495 grafos distintos para N = 15).

    2) Simetría. Rotar o reflejar un plegado no cambia sus contactos. Toda
       caminata se puede rotar para que el primer paso sea R y reflejar
       (arriba <-> abajo) para que el primer giro sea U. Así se recorren
       296 806 caminos para N = 15 en vez de 2 374 444 (≈ 1/8).

    3) Mejor S para un grafo. G tiene pocas aristas (<= 8 con N <= 15), así
       que se enumeran todos los SUBCONJUNTOS DE ARISTAS A (2^E <= 256): si
       A toca v vértices distintos, con B >= v H's se logran al menos |A|
       contactos (poner H en esos v vértices y las B - v restantes en
       cualquier otro lugar; más H nunca quitan contactos). Recíprocamente,
       las aristas internas de un S óptimo son un tal A con v <= B. Por eso
       mejor(B) = max { |A| : A subconjunto de aristas que toca <= B
       vértices }, maximizado sobre todos los grafos. Se calcula
       mejor_exacto[v] y luego un máximo de prefijos sobre v.

    4) Reconstrucción. Se guarda, para cada v, el plegado y los vértices
       cubiertos; la secuencia pone H ahí y completa con H en las primeras
       posiciones libres hasta tener B. Por último se CUENTAN los contactos
       del par (secuencia, plegado) construido y eso es lo que se imprime
       (coincide con el máximo por el argumento de 3).

    Por qué no una fórmula: el problema HP en 2D es NP-difícil en general;
    con N <= 15 la enumeración completa es lo esperado. (La solución del
    usuario precalcula las 135 respuestas fuera de línea; aquí se calculan
    en ejecución, solo para los N pedidos, con caché por N.)

MACROALGORITMO
    1. Leer los pedidos (N, B).
    2. Para cada N distinto: DFS de caminos autoevitantes desde el origen
       (primer paso R, primer giro U), manteniendo en una máscara de bits los
       contactos que se crean al colocar cada aminoácido.
    3. Al completar un camino, guardar su máscara de contactos si es nueva
       (diccionario máscara -> plegado).
    4. Para cada grafo distinto, enumerar los subconjuntos de aristas:
       vértices cubiertos v y número de aristas k; mejorar mejor_exacto[v].
    5. Máximo de prefijos: para cada B, el mejor v <= B.
    6. Construir la secuencia (H en los vértices cubiertos + relleno),
       contar sus contactos sobre el plegado e imprimir.

COMPLEJIDAD
    Tiempo: exponencial en N, dominado por N = 15 (≈3·10^5 caminos y
    ≈6·10^5 subconjuntos de aristas): ~0.8 s para 60 pedidos con N = 15 y
    ~1.2 s para los 135 pares (N, B) posibles (cada N se calcula una sola
    vez y se guarda en caché). Memoria: los
    grafos distintos (~1.2·10^4 enteros).

EJEMPLO A MANO
    N=4, B=2: el único contacto posible es (0,3) (debe ser |i-j| impar y
    >= 3), logrado por el cuadrado RUL -> "1 HPPH RUL".

VERIFICACIÓN
    - Ejemplo del enunciado: probar.py marca FALLA porque compara texto y el
      problema acepta CUALQUIER respuesta óptima: los conteos de contactos
      coinciden con los del ejemplo (1, 2, 0, 0) y las secuencias/plegados
      son válidos, pero difieren en el empate: para "6 4" se imprime
      "2 HHPHPH RULLD" en vez de "2 HHPPHH RRULL" (ambas con 2 contactos).
      Las otras 3 líneas salen idénticas. Se validó con un verificador propio.
    - Verificador (las 135 combinaciones N <= 15, 0 <= B <= N): la secuencia
      tiene N letras y B H, el plegado tiene N-1 pasos y es autoevitante, y
      los contactos recontados coinciden con el número impreso.
    - Fuerza bruta: el máximo coincide para todo N <= 9 (todas las B) con
      una búsqueda que recorre TODOS los caminos sin simetría y TODAS las
      secuencias; y para los 135 pares coincide con la tabla del usuario
      (dont.py en la raíz), que se generó con otro método de maximización.
"""
import sys

ANCHO = 100            # celda (x, y) se codifica como x + ANCHO * y
PASOS = (("R", 1), ("L", -1), ("U", ANCHO), ("D", -ANCHO))
_cache = {}            # N -> lista de (contactos, cubiertos, plegado) por B


def grafos_de_contacto(n):
    """Recorre los caminos autoevitantes de n celdas (primer paso R, primer
    giro U) y devuelve {máscara_de_contactos: un plegado que la produce}.
    El contacto (j, i) con j < i se guarda en el bit j*16 + i."""
    ocupado = {0: 0}                 # celda -> índice del aminoácido
    plegado = []
    grafos = {}

    def dfs(i, celda, mascara, ya_giro):
        if i == n:                   # camino completo
            if mascara not in grafos:
                grafos[mascara] = "".join(plegado)
            return
        for letra, delta in PASOS:
            if i == 1 and letra != "R":
                continue             # simetría de rotación: primer paso R
            if not ya_giro and (letra == "L" or letra == "D"):
                continue             # reflexión: el primer giro es hacia U
            nueva = celda + delta
            if nueva in ocupado:
                continue             # autoevitante
            # Contactos nuevos: vecinos ya ocupados que no son el anterior.
            m = mascara
            for vecina in (nueva + 1, nueva - 1, nueva + ANCHO, nueva - ANCHO):
                j = ocupado.get(vecina)
                if j is not None and j < i - 1:
                    m |= 1 << (j * 16 + i)
            ocupado[nueva] = i
            plegado.append(letra)
            dfs(i + 1, nueva, m, ya_giro or letra == "U")
            del ocupado[nueva]
            plegado.pop()

    dfs(1, 0, 0, False)
    return grafos


def mejores_por_b(n):
    """Para cada B = 0..n devuelve (contactos, máscara_de_vértices, plegado)
    con el máximo de contactos alcanzable usando a lo sumo B vértices H."""
    if n in _cache:
        return _cache[n]
    recto = "R" * (n - 1)
    # mejor_exacto[v] = mejor (aristas, vértices, plegado) cubriendo v vértices.
    mejor_exacto = [(0, 0, recto)] * (n + 1)
    for mascara, plegado in grafos_de_contacto(n).items():
        # Aristas como máscaras de sus dos vértices.
        aristas = []
        while mascara:
            b = (mascara & -mascara).bit_length() - 1
            mascara &= mascara - 1
            aristas.append((1 << (b // 16)) | (1 << (b % 16)))
        # Subconjuntos de aristas: cubiertos[s] = vértices tocados por s.
        e = len(aristas)
        cubiertos = [0] * (1 << e)
        tamano = [0] * (1 << e)
        for s in range(1, 1 << e):
            resto = s & (s - 1)
            bajo = (s & -s).bit_length() - 1
            cub = cubiertos[resto] | aristas[bajo]
            cubiertos[s] = cub
            k = tamano[resto] + 1
            tamano[s] = k
            v = bin(cub).count("1")
            if k > mejor_exacto[v][0]:
                mejor_exacto[v] = (k, cub, plegado)
    # Máximo de prefijos: con B H's sirve cualquier conjunto de v <= B vértices.
    resultado, actual = [], mejor_exacto[0]
    for v in range(n + 1):
        if mejor_exacto[v][0] > actual[0]:
            actual = mejor_exacto[v]
        resultado.append(actual)
    _cache[n] = resultado
    return resultado


def contar_contactos(secuencia, plegado):
    """Cuenta los contactos H-H no consecutivos del plegado (verificación)."""
    delta = dict(PASOS)
    celdas, celda = [0], 0
    for letra in plegado:
        celda += delta[letra]
        celdas.append(celda)
    indice = {c: i for i, c in enumerate(celdas)}
    total = 0
    for i, c in enumerate(celdas):
        if secuencia[i] != "H":
            continue
        for vecina in (c + 1, c + ANCHO):   # cada par se mira una sola vez
            j = indice.get(vecina)
            if j is not None and abs(i - j) > 1 and secuencia[j] == "H":
                total += 1
    return total


def resolver(n, b):
    _, cubiertos, plegado = mejores_por_b(n)[b]
    # H en los vértices cubiertos; completar con H en las primeras libres.
    letras = ["H" if cubiertos >> i & 1 else "P" for i in range(n)]
    faltan = b - letras.count("H")
    for i in range(n):
        if faltan == 0:
            break
        if letras[i] == "P":
            letras[i] = "H"
            faltan -= 1
    secuencia = "".join(letras)
    contactos = contar_contactos(secuencia, plegado)
    if n == 1:
        return f"{contactos} {secuencia}"           # sin plegado
    return f"{contactos} {secuencia} {plegado}"


def main():
    datos = sys.stdin.read().split()
    salida = []
    for idx in range(0, len(datos) - 1, 2):
        n, b = int(datos[idx]), int(datos[idx + 1])
        if n == 0 and b == 0:                        # fin de la entrada
            break
        salida.append(resolver(n, b))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
