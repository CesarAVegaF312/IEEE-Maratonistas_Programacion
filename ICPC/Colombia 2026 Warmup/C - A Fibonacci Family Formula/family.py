"""
Colombia 2026 Warmup — C: A Fibonacci Family Formula («Una fórmula de la familia Fibonacci»)
Ejecutar: python family.py < family.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

NOTA: problema idéntico (enunciado y ejemplo) a Colombia 2018 F; esta solución es copia de
    Colombia 2018/F - A Fibonacci Family Formula/family.py (generada con _herramientas/copiar_warmup.py).

CONTEXTO
    En la familia Fibonacci, cada vez que alguien cumple 21 años se inventa
    una sucesión nueva que suma un término más que la anterior: 1,1,1,…;
    1,1,2,3,5,…; 1,1,2,4,7,13,…  Leonardo será el k-ésimo y le preguntarán
    términos al azar de «su» sucesión.

QUÉ HAY QUE HACER
    Entrada: líneas «k n» hasta «0 0» (OJO: primero k, luego n; así lo
             confirma el ejemplo: «3 4» → 7 = f_4 de la tribonacci).
    Salida:  f_n^(k) mód 1 000 000 009, donde
             f_n = 0 si n < 0,  f_0 = 1,  f_n = f_{n-1} + … + f_{n-k} si n ≥ 1.
    Restricciones clave: 1 ≤ k ≤ 100, 0 ≤ n ≤ 10^15, varios casos.

IDEA Y ALGORITMO
    Recurrencia lineal de orden k con n gigante → método de KITAMASA
    (x^n módulo el polinomio característico), más rápido que exponenciar la
    matriz k×k (que costaría k^3·log n ≈ 5·10^7 por caso en Python).
    - Sea φ el funcional lineal φ(x^m) = f_m. Como f cumple la recurrencia
      para todo m ≥ k, φ se anula en todo múltiplo x^j·P(x) del polinomio
      característico P(x) = x^k − x^{k−1} − … − x − 1. Por eso, si
      x^n ≡ R(x) (mód P), entonces f_n = φ(R) = Σ r_j·f_j: basta conocer
      los k primeros términos, que son f_0 = 1 y f_j = 2^{j−1} (1 ≤ j ≤ k),
      porque cada uno es la suma de TODOS los anteriores.
    - Truco para reducir rápido: Q(x) = (x − 1)·P(x) = x^{k+1} − 2x^k + 1.
      Como P divide a Q, φ también se anula en los múltiplos de Q y podemos
      trabajar módulo Q. La ventaja: x^{k+1} ≡ 2x^k − 1 (mód Q) tiene sólo
      dos términos, así que reducir un polinomio de grado 2k cuesta O(k)
      (cada coeficiente alto c_i se reparte en +2c_i en x^{i−1} y −c_i en
      x^{i−k−1}), en vez de O(k^2).
    - El producto de dos polinomios de grado ≤ k se hace con SUSTITUCIÓN DE
      KRONECKER: se empaquetan los coeficientes en un único entero grande
      (72 bits por coeficiente, suficiente porque cada coeficiente del
      producto es < 101·MOD² < 2^67), se multiplica con la aritmética de
      enteros de Python (en C) y se desempaqueta.
    - x^n mód Q se calcula por exponenciación binaria: por cada bit de n,
      elevar al cuadrado y, si el bit vale 1, multiplicar por x (desplazar).
    - Como R tiene grado ≤ k, f_n = Σ_{j=0..k} r_j·f_j (f_k = 2^{k−1} es un
      término real de la sucesión, así que también vale para j = k).

MACROALGORITMO
    1. Leer pares (k, n) hasta 0 0.
    2. Calcular los términos iniciales f_0..f_k (1, 1, 2, 4, …, 2^{k−1}).
    3. Si n ≤ k, responder f_n directamente.
    4. Si no, R = x^n mód Q con exponenciación binaria
       (cuadrado con Kronecker + reducción O(k) usando x^{k+1} = 2x^k − 1).
    5. Responder Σ r_j·f_j mód 1 000 000 009.

COMPLEJIDAD
    Tiempo O(log n · (M(k) + k)) por caso, donde M(k) es el producto de
    enteros de ~7 000 bits (muy rápido); memoria O(k). Con k ≈ 100 y
    n ≈ 10^15: ~6.5 ms por caso; 1 000 casos así: ~6.5 s (el costo lo
    domina desempacar los coeficientes, no la multiplicación).

EJEMPLO A MANO
    «5 5»: f = 1, 1, 2, 4, 8, 16 → 16 (n ≤ k, respuesta directa).
    «2 3»: Fibonacci 1, 1, 2, 3 → 3.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Warmup/C")
    - Fuerza bruta: OK en 2 000 casos aleatorios (k ≤ 100, n ≤ 3 000) contra
      la simulación directa de la recurrencia con suma deslizante.
"""
import sys

MOD = 1_000_000_009
BYTES = 9            # 72 bits por coeficiente en la sustitución de Kronecker


def empacar(coefs):
    """Polinomio (lista de coeficientes, grado creciente) -> entero grande."""
    return int.from_bytes(b"".join(c.to_bytes(BYTES, "little") for c in coefs), "little")


def desempacar(valor, cantidad):
    """Entero grande -> lista de `cantidad` coeficientes (sin reducir)."""
    crudo = valor.to_bytes(BYTES * cantidad, "little")
    return [int.from_bytes(crudo[BYTES * i:BYTES * (i + 1)], "little") for i in range(cantidad)]


def reducir(c, k):
    """Reduce c (lista, grado arbitrario ≤ 2k) módulo Q = x^{k+1} − 2x^k + 1,
    devolviendo k+1 coeficientes en [0, MOD).  Usa x^{k+1} ≡ 2x^k − 1."""
    for i in range(len(c) - 1, k, -1):
        v = c[i] % MOD
        if v:
            c[i - 1] += 2 * v        # 2·x^{i−1}
            c[i - k - 1] -= v        # −x^{i−k−1}
    return [x % MOD for x in c[:k + 1]]


def x_a_la_n_mod_q(n, k):
    """Coeficientes de x^n mód Q (grado ≤ k)."""
    res = [1] + [0] * k              # el polinomio 1
    for bit in bin(n)[2:]:
        # Elevar al cuadrado (producto de Kronecker) y reducir.
        e = empacar(res)
        res = reducir(desempacar(e * e, 2 * k + 2), k)
        if bit == "1":
            # Multiplicar por x = desplazar un lugar; luego reducir el
            # coeficiente que se sale (grado k+1).
            res = reducir([0] + res, k)
    return res


def termino(k, n):
    # Términos iniciales: f_0 = 1, f_j = 2^{j−1} para 1 ≤ j ≤ k.
    iniciales = [1] + [pow(2, j - 1, MOD) for j in range(1, k + 1)]
    if n <= k:
        return iniciales[n]
    r = x_a_la_n_mod_q(n, k)
    return sum(rj * fj for rj, fj in zip(r, iniciales)) % MOD


def main():
    datos = sys.stdin.buffer.read().split()
    salida = []
    for i in range(0, len(datos) - 1, 2):
        k, n = int(datos[i]), int(datos[i + 1])
        if k == 0 and n == 0:
            break
        salida.append(str(termino(k, n)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
