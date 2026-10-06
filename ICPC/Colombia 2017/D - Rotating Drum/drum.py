"""
Colombia 2017 — D: Rotating Drum («El tambor giratorio»)
Ejecutar: python drum.py < drum.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una banda quiere pintar su bombo dividido en m secciones (como una pizza)
    con k colores, de modo que toda secuencia de n colores aparezca
    exactamente una vez leyendo en sentido horario. El músico "Nick De
    Bruijn" sabe que m = k^n (k >= 2) o m = n (k = 1).

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF; cada uno "k n".
    Salida:  por caso, la secuencia circular (letras 'A'..) que sea la
             PRIMERA en orden lexicográfico entre todas las soluciones.
    Restricciones clave: 1 <= k <= 26, 1 <= n <= 10, m <= 10^5.

IDEA Y ALGORITMO
    Es una SECUENCIA DE DE BRUIJN B(k, n). La menor lexicográficamente se
    obtiene con el algoritmo de Fredricksen–Kessler–Maiorana (FKM):
    concatenar, en orden lexicográfico, todas las PALABRAS DE LYNDON sobre el
    alfabeto de k símbolos cuya longitud divide a n. (Teorema de Fredricksen y
    Maiorana: esa concatenación es una secuencia de De Bruijn y además es la
    menor lexicográficamente.) Ejemplo k=2, n=3: Lyndon de longitud 1 ó 3 en
    orden: 0, 001, 011, 1 -> 0 001 011 1 = AAABABBB, igual al ejemplo.
    Las palabras de Lyndon se generan en orden con el algoritmo de Duval
    (siguiente palabra de Lyndon de longitud <= n), que es iterativo:
        w <- repetir w hasta longitud n; quitar los símbolos máximos del final;
        incrementar el último símbolo.
    Caso especial k = 1: la "secuencia" es n veces 'A' (m = n según el
    enunciado), que es lo que ya pide el ejemplo "1 5 -> AAAAA".

MACROALGORITMO
    1. Leer k y n.
    2. Si k = 1, imprimir 'A' * n.
    3. Si no, generar con Duval las palabras de Lyndon de longitud <= n en
       orden lexicográfico, empezando por [0].
    4. Concatenar sólo las de longitud que divide a n.
    5. Traducir 0.. k-1 a 'A'.. y imprimir.

COMPLEJIDAD
    Tiempo O(n * k^n): se generan O(k^n) palabras de Lyndon y cada paso de
    Duval cuesta O(n); como k^n <= 10^5 y n <= 10 son ~10^6 operaciones.
    Memoria O(k^n).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/D")
    - Fuerza bruta: OK en los 82 pares (k, n) con k^n <= 1024 (k >= 2) más
      todos los k = 1: búsqueda con retroceso en orden lexicográfico que
      construye la primera cadena circular de longitud k^n con cada palabra
      exactamente una vez; y cuando era factible (k^(k^n) <= 2*10^5) también
      con enumeración total de todas las cadenas.
    - Rendimiento: los casos más grandes (10 5, 17 4, 4 8, 3 10, 6 6, ...)
      juntos tardan 0.13 s y se comprobó que son De Bruijn válidas.
"""
import sys


def de_bruijn_minima(k, n):
    """Secuencia de De Bruijn lexicográficamente mínima (lista de 0..k-1)."""
    resultado = []
    w = [0]                      # palabra de Lyndon actual
    while w:
        if n % len(w) == 0:
            resultado.extend(w)
        # Algoritmo de Duval: siguiente palabra de Lyndon de longitud <= n.
        m = len(w)
        while len(w) < n:        # repetir la palabra periódicamente hasta n
            w.append(w[len(w) - m])
        while w and w[-1] == k - 1:   # quitar símbolos máximos del final
            w.pop()
        if w:
            w[-1] += 1
    return resultado


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for p in range(0, len(datos) - 1, 2):
        k, n = int(datos[p]), int(datos[p + 1])
        if k == 1:
            salida.append("A" * n)
            continue
        letras = [chr(ord("A") + i) for i in range(k)]
        salida.append("".join(letras[c] for c in de_bruijn_minima(k, n)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
