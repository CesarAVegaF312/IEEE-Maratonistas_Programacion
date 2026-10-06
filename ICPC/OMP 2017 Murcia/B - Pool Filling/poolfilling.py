"""
OMP 2017 Murcia — B: Pool Filling («Llenado de la piscina»)
Ejecutar: python poolfilling.py < poolfilling.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Hay que llenar una piscina vacía con agua a una temperatura deseada.
    Junto al borde hay una fila de jarras (numeradas desde 0), cada una con
    un volumen y una temperatura; solo se pueden vaciar jarras CONSECUTIVAS.
    Al mezclar, la temperatura es el promedio ponderado por volumen.

QUÉ HAY QUE HACER
    Entrada: número de problemas; cada uno: "capacidad objetivo", luego el
    número de jarras n y n líneas "volumen temperatura".
    Salida:  "i j" = primera y última jarra del tramo elegido, o
    "Not possible".
    Condiciones del tramo [i..j]:
        capacidad/2 ≤ V ≤ capacidad      (V = volumen total; "al menos la
                                           mitad, sin desbordar")
        |T - objetivo| ≤ 5               (T = Σ v·t / V; el original dice
                                           "hotter or warmer", se entiende
                                           más caliente o más fría)
    Se minimiza |T - objetivo|; en empate, "las jarras con los números más
    bajos": se interpreta como el menor i y, a igual i, el menor j (orden
    lexicográfico de (i, j)).
    Restricciones clave: n ≤ 3000 → hay ~4.5·10^6 tramos posibles.

IDEA Y ALGORITMO
    Sumas prefijas + enumeración de tramos con ventana por búsqueda binaria
    + comparación exacta de fracciones.
    - Con w_k = v_k·(t_k - objetivo), la desviación de un tramo es
          T - objetivo = (Σ w_k) / (Σ v_k) = D' / V,
      así que |T - objetivo| = |D'| / V. Con prefijos PW y PV, cada tramo se
      evalúa en O(1): D = |PW[j+1] - PW[i]|, V = PV[j+1] - PV[i].
    - Todo es entero: se comparan fracciones D1/V1 < D2/V2 como
      D1·V2 < D2·V1 (sin errores de coma flotante, importante para empates).
      La condición de 5 grados es D ≤ 5·V.
    - Como los volúmenes son no negativos, PV es no decreciente: para cada
      i, los finales válidos por volumen forman un intervalo contiguo de k
      (k = j+1) que se localiza con bisect. Solo se recorren esos k.
    - Recorriendo i creciente y luego k creciente y actualizando solo con
      mejora ESTRICTA, en empate queda el (i, j) lexicográficamente menor.
    No se ve una estructura que evite enumerar todos los tramos válidos
    (minimizar un cociente |suma|/suma sobre subarreglos), y n ≤ 3000 lo
    permite: O(n²) en el peor caso.

MACROALGORITMO
    1. Leer capacidad, objetivo y las jarras.
    2. Construir prefijos PV (volumen) y PW (volumen·(temp - objetivo)).
    3. Para cada inicio i: con bisect hallar el rango de k tal que
       ceil(cap/2) ≤ PV[k] - PV[i] ≤ cap.
    4. Para cada k del rango: D = |PW[k] - PW[i]|, V = PV[k] - PV[i]; si
       D ≤ 5V y D/V es estrictamente mejor que el mejor, guardar (i, k-1).
    5. Imprimir el mejor par o "Not possible".

COMPLEJIDAD
    Tiempo O(n² ) en el peor caso por problema (todos los tramos válidos),
    O(n log n + nº de tramos válidos) en general; memoria O(n).
    Como V debe estar en [cap/2, cap], no todos los tramos pueden ser
    válidos a la vez; el peor caso construido (n = 3000, una jarra enorme en
    el medio y el resto de 1 litro → ~2.25·10^6 tramos válidos) tarda
    ~0.4 s por problema; n = 3000 jarras de 1 litro (~1.1·10^6 tramos)
    ~0.25 s. Con decenas de problemas de ese tipo Python iría justo.

EJEMPLO A MANO
    Segundo problema: capacidad 100, objetivo 20, jarras (10 l, 20°),
    (66 l, 40°), (5 l, 100°). Tramos con V ∈ [50, 100]: [0..1] V=76,
    T≈37.4; [1] V=66, T=40; [1..2] V=71, T≈44.2; [0..2] V=81, T≈41.2.
    Todos se alejan más de 5 grados de 20 → "Not possible".

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "OMP 2017/B")
    - Fuerza bruta: OK en 1000 casos aleatorios pequeños (n ≤ 12, volúmenes
      y temperaturas pequeñas para provocar empates) contra la enumeración
      literal de todos los (i, j) con Fraction y el criterio de desempate
      lexicográfico.
"""
import sys
from bisect import bisect_left, bisect_right


def resolver(capacidad, objetivo, jarras):
    n = len(jarras)
    # Prefijos: pv[k] = volumen de las k primeras jarras;
    #           pw[k] = Σ v·(t - objetivo) de las k primeras jarras.
    pv = [0] * (n + 1)
    pw = [0] * (n + 1)
    for idx, (v, t) in enumerate(jarras):
        pv[idx + 1] = pv[idx] + v
        pw[idx + 1] = pw[idx] + v * (t - objetivo)

    minimo_volumen = (capacidad + 1) // 2   # V ≥ cap/2  ⇔  V ≥ ceil(cap/2)
    mejor_d, mejor_v = 5, 1                 # cota: desviación máxima 5 grados
    encontrado = False
    mejor_par = None

    for i in range(n):
        vi, wi = pv[i], pw[i]
        # Rango de k = j+1 (k > i) con minimo_volumen ≤ pv[k]-vi ≤ capacidad.
        desde = max(i + 1, bisect_left(pv, vi + minimo_volumen))
        hasta = bisect_right(pv, vi + capacidad)   # exclusivo
        for k in range(desde, hasta):
            vol = pv[k] - vi
            if vol <= 0:
                continue          # tramo sin agua: no tiene temperatura
            d = pw[k] - wi
            if d < 0:
                d = -d
            # Comparar d/vol con mejor_d/mejor_v sin decimales.
            dif = d * mejor_v - mejor_d * vol
            if dif < 0 or (dif == 0 and not encontrado):
                # dif == 0 sin haber encontrado nada = exactamente 5 grados,
                # que sí está permitido ("nunca más de 5").
                mejor_d, mejor_v = d, vol
                encontrado = True
                mejor_par = (i, k - 1)
    return mejor_par


def main():
    datos = sys.stdin.buffer.read().split()
    problemas = int(datos[0])
    idx = 1
    salida = []
    for _ in range(problemas):
        capacidad, objetivo = int(datos[idx]), int(datos[idx + 1])
        n = int(datos[idx + 2])
        idx += 3
        jarras = []
        for _ in range(n):
            jarras.append((int(datos[idx]), int(datos[idx + 1])))
            idx += 2
        par = resolver(capacidad, objetivo, jarras)
        salida.append("Not possible" if par is None else f"{par[0]} {par[1]}")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
