"""
Colombia 2024 — J: Lumina («Lumina»)
Ejecutar: python lumina.py < lumina.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En el reino de Lumina las calles se iluminan con gemas; el aura de una
    gema activa a las gemas cercanas, en reacción en cadena. Un hechizo las
    apagó todas y el rey quiere saber cuántas hay que encender a mano para
    que, en cadena, se enciendan todas.

QUÉ HAY QUE HACER
    Entrada: varios casos; N (1 ≤ N ≤ 5000) y N líneas "X Y R"
             (|X|, |Y| ≤ 10⁹, 0 ≤ R ≤ 10⁹). Termina con 0.
    Salida:  por caso, el mínimo número de gemas a activar manualmente.

IDEA Y ALGORITMO
    Componentes conexas de un grafo no dirigido (BFS).
    El enunciado define explícitamente: "dos gemas se consideran cercanas
    si una gema se encuentra dentro del radio de iluminación de la otra", y
    el aura activa a las gemas cercanas. Esa relación es SIMÉTRICA:
        i ~ j  ⇔  dist(i, j) ≤ R_i  o  dist(i, j) ≤ R_j
              ⇔  dist² ≤ máx(R_i, R_j)²       (todo en enteros, sin raíces).
    Encender una gema enciende toda su componente conexa y nada más, así
    que la respuesta es el número de componentes conexas.
    (Interpretación: si la activación fuera dirigida —i solo activa a las
    gemas dentro de SU radio— la respuesta sería el número de componentes
    fuertemente conexas sin aristas entrantes. Los tres ejemplos dan lo
    mismo con ambas lecturas; seguimos la definición literal de "cercanas"
    del enunciado, que es simétrica.)

    Implementación: BFS con lista de "no visitados". Al sacar una gema de la
    cola se recorre la lista de no visitados una sola vez, separando las
    cercanas (que entran a la cola) de las demás. Así cada arista no se
    guarda: el grafo puede tener ~N²/2 = 1,25·10⁷ aristas.

MACROALGORITMO
    1. Leer las N gemas; precalcular R².
    2. pendientes = todas las gemas; componentes = 0.
    3. Mientras haya pendientes: sacar una, componentes += 1, BFS:
       a. Sacar gema i de la cola.
       b. Recorrer pendientes: las j con dist² ≤ máx(R_i², R_j²) pasan a
          la cola; el resto sigue pendiente.
    4. Imprimir componentes.

COMPLEJIDAD
    O(N²) en el peor caso (todas aisladas: cada gema revisa todas las
    pendientes) y O(N) memoria. Peor caso medido, N = 5000 gemas aisladas:
    ~3 s en Python por caso; con componentes grandes es mucho más rápido
    porque la lista de pendientes se vacía pronto.

EJEMPLO A MANO
    Caso 3: gema 1 (−1,0) R=4 y gema 2 (2,1): dist² = 10 ≤ 16 ⇒ cercanas.
    Gema 3 (4,−2): dist² con la 1 = 29 > 16 y > 1; con la 2 = 13 > 4 y > 1
    ⇒ aislada. Componentes {1,2}, {3} ⇒ 2.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/J")
    - Fuerza bruta: OK en 500 casos aleatorios (N ≤ 12) contra un
      union-find sobre todos los pares.
"""
import sys


def contar_componentes(xs, ys, rs):
    n = len(xs)
    r2 = [r * r for r in rs]
    pendientes = list(range(n))
    componentes = 0
    while pendientes:
        semilla = pendientes.pop()
        componentes += 1
        cola = [semilla]
        while cola and pendientes:
            i = cola.pop()
            xi, yi, ri2 = xs[i], ys[i], r2[i]
            siguen = []
            for j in pendientes:
                dx = xs[j] - xi
                dy = ys[j] - yi
                d2 = dx * dx + dy * dy
                # Cercanas si j está en el radio de i o i en el radio de j.
                if d2 <= ri2 or d2 <= r2[j]:
                    cola.append(j)
                else:
                    siguen.append(j)
            pendientes = siguen
    return componentes


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos < len(datos):
        n = int(datos[pos]); pos += 1
        if n == 0:
            break
        valores = list(map(int, datos[pos:pos + 3 * n]))
        pos += 3 * n
        xs, ys, rs = valores[0::3], valores[1::3], valores[2::3]
        salida.append(str(contar_componentes(xs, ys, rs)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
