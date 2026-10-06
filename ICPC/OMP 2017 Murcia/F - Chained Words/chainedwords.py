"""
OMP 2017 Murcia — F: Chained Words («Palabras encadenadas»)
Ejecutar: python chainedwords.py < chainedwords.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una lista de "palabras encadenadas" es una secuencia donde cada palabra
    empieza con la última letra de la anterior, y además la PRIMERA empieza
    con la última letra de la ÚLTIMA (la cadena se cierra en círculo), p. ej.
    "all lions seek koala".

QUÉ HAY QUE HACER
    Entrada: número de problemas; cada uno: un entero n (2 ≤ n ≤ 200000) y
    n palabras en minúsculas (< 100 letras) separadas por cualquier cantidad
    de espacios/saltos de línea.
    Salida:  las n palabras reordenadas formando una cadena, separadas por un
    espacio; si hay varias, la lexicográficamente menor (comparando palabra
    a palabra); si no hay ninguna, "No way".
    Restricciones clave: n hasta 2·10^5 → se necesita algo casi lineal; probar
    permutaciones es impensable.

IDEA Y ALGORITMO
    Circuito euleriano (algoritmo de Hierholzer) en un multigrafo dirigido de
    26 vértices, eligiendo siempre la arista menor.
    - Cada palabra es una ARISTA dirigida de su primera letra a su última
      letra. Una cadena cerrada que usa todas las palabras una vez es
      exactamente un circuito euleriano.
    - Existe circuito euleriano ⇔ en cada letra grado de entrada = grado de
      salida y todas las aristas están en una misma componente conexa. La
      conectividad se comprueba al final: si Hierholzer no logra usar las n
      aristas, no hay circuito.
    - Lexicográficamente menor: un circuito se puede rotar para empezar por
      cualquier arista, así que la primera palabra es la menor de todas;
      el circuito arranca en su primera letra. Hierholzer con las aristas de
      cada vértice ordenadas y tomando siempre la menor disponible produce el
      circuito lexicográficamente menor (mismo argumento que en "Reconstruct
      Itinerary"): el recorrido voraz solo se aparta de la arista menor
      cuando tomarla dejaría aristas inalcanzables (Hierholzer las "empalma"
      antes, justo donde hay que tomarlas), y en ese caso pone la menor de
      las restantes. Se comprobó contra fuerza bruta (ver VERIFICACIÓN).
    - Como el espacio (' ') es menor que cualquier letra, comparar palabra a
      palabra equivale a comparar las líneas de salida como texto.
    - Implementación iterativa (pila explícita) para no desbordar la
      recursión con 2·10^5 aristas.

MACROALGORITMO
    1. Leer las palabras del problema y ordenarlas.
    2. Repartirlas (ya en orden) en las listas de salida de su primera letra;
       contar grados de entrada y salida por letra.
    3. Si alguna letra tiene entrada ≠ salida → "No way".
    4. Hierholzer iterativo desde la primera letra de la menor palabra:
       mientras el vértice de la cima tenga aristas sin usar, avanzar por la
       menor; si no, sacarlo de la pila y anotar la arista por la que se
       llegó a él.
    5. Las aristas anotadas, invertidas, son el circuito. Si no son n →
       "No way" (grafo no conexo); si no, imprimirlas.

COMPLEJIDAD
    Tiempo O(n log n · |palabra|) por el ordenamiento, el resto O(n).
    Memoria O(total de letras). Caso grande (2 problemas de n = 200000
    palabras con circuito euleriano): ~0.6 s.

EJEMPLO A MANO
    "rack car kiosk minumum atom metal lima arctic kenia": la menor es
    "arctic" (a→c). Recorrido voraz: arctic, car (c→r), rack (r→k), kenia
    (k→a, menor que kiosk), atom (a→m), metal (m→l, menor que minumum),
    lima (l→a) y se atasca en 'a' con "kiosk" (bucle k→k) y "minumum"
    (bucle m→m) sin usar. Al desapilar, Hierholzer empalma "minumum" en la
    visita a m y "kiosk" en la visita a k. Invirtiendo lo desapilado:
    "arctic car rack kiosk kenia atom minumum metal lima". Tomar "kenia"
    antes que "kiosk" era imposible: k no se vuelve a visitar y el bucle
    quedaría sin usar.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/F")
    - Fuerza bruta: OK contra probar TODAS las permutaciones y quedarse con
      la menor lista válida, en 1500 casos totalmente aleatorios (n ≤ 7,
      palabras cortas sobre 2–4 letras, con repetidas; la mayoría "No way")
      y en 1500 casos que SIEMPRE tienen cadena (n ≤ 8, generados partiendo
      un paseo cerrado aleatorio en palabras y barajándolas).
"""
import sys


def cadena_minima(palabras):
    """Devuelve la lista de palabras del circuito mínimo, o None si no existe."""
    palabras = sorted(palabras)
    n = len(palabras)
    # salidas[v] = palabras que empiezan con la letra v, en orden creciente.
    salidas = [[] for _ in range(26)]
    entrada = [0] * 26
    for w in palabras:
        salidas[ord(w[0]) - 97].append(w)
        entrada[ord(w[-1]) - 97] += 1
    # Condición de grados del circuito euleriano dirigido.
    for v in range(26):
        if len(salidas[v]) != entrada[v]:
            return None

    siguiente = [0] * 26                 # puntero a la próxima arista sin usar
    inicio = ord(palabras[0][0]) - 97    # primera letra de la menor palabra
    # Pila de (vértice, palabra por la que se llegó). La raíz no tiene palabra.
    pila_v = [inicio]
    pila_w = [None]
    circuito = []                        # aristas en orden inverso
    while pila_v:
        v = pila_v[-1]
        if siguiente[v] < len(salidas[v]):
            w = salidas[v][siguiente[v]]  # la menor arista libre de v
            siguiente[v] += 1
            pila_v.append(ord(w[-1]) - 97)
            pila_w.append(w)
        else:
            # v no tiene más aristas: se cierra su parte del circuito.
            pila_v.pop()
            w = pila_w.pop()
            if w is not None:
                circuito.append(w)
    if len(circuito) != n:
        return None                      # quedaron aristas en otra componente
    circuito.reverse()
    return circuito


def main():
    datos = sys.stdin.read().split()
    problemas = int(datos[0])
    idx = 1
    salida = []
    for _ in range(problemas):
        n = int(datos[idx])
        palabras = datos[idx + 1: idx + 1 + n]
        idx += 1 + n
        resultado = cadena_minima(palabras)
        salida.append("No way" if resultado is None else " ".join(resultado))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
