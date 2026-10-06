"""
Colombia 2024 — G: Signal Coverage («Cobertura de señal»)
Ejecutar: python signal.py < signal.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Nlogonia negocia con un operador la instalación de n antenas. Cada
    antena cubre un disco cerrado (centro (x, y), radio r) y opera de forma
    continua del día b al día e. Nlogonia exige que ningún punto quede
    cubierto por dos antenas a la vez; el operador exige que, para cada par
    de una lista, se instale al menos una de las dos antenas.

QUÉ HAY QUE HACER
    Entrada: T casos. Cada uno: n m (2 ≤ n ≤ 10⁴, 1 ≤ m ≤ 10⁴); n líneas
             "r x y b e" (1 ≤ r, x, y ≤ 5000; 1 ≤ b ≤ e ≤ 5000); m líneas
             "u v" (pares de restricción, u ≠ v).
    Salida:  "Impossible", o una cadena de n bits (1 = instalar) válida;
             cualquier solución válida sirve.

IDEA Y ALGORITMO
    2-SAT. Variable x_i = "se instala la antena i".
      • Dos antenas CHOCAN si sus discos cerrados se tocan
        (dist² ≤ (r_i + r_j)²) y sus periodos se solapan (b_i ≤ e_j y
        b_j ≤ e_i; ambos días están incluidos). Cláusula: (¬x_i ∨ ¬x_j).
      • Par de restricción (u, v): cláusula (x_u ∨ x_v).
    2-SAT se resuelve con el grafo de implicaciones (a ∨ b ⇒ ¬a→b, ¬b→a) y
    componentes fuertemente conexas (Tarjan): es insatisfacible si x y ¬x
    caen en la misma componente; si no, x = verdadero cuando la componente
    de x va después que la de ¬x en orden topológico.

    Reducción 1: una antena que no aparece en ningún par de restricción se
    pone en 0 sin riesgo (no instalar nunca viola "no se solapan"), así que
    solo intervienen las antenas de los pares.

    Problema: el número de choques puede ser Θ(n²) ≈ 5·10⁷ (discos grandes
    en una zona de 5000×5000), imposible de listar en Python. Solución:
    GENERACIÓN PEREZOSA DE RESTRICCIONES (lazy constraints):
      a) Se listan los choques con un barrido (sweep) en x; si son pocos
         (≤ TOPE) se tienen todos y un único 2-SAT da la respuesta exacta.
      b) Si hay más, se resuelve 2-SAT solo con un subconjunto E de
         choques. Si ya es insatisfacible ⇒ con todos también lo es
         (más cláusulas solo restringen más) ⇒ "Impossible".
         Si es satisfacible, se apagan las antenas que sobran (apagar una
         antena nunca rompe un "no ambos"; solo hace falta que sus pares
         (u, v) sigan cubiertos por el otro extremo), se toma el conjunto S
         de antenas encendidas y se buscan choques DENTRO de S (a lo sumo
         TOPE_RONDA por ronda). Si no hay ninguno, la asignación
         cumple TODAS las cláusulas ⇒ es respuesta válida. Si los hay, se
         agregan a E (son nuevos: la asignación actual los violaba) y se
         repite. Termina porque E crece estrictamente cada ronda.
    Así la respuesta siempre es exacta; solo el tiempo depende de cuántas
    rondas hagan falta (en la práctica pocas: con muchos choques el 2-SAT
    se vuelve insatisfacible enseguida, o S queda pequeño).

    Barrido para listar choques: ordenar por x − r; mantener una lista de
    "activos" cuyo intervalo [x − r, x + r] aún puede solapar; para cada
    antena nueva se descartan los activos con x + r < x_nueva − r y se
    prueban los restantes (tiempo y distancia exacta con enteros).

MACROALGORITMO
    1. Leer antenas y pares; quedarse con las antenas que aparecen en pares
       (renumeradas 0..k-1).
    2. Listar choques entre ellas con el barrido, con un tope TOPE.
    3. Repetir:
       a. Construir el grafo de implicaciones con los pares (x_u ∨ x_v) y
          los choques conocidos (¬x_i ∨ ¬x_j); Tarjan iterativo.
       b. Si alguna x_i comparte componente con ¬x_i ⇒ "Impossible".
       c. Si la lista de choques era completa, terminar. Si no, apagar las
          antenas sobrantes (de mayor a menor radio), S = encendidas, y
          buscar choques dentro de S (barrido con tope por ronda); si no
          hay, terminar; si hay, agregarlos y volver a (a).
    4. Imprimir la cadena de n bits (antenas fuera de los pares = 0).

COMPLEJIDAD
    Barrido: O(k log k + pares candidatos). 2-SAT: O(k + m + |E|) por ronda.
    Casos medidos (n = m = 10⁴, una sola prueba):
      - discos pequeños y tiempos aleatorios (pocos choques): ~0,2 s;
      - discos y tiempos aleatorios en todo el rango (~10⁷ choques):
        ~0,5 s ("Impossible" ya con el primer subconjunto);
      - radios ≤ 300, mismo periodo, pares en ciclo o aleatorios: ~1,5–2 s;
      - ADVERSARIO satisfacible "plantado" (la mitad son antenas diminutas
        compatibles entre sí, la otra mitad discos enormes que chocan con
        casi todo, y cada par incluye una diminuta): 5,5–8,5 s, porque se
        necesitan ~10 rondas de 2-SAT con ~10⁶ cláusulas. Es el caso lento
        en Python; el número de rondas no tiene una cota ajustada pequeña.
    Memoria: O(k + m + |E|), con |E| ≲ 1,5·10⁶ en los casos medidos.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/G")
    - Fuerza bruta: OK en 1500 casos aleatorios (n ≤ 9, coordenadas y
      radios pequeños para forzar choques) contra la enumeración de los 2^n
      subconjuntos: misma decisión posible/imposible y, cuando es posible,
      nuestra cadena cumple todas las restricciones. Se probó con los topes
      normales y con topes 1, 2, 3 para ejercitar las rondas perezosas.
    - Casos grandes satisfacibles: la cadena devuelta se validó con un
      verificador O(|S|²) independiente (todas las restricciones OK).
    - Nota: cualquier solución válida es aceptada; la numeración de
      literales elegida reproduce exactamente la salida de ejemplo.
"""
import sys

TOPE = 300000         # máximo de choques que se listan de una vez al inicio
TOPE_RONDA = 100000   # máximo de choques nuevos que se agregan por ronda


def listar_choques(ids, R, X, Y, B, E, tope):
    """Pares (u, v) de antenas de `ids` que chocan (espacio y tiempo).
    Devuelve (pares, completo); completo = False si se alcanzó el tope."""
    orden = sorted(ids, key=lambda v: X[v] - R[v])
    activos = []                  # antenas cuyo intervalo en x sigue "abierto"
    pares = []
    for v in orden:
        xv, yv, rv, bv, ev = X[v], Y[v], R[v], B[v], E[v]
        izq = xv - rv
        siguen = []
        for u in activos:
            ru = R[u]
            if X[u] + ru < izq:   # ya no puede solapar a nadie posterior
                continue
            siguen.append(u)
            if B[u] <= ev and bv <= E[u]:          # periodos solapados
                dx = X[u] - xv
                dy = Y[u] - yv
                s = ru + rv
                if dx * dx + dy * dy <= s * s:     # discos cerrados se tocan
                    pares.append((u, v))
                    if len(pares) >= tope:
                        return pares, False
        siguen.append(v)
        activos = siguen
    return pares, True


def dos_sat(k, clausulas_o, clausulas_no_ambos):
    """2-SAT sobre k variables. Nodo 2i = ¬x_i, 2i+1 = x_i.
    (Cualquier asignación válida sirve; con esta numeración, en el ejemplo
    del enunciado sale justo la misma cadena que la salida de muestra.)
    clausulas_o: (u, v) para (x_u ∨ x_v); clausulas_no_ambos: (u, v) para
    (¬x_u ∨ ¬x_v). Devuelve lista de bool o None si es insatisfacible."""
    total = 2 * k
    ady = [[] for _ in range(total)]
    for u, v in clausulas_o:              # ¬u → v,  ¬v → u
        ady[2 * u].append(2 * v + 1)
        ady[2 * v].append(2 * u + 1)
    for u, v in clausulas_no_ambos:       # u → ¬v,  v → ¬u
        ady[2 * u + 1].append(2 * v)
        ady[2 * v + 1].append(2 * u)

    # Tarjan iterativo: comp[] se numera en orden topológico INVERSO.
    indice = [-1] * total
    bajo = [0] * total
    en_pila = [False] * total
    comp = [-1] * total
    pila = []
    contador = 0
    ncomp = 0
    for raiz in range(total):
        if indice[raiz] != -1:
            continue
        trabajo = [(raiz, 0)]
        indice[raiz] = bajo[raiz] = contador; contador += 1
        pila.append(raiz); en_pila[raiz] = True
        while trabajo:
            nodo, i = trabajo[-1]
            vecinos = ady[nodo]
            if i < len(vecinos):
                trabajo[-1] = (nodo, i + 1)
                w = vecinos[i]
                if indice[w] == -1:
                    indice[w] = bajo[w] = contador; contador += 1
                    pila.append(w); en_pila[w] = True
                    trabajo.append((w, 0))
                elif en_pila[w] and indice[w] < bajo[nodo]:
                    bajo[nodo] = indice[w]
            else:
                trabajo.pop()
                if trabajo:
                    padre = trabajo[-1][0]
                    if bajo[nodo] < bajo[padre]:
                        bajo[padre] = bajo[nodo]
                if bajo[nodo] == indice[nodo]:      # raíz de una componente
                    while True:
                        w = pila.pop()
                        en_pila[w] = False
                        comp[w] = ncomp
                        if w == nodo:
                            break
                    ncomp += 1
    asignacion = []
    for i in range(k):
        if comp[2 * i] == comp[2 * i + 1]:
            return None
        # x_i es verdadero si su componente va DESPUÉS que la de ¬x_i en el
        # orden topológico, es decir, si tiene número de Tarjan MENOR.
        asignacion.append(comp[2 * i + 1] < comp[2 * i])
    return asignacion


def apagar_sobrantes(asignacion, clausulas_o, R):
    """Mejora local que conserva la validez: apagar una antena nunca viola
    un (¬x_i ∨ ¬x_j); solo puede violar un par (x_u ∨ x_v) si el otro
    extremo está apagado. Se intenta apagar primero las de mayor radio
    (las que más choques suelen tener)."""
    k = len(asignacion)
    vecinos = [[] for _ in range(k)]
    for u, v in clausulas_o:
        vecinos[u].append(v)
        vecinos[v].append(u)
    for i in sorted(range(k), key=lambda i: -R[i]):
        if asignacion[i] and all(asignacion[j] for j in vecinos[i] if j != i):
            if i not in vecinos[i]:          # (x_i ∨ x_i) obliga a x_i
                asignacion[i] = False


def resolver(n, antenas, pares, tope=TOPE, tope_ronda=TOPE_RONDA):
    """antenas: lista de (r, x, y, b, e); pares: lista de (u, v) 0-indexados.
    Devuelve la cadena de bits o "Impossible"."""
    # 1. Solo importan las antenas que aparecen en algún par.
    relevantes = sorted({u for par in pares for u in par})
    pos = {v: i for i, v in enumerate(relevantes)}
    k = len(relevantes)
    R = [antenas[v][0] for v in relevantes]
    X = [antenas[v][1] for v in relevantes]
    Y = [antenas[v][2] for v in relevantes]
    B = [antenas[v][3] for v in relevantes]
    E = [antenas[v][4] for v in relevantes]
    clausulas_o = [(pos[u], pos[v]) for u, v in pares]

    # 2. Choques conocidos (todos, si caben bajo el tope).
    choques, completo = listar_choques(range(k), R, X, Y, B, E, tope)
    while True:
        asignacion = dos_sat(k, clausulas_o, choques)
        if asignacion is None:
            return "Impossible"       # insatisfacible ya con un subconjunto
        if completo:
            break
        # 3. Apagar lo que sobra (no rompe ninguna cláusula conocida) para
        #    que S sea pequeño y aparezcan menos choques nuevos.
        apagar_sobrantes(asignacion, clausulas_o, R)
        # 4. Verificar la asignación: ¿chocan antenas encendidas entre sí?
        encendidas = [i for i in range(k) if asignacion[i]]
        nuevos, _ = listar_choques(encendidas, R, X, Y, B, E, tope_ronda)
        if not nuevos:
            break                     # cumple todas las cláusulas
        choques.extend(nuevos)
    bits = ['0'] * n
    for i, v in enumerate(relevantes):
        if asignacion[i]:
            bits[v] = '1'
    return "".join(bits)


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    t = int(datos[pos]); pos += 1
    salida = []
    for _ in range(t):
        n, m = int(datos[pos]), int(datos[pos + 1]); pos += 2
        antenas = []
        for _ in range(n):
            antenas.append(tuple(int(z) for z in datos[pos:pos + 5]))
            pos += 5
        pares = []
        for _ in range(m):
            pares.append((int(datos[pos]) - 1, int(datos[pos + 1]) - 1))
            pos += 2
        salida.append(resolver(n, antenas, pares))
    sys.stdout.write("\n".join(salida) + "\n")


if __name__ == "__main__":
    main()
