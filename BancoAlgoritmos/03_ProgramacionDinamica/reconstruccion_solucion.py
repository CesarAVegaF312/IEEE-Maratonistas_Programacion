"""
Programación dinámica — Reconstrucción de la solución óptima («Solution reconstruction»)
Nivel: Intermedio
Ejecutar: python reconstruccion_solucion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    La DP da el VALOR óptimo; muchos problemas además piden «muestre una
    solución», «imprima los objetos elegidos», o «si hay varias, la
    lexicográficamente menor». Esta técnica general se aplica a cualquier
    DP; aquí se ilustra con dos problemas clásicos:
      - Corte de varilla: una varilla de largo n se corta en piezas; una
        pieza de largo l vale precio[l]; maximizar la suma y decir las piezas.
      - Mochila 0/1 con el conjunto de índices lexicográficamente menor
        entre todos los óptimos.
    Señales: «imprima la solución», «en caso de empate, la menor
    lexicográficamente», «muestre el camino / las operaciones».

FUNCIÓN
    corte_guardando_decision(precio, n) -> (int, list)    método A
    corte_retrocediendo(precio, n) -> (int, list)         método B
        precio[l] para l = 1..L (precio[0] se ignora); n ≥ 0. Devuelven el
        valor máximo y una lista de largos de piezas que lo logra.
    mochila_lexicografica(pesos, valores, W) -> (int, list)  método C
        Valor máximo y la lista de índices (creciente) lexicográficamente
        menor entre todas las óptimas. Requiere valores ≥ 1.

IDEA Y ALGORITMO
    Corte de varilla (DP base):
      ESTADO      dp[x] = mejor valor cortando una varilla de largo x.
      TRANSICIÓN  la primera pieza mide l: dp[x] = max_{1≤l≤min(x,L)}
                  precio[l] + dp[x - l].
      CASO BASE   dp[0] = 0.   ORDEN  x creciente.   RESPUESTA  dp[n].
    Método A — GUARDAR LA DECISIÓN: al calcular dp[x], anotar en corte[x]
      el l que dio el máximo. Después: x = n; mientras x > 0: pieza
      corte[x], x -= corte[x]. Cuesta memoria extra del tamaño de la tabla
      pero la reconstrucción es directa.
    Método B — RETROCEDER SOBRE LA TABLA: no se guarda nada extra. Estando
      en x, se busca un l con precio[l] + dp[x - l] == dp[x] (una transición
      que «explica» el óptimo) y se pasa a x - l. Funciona porque dp[x - l]
      es óptimo para el resto: seguir desde ahí siempre llega a una solución
      completa óptima. Ahorra memoria y permite elegir entre empates.
    Método C — LEXICOGRÁFICAMENTE MENOR: para decidir de ADELANTE hacia
      atrás (primero el elemento más importante para el orden), la DP debe
      estar definida sobre lo que FALTA (el sufijo):
        ESTADO      suf[i][c] = mejor valor usando solo objetos i..n-1 con
                    capacidad c.
        TRANSICIÓN  suf[i][c] = max(suf[i+1][c], v_i + suf[i+1][c - p_i]).
        CASO BASE   suf[n][c] = 0.  ORDEN  i decreciente.  RESPUESTA suf[0][W].
      Reconstrucción: para i = 0, 1, …: si TOMAR i todavía permite el
      óptimo (p_i ≤ c y v_i + suf[i+1][c - p_i] == suf[i][c]), tomarlo.
      Tomar el índice menor posible hace la lista lexicográficamente menor
      (cualquier lista óptima que no incluya i empieza con algo > i). Con una
      DP sobre prefijos no se puede: al retroceder se decide primero el
      ÚLTIMO índice, que es el menos importante para el orden.
      (Con valores 0 un objeto inútil podría tomarse o no y la lista con
      menos elementos sería «menor»; por eso se piden valores ≥ 1.)

MACROALGORITMO
    1. Llenar la DP normalmente (y, en el método A, guardar la decisión).
    2. Partir del estado de la respuesta.
    3. A: seguir la decisión guardada. B/C: probar las transiciones y
       quedarse con una cuyo valor coincida exactamente con dp del estado.
    4. Pasar al subproblema elegido; repetir hasta el caso base.
    5. Si se recogió al revés, invertir.

COMPLEJIDAD
    La reconstrucción cuesta (largo de la solución) × (transiciones por
    estado), despreciable frente a llenar la tabla. Corte: O(n·L).
    Mochila: O(n·W) tiempo y memoria (la tabla completa hace falta).

EJEMPLO A MANO
    precio[1..8] = [1, 5, 8, 9, 10, 17, 17, 20], n = 8:
      dp: x=1:1 2:5 3:8 4:10 5:13 6:17 7:18 8:22
    Método B en x = 8: l=1: 1+18=19; l=2: 5+17=22 ✓ -> x = 6;
      l=6: 17+0 = 17 ✓ (l=1..5 no dan 17) -> piezas [2, 6], valor 22.
    Mochila: pesos [2, 2, 3], valores [3, 3, 3], W = 4: óptimos {0,1}
      (valor 6). suf[0][4] = 6; tomar 0: 3 + suf[1][2] = 3 + 3 = 6 ✓;
      tomar 1: 3 + suf[2][0] = 3 ✓ -> [0, 1].

ERRORES TÍPICOS
    - Retroceder comparando con el valor equivocado (dp de otro estado o
      sin el costo de la transición).
    - Comparar flotantes con == al retroceder: usar enteros o tolerancia
      (o mejor, guardar la decisión).
    - Buscar la solución lexicográficamente menor con una DP sobre
      prefijos (hay que invertir el sentido de la DP).
    - Ahorrar memoria (una sola fila) y después querer reconstruir.

VARIANTES Y RELACIONADOS
    - lcs.py, distancia_edicion.py, caminos_grilla.py, lis.py (previo[]),
      dp_intervalos.py (guardar el corte k), dp_mascaras.py (padre en TSP).
    - k-ésima solución en orden lexicográfico: DP que CUENTA soluciones por
      sufijo y luego se baja eligiendo la rama según el conteo.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/E - Custom Keypad (DP de partición + reconstrucción
      voraz con desempate, eligiendo los separadores desde la derecha).
    - Externos: UVa 526 «String Distance and Transform Process»; UVa 531
      «Compromise».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (todas las composiciones de n ≤ 11 para
      el corte; todos los subconjuntos para la mochila, tomando la lista
      mínima con min() de Python) en 400 + 400 casos aleatorios + casos borde
      (python reconstruccion_solucion.py)
"""
import random


def _tabla_corte(precio, n):
    L = len(precio) - 1
    dp = [0] * (n + 1)
    corte = [0] * (n + 1)
    for x in range(1, n + 1):
        mejor = -1
        for l in range(1, min(x, L) + 1):
            v = precio[l] + dp[x - l]
            if v > mejor:
                mejor, corte[x] = v, l          # método A: guardar la decisión
        dp[x] = mejor
    return dp, corte


def corte_guardando_decision(precio, n):
    """Método A: seguir el arreglo corte[] guardado al llenar la DP."""
    dp, corte = _tabla_corte(precio, n)
    piezas, x = [], n
    while x > 0:
        piezas.append(corte[x])
        x -= corte[x]
    return dp[n], piezas


def corte_retrocediendo(precio, n):
    """Método B: solo la tabla dp; en cada paso buscar una transición que explique dp[x]."""
    dp, _ = _tabla_corte(precio, n)
    L = len(precio) - 1
    piezas, x = [], n
    while x > 0:
        for l in range(1, min(x, L) + 1):
            if precio[l] + dp[x - l] == dp[x]:  # esta pieza es compatible con el óptimo
                piezas.append(l)
                x -= l
                break
    return dp[n], piezas


def mochila_lexicografica(pesos, valores, W):
    """Método C: DP sobre SUFIJOS y decisión de adelante hacia atrás."""
    n = len(pesos)
    suf = [[0] * (W + 1) for _ in range(n + 1)]   # suf[n][*] = 0: caso base
    for i in range(n - 1, -1, -1):
        p, v, sig, fila = pesos[i], valores[i], suf[i + 1], suf[i]
        for c in range(W + 1):
            fila[c] = sig[c]
            if p <= c and v + sig[c - p] > fila[c]:
                fila[c] = v + sig[c - p]
    elegidos, c = [], W
    for i in range(n):                             # el índice menor decide primero
        if pesos[i] <= c and valores[i] + suf[i + 1][c - pesos[i]] == suf[i][c]:
            elegidos.append(i)
            c -= pesos[i]
    return suf[0][W], elegidos


def demo():
    precio = [0, 1, 5, 8, 9, 10, 17, 17, 20]
    print("precio[1..8] =", precio[1:], " n = 8")
    print("A guardando la decisión ->", corte_guardando_decision(precio, 8))  # (22, [2, 6])
    print("B retrocediendo         ->", corte_retrocediendo(precio, 8))       # (22, [2, 6])
    print("C mochila lexicográfica ->", mochila_lexicografica([2, 2, 3], [3, 3, 3], 4))  # (6, [0, 1])


def pruebas():
    random.seed(531)

    def composiciones(n):
        """Todas las listas de enteros positivos que suman n (cortes por máscara)."""
        if n == 0:
            yield []
            return
        for mask in range(1 << (n - 1)):
            piezas, largo = [], 1
            for b in range(n - 1):
                if mask >> b & 1:
                    piezas.append(largo)
                    largo = 1
                else:
                    largo += 1
            piezas.append(largo)
            yield piezas

    # Casos borde
    assert corte_guardando_decision([0, 3], 0) == (0, [])
    assert corte_retrocediendo([0, 3], 5) == (15, [1] * 5)
    assert mochila_lexicografica([], [], 3) == (0, [])
    assert mochila_lexicografica([5], [1], 4) == (0, [])

    for _ in range(400):
        L = random.randint(1, 6)
        precio = [0] + [random.randint(0, 12) for _ in range(L)]
        n = random.randint(0, 11)
        mejor = max(sum(precio[l] for l in p) for p in composiciones(n) if max(p, default=0) <= L)
        for f in (corte_guardando_decision, corte_retrocediendo):
            valor, piezas = f(precio, n)
            assert valor == mejor
            assert sum(piezas) == n and all(1 <= l <= L for l in piezas)
            assert sum(precio[l] for l in piezas) == valor

    for _ in range(400):
        n = random.randint(0, 9)
        pesos = [random.randint(1, 6) for _ in range(n)]
        valores = [random.randint(1, 4) for _ in range(n)]      # pocos valores: muchos empates
        W = random.randint(0, 15)
        mejor, mejor_lista = -1, None
        for mask in range(1 << n):
            idx = [i for i in range(n) if mask >> i & 1]
            if sum(pesos[i] for i in idx) <= W:
                v = sum(valores[i] for i in idx)
                if v > mejor or (v == mejor and idx < mejor_lista):
                    mejor, mejor_lista = v, idx
        assert mochila_lexicografica(pesos, valores, W) == (mejor, mejor_lista)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
