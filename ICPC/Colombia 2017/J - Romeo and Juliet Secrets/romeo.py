"""
Colombia 2017 — J: Romeo and Juliet Secrets («Los secretos de Romeo y Julieta»)
Ejecutar: python romeo.py < romeo.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Romeo y Julieta esconden una palabra W en sus mensajes: en cada aparición
    de W reemplazan una subcadena de longitud K por K letras al azar. Lord
    Capulet interceptó un mensaje T y quiere saber cuántas veces pudo estar W.

QUÉ HAY QUE HACER
    Entrada: número de casos; por caso T, W y K (en líneas separadas).
    Salida:  por caso, cuántas posiciones i de T cumplen que T[i:i+|W|]
             es W con a lo sumo un bloque CONTIGUO de longitud K alterado
             (las apariciones solapadas cuentan por separado).
    Restricciones clave: |T| <= 10^5, 1 <= K <= |W| <= |T|.

IDEA Y ALGORITMO
    La ventana V = T[i:i+L] (L = |W|) es válida si todas las diferencias con
    W caen dentro de un intervalo de longitud K. Si P = largo del prefijo
    común de V y W, y Q = largo del sufijo común, las diferencias están en
    [P, L-1-Q], así que la condición es  P + Q >= L - K  (si P = L la ventana
    es W exacta, que también vale: las letras "al azar" pueden coincidir).
    P y Q para TODAS las ventanas a la vez con la FUNCIÓN Z:
      * Z de  W + '#' + T  da, para cada i, el prefijo común de T[i:] y W.
      * Z de  rev(W) + '#' + rev(T)  da el sufijo común de T[:j+1] y W, que
        para la ventana que empieza en i se lee en j = i + L - 1.
    Probar cada ventana carácter a carácter sería O(|T|*|W|) = 10^10.

MACROALGORITMO
    1. Leer el número de casos y, por caso, T, W, K.
    2. zp = Z(W + '#' + T); P[i] = min(zp[L+1+i], L).
    3. zs = Z(rev(W) + '#' + rev(T)); la ventana i termina en j = i+L-1, que
       en el texto invertido es la posición |T|-1-j.
    4. Contar las i en [0, |T|-L] con P[i] + Q[i] >= L - K.
    5. Imprimir el conteo.

COMPLEJIDAD
    Tiempo O(|T| + |W|) por caso, memoria O(|T| + |W|).
    Medido: 5 casos con |T| = 10^5 (y |W| hasta 10^5) en 0.97 s en total,
    ~0.2 s por caso; con muchos casos grandes Python podría ser lento.

EJEMPLO A MANO
    T = abcabc..., W = acb, K = 2: en "abc" P = 1, Q = 0 -> 1 >= 1 sí; en
    "cab" P = 0, Q = 1 -> sí; en "bca" P = Q = 0 -> no. 5 + 4 = 9 ventanas.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/J")
    - Fuerza bruta: OK en 2000 casos aleatorios (|T| <= 15, alfabetos de 1 a
      3 letras): para cada ventana y cada posición del bloque de largo K se
      compara literalmente fuera del bloque.
"""
import sys


def funcion_z(s):
    """z[i] = largo del prefijo común más largo entre s y s[i:] (z[0] = n)."""
    n = len(s)
    z = [0] * n
    if n == 0:
        return z
    z[0] = n
    izq = der = 0                    # [izq, der) = caja Z más a la derecha
    for i in range(1, n):
        if i < der:
            zi = z[i - izq]
            if zi > der - i:
                zi = der - i
        else:
            zi = 0
        while i + zi < n and s[zi] == s[i + zi]:
            zi += 1
        z[i] = zi
        if i + zi > der:
            izq, der = i, i + zi
    return z


def contar(t, w, k):
    n, L = len(t), len(w)
    if L > n:
        return 0
    zp = funcion_z(w + "#" + t)              # prefijos comunes con W
    zs = funcion_z(w[::-1] + "#" + t[::-1])  # sufijos comunes con W
    necesario = L - k
    total = 0
    for i in range(n - L + 1):
        p = zp[L + 1 + i]
        if p >= necesario:                   # incluye el caso p == L
            total += 1
            continue
        j = i + L - 1                        # último índice de la ventana
        q = zs[L + 1 + (n - 1 - j)]
        if p + q >= necesario:
            total += 1
    return total


def main():
    datos = sys.stdin.read().split()
    if not datos:
        return
    casos = int(datos[0])
    salida = []
    pos = 1
    for _ in range(casos):
        t, w, k = datos[pos], datos[pos + 1], int(datos[pos + 2])
        pos += 3
        salida.append(str(contar(t, w, k)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
