"""
Colombia 2024 — A: Arctic Virus («Virus ártico»)
Ejecutar: python arctic.py < arctic.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    En 2045 se descubre bajo el hielo una tecnología antigua que solo se
    desbloquea con un virus ártico. Los científicos fabrican cadenas de bases
    (A, C, G, T) en el laboratorio y necesitan saber si cada una es una
    configuración válida del virus.

QUÉ HAY QUE HACER
    El virus es el lenguaje generado por la gramática
            φ ::= A | T | φC | Aφ | Aφ⁻¹ | Gφ⁻¹C
    donde φ⁻¹ es la cadena φ invertida (leída al revés).
    Entrada: varias líneas "n s" hasta fin de archivo (EOF), 1 ≤ n ≤ 1000.
    Salida:  por línea, "simple" si s es A o T, "mutation" si s se genera
             con al menos una regla de mutación, "doomed" si no es del virus.
    Restricciones clave: |s| ≤ 1000; número de casos no acotado.

IDEA Y ALGORITMO
    Programación dinámica por intervalos (subcadenas) con DOS lenguajes:
        L = cadenas generadas por φ,
        R = cadenas cuya inversa está en L   (R = { w⁻¹ : w ∈ L }).
    Invirtiendo cada regla de L se obtienen las reglas de R:
        L: A | T | L·C | A·L | A·R | G·R·C
           (Aφ⁻¹ = A seguido de algo de R; Gφ⁻¹C = G, algo de R, C)
        R: A | T | C·R | R·A | L·A | C·L·G
           (inversa de φC es C·φ⁻¹; de Aφ es φ⁻¹A; de Aφ⁻¹ es φA;
            de Gφ⁻¹C es C·φ·G)
    Así, "s[i:i+ℓ] ∈ L" depende solo de subcadenas de longitud ℓ-1 o ℓ-2
    (en L o en R), y basta recorrer las longitudes de menor a mayor.

    Truco de implementación (paralelismo de bits): para cada longitud ℓ
    guardamos un entero de Python cuyo bit i vale 1 si s[i:i+ℓ] ∈ L (ídem
    para R). Las condiciones "s[i] == 'A'" o "s[i+ℓ-1] == 'C'" también son
    máscaras de bits (la segunda es la máscara de C desplazada ℓ-1 a la
    derecha), y "s[i+1:...] ∈ L" es la máscara de la longitud anterior
    desplazada 1 bit. Cada longitud se calcula con unas pocas operaciones
    AND/OR/SHIFT sobre enteros de n bits, en vez de un ciclo sobre i.

    La DP ingenua con memo sobre (i, j, lenguaje) tiene O(n²) estados y en
    Python es lenta si hay muchos casos; con bits pasa a O(n²/64).

MACROALGORITMO
    1. Leer cada línea "n s".
    2. Construir las máscaras de posiciones de A, C, G y T.
    3. Longitud 1: L₁ = R₁ = posiciones con A o T.
    4. Para ℓ = 2..n calcular L_ℓ y R_ℓ con las reglas de arriba, usando
       L_{ℓ-1}, R_{ℓ-1}, L_{ℓ-2}, R_{ℓ-2} y las máscaras de letras.
    5. Si s ∈ L (bit 0 de L_n): "simple" si n == 1, si no "mutation".
       Si no: "doomed".

COMPLEJIDAD
    Tiempo O(n · n/64) operaciones de máquina por caso (n operaciones con
    enteros de n bits); memoria O(n) bits por máscara. n = 1000 tarda
    ~2 ms por caso.

EJEMPLO A MANO
    "AT": ℓ=2, i=0: s[0]='A' y s[1:2]="T" ∈ L  ⇒  AT = A·φ con φ=T ⇒ mutation.
    "TTG": termina en G y no empieza por A/G; L exige terminar en C, empezar
    por A o empezar por G ⇒ doomed.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/A")
    - Fuerza bruta: OK. Se generaron TODAS las cadenas del lenguaje hasta
      longitud 9 aplicando la gramática y se comparó la respuesta para todas
      las 4^1+…+4^8 cadenas de longitud ≤ 8 (y 3000 aleatorias de long. 9).
"""
import sys


def clasificar(s):
    """Devuelve 'simple', 'mutation' o 'doomed' para la cadena s."""
    n = len(s)
    # Máscaras de letras: bit i encendido si s[i] es esa letra.
    mA = mC = mG = mT = 0
    for i, ch in enumerate(s):
        b = 1 << i
        if ch == 'A':
            mA |= b
        elif ch == 'C':
            mC |= b
        elif ch == 'G':
            mG |= b
        else:
            mT |= b

    # Longitud 1: tanto L como R contienen exactamente "A" y "T".
    L_prev2 = R_prev2 = 0          # longitud ℓ-2 (para ℓ=2 sería la vacía: no está)
    L_prev = R_prev = mA | mT      # longitud ℓ-1
    for ell in range(2, n + 1):
        valido = (1 << (n - ell + 1)) - 1      # inicios i con i+ℓ ≤ n
        finC = mC >> (ell - 1)                 # bit i: s[i+ℓ-1] == 'C'
        finA = mA >> (ell - 1)                 # bit i: s[i+ℓ-1] == 'A'
        finG = mG >> (ell - 1)                 # bit i: s[i+ℓ-1] == 'G'
        # L_ℓ[i]:
        #   φC   : último es C y s[i:i+ℓ-1] ∈ L          -> finC & L_prev
        #   Aφ   : primero A y s[i+1:i+ℓ] ∈ L            -> mA & (L_prev >> 1)
        #   Aφ⁻¹ : primero A y s[i+1:i+ℓ] ∈ R            -> mA & (R_prev >> 1)
        #   Gφ⁻¹C: primero G, último C, medio ∈ R        -> mG & finC & (R_prev2 >> 1)
        L_cur = ((finC & L_prev)
                 | (mA & ((L_prev | R_prev) >> 1))
                 | (mG & finC & (R_prev2 >> 1))) & valido
        # R_ℓ[i] (reglas invertidas):
        #   C·R  : primero C y resto ∈ R                  -> mC & (R_prev >> 1)
        #   R·A, L·A : último A y prefijo ∈ R o L         -> finA & (R_prev | L_prev)
        #   C·L·G: primero C, último G, medio ∈ L         -> mC & finG & (L_prev2 >> 1)
        R_cur = ((mC & (R_prev >> 1))
                 | (finA & (R_prev | L_prev))
                 | (mC & finG & (L_prev2 >> 1))) & valido
        L_prev2, R_prev2 = L_prev, R_prev
        L_prev, R_prev = L_cur, R_cur

    if L_prev & 1:                 # s = s[0:n] pertenece a L
        return "simple" if n == 1 else "mutation"
    return "doomed"


def main():
    salida = []
    for linea in sys.stdin.read().splitlines():
        partes = linea.split()
        if len(partes) < 2:
            continue
        # La cadena es el segundo campo; n es redundante (n == len(s)).
        salida.append(clasificar(partes[1]))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
