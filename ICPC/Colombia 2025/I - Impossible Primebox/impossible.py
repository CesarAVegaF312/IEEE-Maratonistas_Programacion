"""
Colombia 2025 — I: Impossible Primebox («La Primebox imposible»)
Ejecutar: python impossible.py < impossible.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Danny O'sea quiere abrir la Primebox: L "cerrojos primos", cada uno un
    mini-programa  x = x*A + B ;  si P divide a x salta a j (o termina), si no
    salta a m (o termina). Se arranca en el cerrojo 0 con un x inicial ≥ 0.
    La caja se abre si cada cerrojo i se ejecuta EXACTAMENTE K_i veces antes
    de terminar. La clave es el menor x inicial que lo logra (existe y es
    < 50 000).

QUÉ HAY QUE HACER
    Entrada: varios casos: L, luego 3·L líneas con el código de los cerrojos
             ("prlck i:", "x = x [* A] [+ B]", "if P div x jumpto {prlck j|end}
             else jumpto {prlck m|end}") y una línea con K_0..K_{L-1}.
             Un L = 0 termina. Las partes "* A" y "+ B" son opcionales.
    Salida:  por caso, la clave.
    Restricciones clave: L ≤ 10, A, B, P ≤ 1000 (P primo), K_i ≤ 1000
             (≤ 10 000 ejecuciones en total), clave < 50 000.
             (El enunciado dice "enteros positivos" pero escribe 0 ≤ A, B: se
             acepta A = 0 o B = 0 sin problema.)

IDEA Y ALGORITMO
    La idea base es la fuerza bruta que sugiere el enunciado: probar
    x0 = 0, 1, 2, … y simular hasta que algún cerrojo se pase de K_i o se
    llegue a "end". Pero cada simulación puede durar ΣK ≈ 10^4 pasos y la
    clave puede rondar 5·10^4: 5·10^8 pasos, inviable en Python. Tres ideas:

    1) Solo importa x MÓDULO M = producto de los primos distintos: x solo se
       usa en pruebas "P divide a x" y se transforma con x·A + B (que respeta
       congruencias). Además, dos x0 con el mismo resto mod M se comportan
       igual, así que basta probar x0 < M (si M es chico, se prueban pocos).

    2) MACRO-PASOS sobre la "cadena del no". Desde un cerrojo i, mientras las
       pruebas fallen, el camino es FIJO: i → m_i → m_{m_i} → …  A lo largo
       de esa cadena, tras k pasos  x_k = α_k·x + β_k (mod M)  con α_k, β_k
       precalculados. El paso k "dispara" (P | x_k, con P el primo del
       cerrojo ejecutado) si y solo si
           α_k ≡ 0 (mod P):  β_k ≡ 0  (siempre o nunca, sin importar x);
           si no:            x ≡ ρ_k = −β_k·α_k⁻¹ (mod P)  (UN residuo).
       Se precalcula, por cerrojo inicial i y primo q, un diccionario
       residuo → primer k que dispara. Entonces, dado x, el primer disparo
       desde i es  mín_q primero[i][q][x mod q]  (≤ 10 consultas) en vez de
       simular paso a paso. También se precalcula en qué paso la cadena llega
       a "end" por la rama del no, y los contadores acumulados pre[k] (visitas
       a cada cerrojo en los pasos 1..k), para sumar un tramo entero de golpe.
       Si tras sumar el tramo hasta el evento algún contador supera K, el
       exceso ocurrió en un paso ≤ evento y por el orden de eventos (punto 3)
       la trayectoria falla.
       Cada macro-paso salta de un disparo al siguiente. Con primos grandes
       los disparos son raros (~1/P por paso) y una trayectoria de miles de
       pasos se resuelve en unos pocos macro-pasos; si todos los primos son
       chicos, los disparos son frecuentes pero M es chico y hay pocos x0.

    3) Orden de eventos dentro de un mismo paso (importa en empates): primero
       se cuenta la visita (si supera K_i → falla), luego la prueba (si
       dispara → rama "sí"), y solo si no dispara se toma la rama "no"
       (que puede ser "end").

MACROALGORITMO
    1. Leer y "parsear" los L cerrojos (A, B, P, destinos; −1 = end) y los K.
    2. M = producto de primos distintos; H = ΣK + 1 (ninguna trayectoria
       válida da más pasos).
    3. Para cada cerrojo inicial i, recorrer su cadena del "no" hasta H pasos
       o hasta "end", guardando α_k, β_k, el destino "sí" de cada paso, el
       primer disparo por (primo, residuo), disparos incondicionales,
       el paso de fin y los contadores acumulados.
    4. Para x0 = 0, 1, …, < M: estado (cerrojo, x, contadores). Repetir:
       evento = mín(primer disparo para x, fin de la cadena); sumar los
       contadores del tramo (si alguno supera K → falla); si fue fin,
       comparar con K; si fue disparo, x = α_t·x + β_t y saltar a la rama "sí".
    5. El primer x0 que termina con contadores == K es la clave.

COMPLEJIDAD
    Precálculo O(L·H) operaciones con enteros mod M (y O(L·H) tuplas de
    contadores). Luego O(#disparos · L) por x0 en vez de O(#pasos).
    Medido con L = 10, trayectorias de 4 000–10 000 pasos y clave entre
    30 000 y 50 000:
      - primos ~1000:                      0.5–1.1 s por caso (la simulación
        paso a paso tardaba 30–97 s);
      - 9 primos chicos (11..47) + 1 grande: 5–15 s por caso (los disparos
        ocurren cada ~30 pasos; paso a paso tardaba 39–50 s). Python puede
        ser lento con datos así.
    Se probó también una versión "agrupada" (simular juntos los x0 con el
    mismo camino, separándolos por residuos): resultó MÁS lenta que la fuerza
    bruta (90–260 s), porque las trayectorias se separan muy pronto.
    Peor caso teórico (disparos en casi cada paso y M > 50 000) sigue siendo
    ~5·10^8 operaciones.

EJEMPLO A MANO
    Caso 1 con x0 = 10: c0: 23, 3∤23 → c1: 93, 5∤93 → c2: 98, 7|98 → c1:
    393, 5∤ → c2: 398, 7∤398 → end. Visitas (1, 2, 2) = K ✔; ningún x0 < 10
    lo logra → 10.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/I")
    - Fuerza bruta (simular cada x0 = 0, 1, 2, … paso a paso): OK en 800
      casos aleatorios pequeños (L ≤ 4, primos chicos, A o B a veces 0 u
      omitidos, líneas con y sin espacios), en 40 casos medianos (L ≤ 10,
      primos < 200, A y B hasta 1000) y en 9 casos grandes (L = 10,
      trayectorias de 4 000–10 000 pasos, clave 30 000–50 000).
    - Rendimiento: ver COMPLEJIDAD.
"""
import sys
import re

FIN = -1          # destino "end"
INF = float("inf")

RE_ASIG = re.compile(r"^x=x(?:\*(\d+))?(?:\+(\d+))?$")
RE_SALTO = re.compile(
    r"if\s*(\d+)\s*div\s*x\s*jumpto\s*(end|prlck\s*(\d+))\s*else\s*jumpto\s*(end|prlck\s*(\d+))")


def parsear_cerrojo(linea_asig, linea_if):
    """Devuelve (A, B, P, destino_si_divide, destino_si_no)."""
    m = RE_ASIG.match(linea_asig.replace(" ", ""))
    a = int(m.group(1)) if m.group(1) is not None else 1
    b = int(m.group(2)) if m.group(2) is not None else 0
    s = RE_SALTO.search(linea_if)
    p = int(s.group(1))
    si = FIN if s.group(2) == "end" else int(s.group(3))
    no = FIN if s.group(4) == "end" else int(s.group(5))
    return a, b, p, si, no


def precalcular_cadena(i, cerrojos, M, H):
    """Recorre la cadena del 'no' desde el cerrojo i (máx. H pasos).

    Devuelve una tupla (alfa, beta, si_destino, primero, siempre, fin, pre):
      alfa[k], beta[k]: x tras k pasos = alfa[k]·x0 + beta[k] (mod M)
      si_destino[k]:    destino de la rama "sí" del cerrojo ejecutado en el
                        paso k (1-indexado)
      primero:          lista de (q, tabla) con tabla = residuo r mod q →
                        primer paso k que dispara si x0 ≡ r (mod q)
      siempre:          primer paso que dispara para cualquier x0 (o INF)
      fin:              paso en que la rama "no" lleva a end (o INF)
      pre[k]:           tupla con las visitas a cada cerrojo en los pasos 1..k
    """
    L = len(cerrojos)
    alfa, beta, si_destino = [1 % M], [0], [None]
    primero = {}
    siempre = INF
    fin = INF
    cuenta = [0] * L
    pre = [tuple(cuenta)]
    actual, a_k, b_k = i, 1 % M, 0
    for k in range(1, H + 1):
        A, B, P, si, no = cerrojos[actual]
        a_k = a_k * A % M
        b_k = (b_k * A + B) % M
        alfa.append(a_k)
        beta.append(b_k)
        si_destino.append(si)
        cuenta[actual] += 1
        pre.append(tuple(cuenta))
        ap, bp = a_k % P, b_k % P
        if ap == 0:
            if bp == 0 and siempre == INF:
                siempre = k  # dispara sin importar x0
        else:
            r = (-bp * pow(ap, -1, P)) % P
            tabla = primero.setdefault(P, {})
            if r not in tabla:
                tabla[r] = k  # solo interesa el PRIMER disparo
        if no == FIN:
            fin = k  # si en este paso no dispara, se termina
            break
        actual = no
    return alfa, beta, si_destino, list(primero.items()), siempre, fin, pre


def abre_la_caja(x0, K, cadenas, M):
    """¿El x0 dado ejecuta cada cerrojo exactamente K_i veces?"""
    cont = (0,) * len(K)
    lock, x = 0, x0 % M
    while True:
        alfa, beta, si_destino, primero, siempre, t_fin, pre = cadenas[lock]
        # Primer paso que dispara para este x (una consulta por primo).
        t_disp = siempre
        for q, tabla in primero:
            t = tabla.get(x % q)
            if t is not None and t < t_disp:
                t_disp = t
        t = t_disp if t_disp <= t_fin else t_fin  # primer evento
        if t == INF:
            # La cadena se cortó a los H pasos sin eventos: seguro se pasa.
            return False
        # Contadores tras los pasos 1..t. Si alguno supera K, el exceso
        # ocurrió en un paso ≤ t, y el conteo va antes que la prueba: falla.
        cont = tuple(map(int.__add__, cont, pre[t]))
        if any(map(int.__gt__, cont, K)):
            return False
        if t_disp > t_fin:
            return cont == K  # no disparó y la rama "no" era end
        # Disparó en el paso t: x avanza en bloque y se toma la rama "sí".
        x = (alfa[t] * x + beta[t]) % M
        lock = si_destino[t]
        if lock == FIN:
            return cont == K


def resolver(cerrojos, K):
    M = 1
    for p in {c[2] for c in cerrojos}:
        if p > 1:
            M *= p
    K = tuple(K)
    H = sum(K) + 1  # tras H pasos algún contador ya se pasó seguro
    cadenas = [precalcular_cadena(i, cerrojos, M, H) for i in range(len(cerrojos))]
    # x0 y x0 + M se comportan igual: basta revisar x0 < M.
    x0 = 0
    while x0 < M:
        if abre_la_caja(x0, K, cadenas, M):
            return x0
        x0 += 1
    return -1  # no debería ocurrir: el enunciado garantiza que la clave existe


def main():
    lineas = [l.strip() for l in sys.stdin.read().splitlines()]
    lineas = [l for l in lineas if l]
    pos = 0
    salida = []
    while pos < len(lineas):
        L = int(lineas[pos])
        pos += 1
        if L == 0:
            break
        cerrojos = []
        for _ in range(L):
            # lineas[pos] es "prlck i:" (los cerrojos vienen en orden)
            cerrojos.append(parsear_cerrojo(lineas[pos + 1], lineas[pos + 2]))
            pos += 3
        K = [int(v) for v in lineas[pos].split()]
        pos += 1
        salida.append(str(resolver(cerrojos, K)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
