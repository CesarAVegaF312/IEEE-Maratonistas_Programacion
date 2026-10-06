"""
OMP 2017 Murcia — E: Prime Darts («Dardos primos»)
Ejecutar: python primedarts.py < primedarts.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un fabricante diseña "dianas primas": una diana con n áreas tiene un área
    que vale 1 punto y n-1 áreas que valen los primeros n-1 números primos
    (2, 3, 5, 7, …). Cada dardo suma el valor del área donde cae.

QUÉ HAY QUE HACER
    Entrada: t casos; cada uno "n q" (áreas de la diana y puntuación pedida).
    Salida:  una línea por caso con el mínimo número de dardos que suman
    exactamente q puntos.
    Restricciones clave: 1 ≤ n ≤ 100, 1 ≤ q ≤ 5000 (el enunciado escribe
    "1 ≤ k ≤ 5000"; se refiere a q). Como siempre existe el área de 1 punto,
    toda q es alcanzable (q dardos de 1).

IDEA Y ALGORITMO
    Problema del cambio de monedas (coin change) con mínimo número de
    monedas, monedas ilimitadas: DP clásica
        mejor[x] = min(mejor[x], mejor[x - c] + 1)  para cada moneda c.
    Hacer esa DP desde cero en cada caso cuesta O(n·q) ≈ 5·10^5 operaciones
    por caso; con muchos casos sería lento en Python. Observación: la diana
    de tamaño n tiene las MISMAS monedas que la de tamaño n-1 más un primo
    nuevo. La DP de mochila ilimitada se puede extender moneda a moneda (el
    orden en que se añaden las monedas no cambia el óptimo), así que se
    construyen incrementalmente las 100 tablas (una por n) UNA sola vez:
    tabla[n] = tabla[n-1] relajada con el primo n-1. Total 100·5000 = 5·10^5
    actualizaciones, y luego cada consulta es O(1).
    Por qué la relajación en orden creciente de x permite reusar la moneda
    nueva varias veces: al procesar x, mejor[x - c] ya puede incluir la
    moneda c (se actualizó antes en el mismo barrido) → mochila ilimitada.

MACROALGORITMO
    1. Generar los primeros 99 primos (criba hasta 600; el primo 99 es 523).
    2. tabla_1[x] = x (solo hay área de 1 punto).
    3. Para n = 2..100: copiar tabla_{n-1} y relajarla con la moneda p_{n-1}
       recorriendo x de p a QMAX en orden creciente.
    4. Para cada caso (n, q) imprimir tabla_n[q].

COMPLEJIDAD
    Precálculo O(100·5000) tiempo y memoria (100 listas de 5001 enteros).
    Cada caso O(1). Caso grande (100 000 consultas): ~0.2 s en total.

EJEMPLO A MANO
    n = 5 → áreas {1, 2, 3, 5, 7}. q = 15 → 5+5+5 (3 dardos; con 2 dardos el
    máximo es 14). q = 34 → 7·4 + 5 + 1 = 34 son 6 dardos. Con 5 dardos no
    se puede: 4 sietes exigirían un 6 (no existe) y con 3 sietes faltan 13
    con dos dardos ≤ 5 (máximo 10). La DP da 6.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/E")
    - Fuerza bruta: OK en 500 casos aleatorios (n ≤ 100, q ≤ 400) contra una
      BFS independiente sobre las sumas parciales (cada arista = un dardo).
"""
import sys

MAX_AREAS = 100
MAX_PUNTOS = 5000


def primeros_primos(cuantos):
    """Criba de Eratóstenes; devuelve los primeros `cuantos` primos."""
    limite = 600  # el primo número 99 es 523, así que 600 sobra
    es_primo = bytearray([1]) * (limite + 1)
    es_primo[0] = es_primo[1] = 0
    for i in range(2, int(limite ** 0.5) + 1):
        if es_primo[i]:
            es_primo[i * i::i] = bytearray(len(es_primo[i * i::i]))
    primos = [i for i in range(limite + 1) if es_primo[i]]
    return primos[:cuantos]


def construir_tablas():
    """tablas[n][x] = mínimo de dardos para sumar x con una diana de n áreas."""
    primos = primeros_primos(MAX_AREAS - 1)
    tablas = [None] * (MAX_AREAS + 1)
    # n = 1: solo existe el área de 1 punto → hacen falta x dardos.
    actual = list(range(MAX_PUNTOS + 1))
    tablas[1] = actual
    for n in range(2, MAX_AREAS + 1):
        c = primos[n - 2]        # moneda nueva que aporta la diana de tamaño n
        actual = actual[:]       # se copia para no estropear la tabla anterior
        # Relajación en orden creciente: permite usar la moneda c varias veces.
        for x in range(c, MAX_PUNTOS + 1):
            candidato = actual[x - c] + 1
            if candidato < actual[x]:
                actual[x] = candidato
        tablas[n] = actual
    return tablas


def main():
    datos = sys.stdin.buffer.read().split()
    t = int(datos[0])
    tablas = construir_tablas()
    salida = []
    for k in range(t):
        n = int(datos[1 + 2 * k])
        q = int(datos[2 + 2 * k])
        salida.append(str(tablas[n][q]))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
