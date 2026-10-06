"""
Colombia 2023 — B: Be Strong («Sé fuerte»)
Ejecutar: python be.py < be.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    El "prefijo fuerte" de una colección de palabras es el prefijo común más
    largo de todas ellas, sin distinguir mayúsculas de minúsculas.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno empieza con M y siguen M palabras (letras
             inglesas mayúsculas/minúsculas, 1 ≤ |W| ≤ 200). Termina con M = 0.
    Salida:  por caso, el prefijo fuerte en minúsculas, o '*' si es vacío.
    Restricciones clave: M ≤ 5000, |W| ≤ 200.

IDEA Y ALGORITMO
    Prefijo común más largo (LCP) por reducción: se pasa todo a minúsculas
    (así las mayúsculas dejan de importar) y se mantiene un prefijo candidato
    que se va recortando contra cada palabra. Es correcto porque el LCP de
    un conjunto es LCP(LCP(w1..wi), w(i+1)): el prefijo común de todos solo
    puede acortarse al agregar palabras.
    Atajo equivalente: el LCP de todo el conjunto es el LCP entre la menor y
    la mayor palabra en orden lexicográfico (todas las demás quedan "entre"
    ellas). Se usa la reducción directa, que es más fácil de seguir.

MACROALGORITMO
    1. Leer M; si es 0, terminar.
    2. Leer las M palabras y pasarlas a minúsculas.
    3. Prefijo = primera palabra.
    4. Para cada palabra siguiente, recortar el prefijo hasta la primera
       posición donde difieran.
    5. Imprimir el prefijo, o '*' si quedó vacío.

COMPLEJIDAD
    Tiempo O(suma de longitudes) por caso, memoria O(suma de longitudes).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2023/B")
    - Fuerza bruta: comparada con os.path.commonprefix sobre palabras en
      minúsculas en 500 casos aleatorios (alfabeto pequeño aA bB): OK.
"""
import sys


def prefijo_comun(palabras):
    """LCP de una lista no vacía de palabras ya en minúsculas."""
    prefijo = palabras[0]
    for w in palabras[1:]:
        # Recortamos el prefijo a la parte que coincide con w.
        limite = min(len(prefijo), len(w))
        i = 0
        while i < limite and prefijo[i] == w[i]:
            i += 1
        prefijo = prefijo[:i]
        if not prefijo:
            break  # ya no puede crecer: vacío es definitivo
    return prefijo


def main():
    datos = sys.stdin.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        m = int(datos[pos])
        pos += 1
        if m == 0:
            break
        palabras = [w.lower() for w in datos[pos:pos + m]]
        pos += m
        p = prefijo_comun(palabras)
        salida.append(p if p else "*")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
