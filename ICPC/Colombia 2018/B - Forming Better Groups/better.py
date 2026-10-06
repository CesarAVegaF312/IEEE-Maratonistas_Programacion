"""
Colombia 2018 — B: Forming Better Groups («Formando mejores grupos»)
Ejecutar: python better.py < better.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    El profesor Smith quiere evitar que los perezosos se cuelguen de los
    trabajadores: sólo permite grupos de 3 cuyas notas previas difieran a lo
    sumo en un umbral D (máx − mín ≤ D), y quiere saber cuántas opciones
    tienen sus estudiantes para formar los grupos.

QUÉ HAY QUE HACER
    Entrada: varios casos «N D» + N notas, hasta «0 0».
    Salida:  el número de formas de repartir a los N estudiantes en N/3
             grupos de 3 (grupos sin orden, estudiantes distinguibles) tales
             que cada grupo cumpla máx − mín ≤ D.
    Restricciones clave: N ≤ 21 (múltiplo de 3), notas y D ≤ 500.
             Sin restricción, el total de particiones es 21!/(3!^7·7!) ≈
             3.6·10^10: no se pueden enumerar; con N ≤ 21 cabe una DP sobre
             subconjuntos (2^21 ≈ 2·10^6).

IDEA Y ALGORITMO
    DP SOBRE MÁSCARAS DE BITS con «elemento más bajo libre» (técnica clásica
    para contar particiones sin contar dos veces el mismo reparto).
    - Se ordenan las notas. Estado: máscara de estudiantes ya agrupados.
    - Para no contar la misma partición en distinto orden, el siguiente
      grupo SIEMPRE contiene al estudiante libre de menor índice i. Así cada
      partición se genera exactamente una vez (los grupos quedan ordenados
      por su mínimo).
    - Como las notas están ordenadas, i es el mínimo de su grupo y el máximo
      es el compañero de mayor índice k: la condición es nota[k] − nota[i]
      ≤ D. Se precalculan, para cada i, las parejas (j, k), i < j < k, que
      cumplen eso, como máscaras de bits.
    - ways(máscara) = Σ ways(máscara ∪ {i, j, k}) sobre esas parejas libres;
      ways(todos) = 1. Memoización con diccionario.
    - Los estados alcanzables son pocos: los índices < i están todos usados,
      así que el número de máscaras visitadas es mucho menor que 2^21.

MACROALGORITMO
    1. Leer N, D y las notas; ordenarlas.
    2. Para cada i, lista de máscaras (1<<j)|(1<<k) con i<j<k y
       nota[k] − nota[i] ≤ D.
    3. ways(máscara): si está llena → 1; si no, i = menor bit libre y
       sumar ways(máscara | 1<<i | par) para cada par disjunto de la máscara.
    4. Imprimir ways(0).

COMPLEJIDAD
    Tiempo O(#estados alcanzables · N^2) en el peor caso, memoria
    O(#estados). Peor caso (N = 21, D = 500, todos compatibles): 55 405
    estados alcanzables y ~0.6 s en Python (respuesta 36 212 176 000).
    Python usa enteros grandes, así que no hay desbordamiento.

EJEMPLO A MANO
    6 3, notas 1..6: el grupo de 1 puede ser {1,2,3}, {1,2,4} o {1,3,4}; sus
    complementos {4,5,6}, {3,5,6} sirven y {2,5,6} no (6−2 > 3) → 2.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/B")
    - Fuerza bruta: OK en 600 casos aleatorios (N ≤ 12) contra la
      enumeración de todas las asignaciones de etiquetas de grupo
      (canónicas) a cada estudiante.
"""
import sys


def contar_formas(n, d, notas):
    notas = sorted(notas)
    lleno = (1 << n) - 1
    # parejas[i]: compañeros válidos (j, k) para el estudiante i como mínimo.
    parejas = []
    for i in range(n):
        lista = []
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if notas[k] - notas[i] <= d:
                    lista.append((1 << j) | (1 << k))
        parejas.append(lista)

    memo = {lleno: 1}

    def ways(mascara):
        # Recursión de profundidad ≤ N/3 = 7: no hay problema de pila.
        if mascara in memo:
            return memo[mascara]
        libres = ~mascara & lleno
        i = (libres & -libres).bit_length() - 1   # menor estudiante libre
        nueva = mascara | (1 << i)
        total = 0
        for par in parejas[i]:
            if not (par & mascara):
                total += ways(nueva | par)
        memo[mascara] = total
        return total

    return ways(0)


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        n, d = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if n == 0 and d == 0:
            break
        notas = [int(x) for x in datos[pos:pos + n]]
        pos += n
        salida.append(str(contar_formas(n, d, notas)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
