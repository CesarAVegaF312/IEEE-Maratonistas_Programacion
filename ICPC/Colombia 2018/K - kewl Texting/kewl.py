"""
Colombia 2018 — K: kewl Texting («Mensajes de texto kewl»)
Ejecutar: python kewl.py < kewl.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Alicia y Roberto arman un «modelo de lenguaje» de bigramas con sus
    mensajes pasados: para cada palabra w se sugiere la palabra w' que más
    veces la siguió. Quieren saber qué frase sale si siempre se acepta la
    sugerencia, empezando desde el inicio de mensaje.

QUÉ HAY QUE HACER
    Entrada: varios casos hasta fin de archivo. Cada caso: n y n líneas
             (mensajes de palabras en minúsculas).
    Salida:  la frase generada (palabras separadas por un espacio) o
             «INFINITE» si el proceso nunca llega al fin de mensaje.
    Restricciones clave: ≤ 10^5 palabras en total, cada una ≤ 20 letras.

IDEA Y ALGORITMO
    Conteo de bigramas con diccionarios + recorrido de un grafo funcional.
    - Cada mensaje w1..wl se ve como {start} w1 ... wl {end}. Se cuentan:
        sig[w][w'] = cuántas veces w' aparece justo después de w,
        total[w]   = cuántas veces aparece w en todos los textos.
      {start} y {end} se tratan como palabras más: aparecen una vez por
      mensaje (total = n). (El enunciado no dice explícitamente su «total»;
      ésta es la interpretación natural de «también se consideran palabras».)
    - Sugerencia de w = máximo de sig[w] según la clave
        (más veces después de w, más veces en total, menor lexicográfico),
      con el orden lexicográfico especial {start} < {end} < palabras. Se
      implementa con la tupla (-sig, -total, rango, palabra), rango 0/1/2.
    - Cada palabra tiene exactamente una sugerencia → grafo funcional
      (cada nodo tiene una sola arista de salida). Desde {start} se sigue la
      cadena: o llega a {end} (frase finita) o entra en un ciclo. Un ciclo se
      detecta en cuanto se repite una palabra ya visitada: a partir de ahí
      la secuencia es periódica y nunca termina → INFINITE.

MACROALGORITMO
    1. Leer n y los n mensajes del caso.
    2. Recorrer cada mensaje con los marcadores {start}/{end}, sumando
       total[] y sig[][].
    3. Para cada palabra calcular su sugerencia (mínimo con la clave).
    4. Partir de {start}; repetir: w = sugerencia(w).
    5. Si w es {end} → imprimir las palabras recogidas.
    6. Si w ya se visitó → imprimir INFINITE.

COMPLEJIDAD
    Tiempo O(P) por caso (P = número de palabras), memoria O(P). Un caso
    de 10 000 mensajes × 10 palabras más otro de un mensaje con 99 999
    palabras distintas: ~0.4 s.

EJEMPLO A MANO
    Caso 3: «a rose is a rose». start→a, a→rose (2 veces), rose→is/{end}
    (1 y 1; total: is=1, {end}=1 → empate → {end} va primero
    lexicográficamente) → «a rose».

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/K")
    - Fuerza bruta: OK en 500 casos aleatorios pequeños contra una versión
      que, para cada palabra, recuenta los bigramas recorriendo todos los
      mensajes y ordena candidatos con un comparador explícito.
"""
import sys
from collections import defaultdict

INICIO = "{start}"
FIN = "{end}"


def rango(palabra):
    """{start} < {end} < cualquier palabra normal en el orden lexicográfico."""
    if palabra == INICIO:
        return 0
    if palabra == FIN:
        return 1
    return 2


def resolver(mensajes):
    total = defaultdict(int)
    sig = defaultdict(lambda: defaultdict(int))
    for palabras in mensajes:
        secuencia = [INICIO] + palabras + [FIN]
        for w in secuencia:
            total[w] += 1
        for a, b in zip(secuencia, secuencia[1:]):
            sig[a][b] += 1

    def sugerencia(w):
        # Mínimo según (más seguidas, más total, orden lexicográfico especial).
        return min(sig[w].items(),
                   key=lambda par: (-par[1], -total[par[0]], rango(par[0]), par[0]))[0]

    frase = []
    visitadas = {INICIO}
    w = INICIO
    while True:
        w = sugerencia(w)
        if w == FIN:
            return " ".join(frase)
        if w in visitadas:
            return "INFINITE"   # se repitió una palabra: ciclo sin fin
        visitadas.add(w)
        frase.append(w)


def main():
    # Leemos por líneas: cada línea es un mensaje. Se ignoran líneas vacías.
    lineas = [l.split() for l in sys.stdin.read().split("\n")]
    lineas = [l for l in lineas if l]
    salida = []
    i = 0
    while i < len(lineas):
        n = int(lineas[i][0])
        i += 1
        mensajes = lineas[i:i + n]
        i += n
        salida.append(resolver(mensajes))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
