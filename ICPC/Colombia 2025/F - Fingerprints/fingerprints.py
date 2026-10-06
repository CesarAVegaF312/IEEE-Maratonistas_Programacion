"""
Colombia 2025 — F: Fingerprints («Huellas dactilares»)
Ejecutar: python fingerprints.py < fingerprints.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una base de datos forense guarda huellas como cadenas circulares: ABCD,
    BCDA, CDAB y DABC son la misma huella. Para ahorrar espacio se quiere
    guardar una sola copia por huella, usando como representante canónico su
    rotación lexicográficamente mínima.

QUÉ HAY QUE HACER
    Entrada: varios casos; cada uno empieza con N y siguen N líneas "M F"
             (M = |F|, F en mayúsculas). Una línea con 0 termina la entrada.
    Salida:  por caso, las codificaciones canónicas de las huellas distintas,
             una por línea, en el orden de su primera aparición.
    Restricciones clave: N ≤ 100, M ≤ 5 000.

IDEA Y ALGORITMO
    Rotación lexicográficamente mínima con el ALGORITMO DE BOOTH / "dos
    punteros" (también llamado algoritmo de la mínima representación) en O(M):
      - Se trabaja sobre s+s implícito (índices módulo M) con dos candidatos
        de inicio i < j y un desfase k ya comparado.
      - Si s[i+k] == s[j+k], se avanza k.
      - Si s[i+k] > s[j+k], ninguna rotación que empiece en i, i+1, ..., i+k
        puede ser la mínima (cada una pierde contra la que empieza en la
        posición correspondiente desde j), así que i salta a i+k+1.
        Simétrico si s[j+k] > s[i+k].
      - Si i == j se mueve j una posición. Termina cuando un puntero pasa M o
        k llega a M (todas las rotaciones restantes son iguales).
      El mínimo es min(i, j). Cada comparación hace avanzar i+j+k, por eso es
      lineal.
    Dos huellas son la misma si y solo si sus representaciones canónicas son
    iguales (rotación mínima = invariante completo bajo rotaciones).
    Luego se eliminan duplicados conservando el orden con un conjunto "vistos".
    El enfoque ingenuo (generar las M rotaciones y tomar el mínimo) es O(M²)
    por huella: 2.5·10^7 caracteres copiados por huella, demasiado en Python
    con 100 huellas por caso.

MACROALGORITMO
    1. Leer N; si es 0, terminar.
    2. Para cada una de las N huellas, calcular su rotación mínima (Booth).
    3. Recorrer las canónicas en orden; imprimir cada una la primera vez que
       aparece (conjunto de vistas).

COMPLEJIDAD
    Tiempo O(Σ M) por caso, memoria O(Σ M).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/F")
    - Fuerza bruta (min de todas las rotaciones s[i:]+s[:i]): OK en ~1600
      cadenas aleatorias con alfabeto pequeño (muchos empates/periodos).
    - Caso grande (20 casos × 100 huellas × M = 5 000, alfabeto {A,B}): ~3 s
      (≈0.15 s por caso de tamaño máximo).
"""
import sys


def rotacion_minima(s):
    """Rotación lexicográficamente mínima de s en O(len(s))."""
    m = len(s)
    i, j, k = 0, 1, 0
    while i < m and j < m and k < m:
        a = s[(i + k) % m]
        b = s[(j + k) % m]
        if a == b:
            k += 1
            continue
        if a > b:
            # Las rotaciones que empiezan en i..i+k pierden: saltarlas.
            i += k + 1
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    inicio = min(i, j)
    return s[inicio:] + s[:inicio]


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos])
        pos += 1
        if n == 0:  # fin de la entrada
            break
        vistos = set()
        for _ in range(n):
            # Cada huella viene como "M F"; M es redundante (M = |F|).
            huella = datos[pos + 1].decode()
            pos += 2
            canonica = rotacion_minima(huella)
            if canonica not in vistos:
                vistos.add(canonica)
                salida.append(canonica)
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
