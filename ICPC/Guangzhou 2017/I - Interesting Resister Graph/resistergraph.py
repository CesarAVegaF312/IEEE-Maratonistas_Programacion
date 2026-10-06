"""
ACM ICPC Guangzhou Summer Series 2017 — I: Interesting Resister Graph («Un grafo de resistencias interesante»)
Ejecutar: python resistergraph.py < resistergraph.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

ESTADO: la salida del EJEMPLO NO SE REPRODUCE (ver VERIFICACIÓN). La
solución calcula la resistencia equivalente físicamente correcta para la
lectura natural del grafo y está verificada contra fuerza bruta, pero el
juez original parece usar otra fórmula (probablemente con un error).

CONTEXTO
    Un grafo "abanico": los nodos v1, …, v_{n-1} forman un camino
    (v_i – v_{i+1}) y el último nodo v_n (el "centro") está unido a todos
    los demás. Cada arista es una resistencia de 1 Ω. Se pide la
    resistencia equivalente entre dos nodos v_i y v_j.

QUÉ HAY QUE HACER
    Entrada: hasta fin de archivo, líneas "n i j" (≤ 10000 líneas),
             1 ≤ i < j ≤ n ≤ 10000.
    Salida:  la resistencia equivalente entre v_i y v_j con 6 decimales.
    Erratas del enunciado: numera los nodos v1..vn pero escribe los rangos
    como 0 ≤ i ≤ n-2 y 0 ≤ j ≤ n-1. Lo leemos como índices 1..n: camino
    v1–v2–…–v_{n-1} y centro v_n unido a v1..v_{n-1} (si se lee con un v0
    extra el resultado tampoco reproduce el ejemplo; ver VERIFICACIÓN).

IDEA Y ALGORITMO
    Resistencia efectiva = función de Green del Laplaciano reducido.
    * Si conectamos el centro v_n a tierra (potencial 0), los potenciales de
      v1..vm (m = n-1) cumplen T·φ = corriente inyectada, donde T es el
      Laplaciano sin la fila/columna del centro: tridiagonal con -1 fuera de
      la diagonal y diagonal 2 en los extremos (grado 2) y 3 en el interior.
    * Para una matriz tridiagonal la inversa tiene forma "producto":
          G(i,j) = (T^-1)_{ij} = u_i · w_j / det(T)   (i ≤ j)
      con u la solución de la recurrencia de las filas desde arriba y w
      desde abajo. Aquí u_i = F_{2i-1} (Fibonacci impares: cumplen
      x_{k+1} = 3x_k - x_{k-1}, que es la fila interior, y 2·u_1 = u_2 es la
      primera fila), w_j = F_{2(m-j)+1} por simetría y det(T) = F_{2m}.
    * Con la fuente de 1 A entre a y b, la resistencia es
          R(v_a, centro) = G(a,a)
          R(v_a, v_b)    = G(a,a) + G(b,b) - 2·G(a,b)
      (superposición: φ = G·(e_a - e_b), R = (e_a - e_b)^T G (e_a - e_b)).
    * Los Fibonacci de índice 2·10^4 tienen ~14 000 bits: se usan enteros
      exactos de Python y una sola división real al final (int / int en
      Python redondea correctamente aunque los enteros sean enormes).

MACROALGORITMO
    1. Leer todas las consultas; precalcular F_0..F_{2·max n} exactos.
    2. Para cada consulta: m = n-1.
    3. Si j = n (el centro): R = F_{2i-1}·F_{2m-2i+1} / F_{2m}.
    4. Si no: R = (F_{2i-1}F_{2m-2i+1} + F_{2j-1}F_{2m-2j+1}
                   - 2·F_{2i-1}F_{2m-2j+1}) / F_{2m}.
    5. Imprimir con 6 decimales.

COMPLEJIDAD
    Precálculo O(N) sumas de enteros grandes (N = 2·10^4) y O(1)
    multiplicaciones de enteros de ~14 000 bits por consulta: 10 000
    consultas aleatorias con n = 10^4 tardan ≈ 1 s.

VERIFICACIÓN
    - Ejemplo del enunciado: NO coincide. Esperado 0.298142 y 0.447214;
      esta solución da 0.666667 y 0.666667 (n = 3 es un triángulo de
      resistencias de 1 Ω: entre cualquier par, 1 Ω ‖ 2 Ω = 2/3 Ω).
      Investigación hecha (scripts en la carpeta temporal):
        · 0.298142 = 2/(3√5) y 0.447214 = 1/√5 son irracionales; una red
          FINITA de resistencias racionales siempre da un valor racional,
          así que NINGUNA lectura con resistencias de 1 Ω puede dar
          exactamente esos números.
        · Se probaron abanicos y ruedas (con y sin v0 extra, índices 0 o 1)
          hasta 40 nodos y todos los pares: 0.447214 aparece solo como
          límite (n grande, nodo lejos de los extremos) de R(centro, v_i),
          que tiende a 1/√5; 0.298142 no aparece nunca.
        · 1/√5 es exactamente lo que da la fórmula G(i,i) si se usa la
          aproximación de Binet F_k ≈ φ^k/√5 (sin el término ψ^k): sugiere
          que el juez usó fórmulas asintóticas o con Binet mal aplicado.
          No encontramos una fórmula "con error" natural que dé además
          2/(3√5) para (3,1,2), así que no podemos imitar al juez.
    - Fuerza bruta (Laplaciano completo resuelto con fracciones exactas,
      n ≤ 12, todos los pares): OK en todos los casos (n = 2..12).
"""
import sys


def main():
    datos = sys.stdin.buffer.read().split()
    consultas = [tuple(int(x) for x in datos[k:k + 3])
                 for k in range(0, len(datos) - 2, 3)]
    if not consultas:
        return
    max_n = max(c[0] for c in consultas)

    # Fibonacci exactos: fib[0] = 0, fib[1] = 1, …
    tope = 2 * max_n + 2
    fib = [0] * (tope + 1)
    fib[1] = 1
    for k in range(2, tope + 1):
        fib[k] = fib[k - 1] + fib[k - 2]

    salida = []
    for n, i, j in consultas:
        if i > j:
            i, j = j, i
        m = n - 1                     # nodos del camino: v1..vm; centro v_n
        det = fib[2 * m]

        def g(a, b):
            """Numerador de la función de Green G(a,b) (a ≤ b); G = g/det."""
            return fib[2 * a - 1] * fib[2 * (m - b) + 1]

        if j == n:                    # par (camino, centro)
            num = g(i, i)
        else:                         # dos nodos del camino
            num = g(i, i) + g(j, j) - 2 * g(i, j)
        salida.append("%.6f" % (num / det))
    sys.stdout.write("\n".join(salida) + "\n")


if __name__ == "__main__":
    main()
