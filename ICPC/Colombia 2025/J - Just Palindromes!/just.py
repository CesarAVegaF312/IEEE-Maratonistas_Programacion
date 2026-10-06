"""
Colombia 2025 — J: Just Palindromes! («¡Solo palíndromos!»)
Ejecutar: python just.py < just.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    A Ana le gustan los palíndromos: frases que se leen igual al derecho y al
    revés si se ignoran espacios, puntuación, mayúsculas/minúsculas y todo lo
    que no sea letra del alfabeto inglés.

QUÉ HAY QUE HACER
    Entrada: varias líneas (frases de 0 a 999 caracteres ASCII imprimibles).
             Una línea con un único "*" termina la entrada.
    Salida:  por frase, "Y" si es palíndromo y "N" si no.
    Restricciones clave: |S| < 1000; puede haber frases vacías o sin letras.

IDEA Y ALGORITMO
    Normalización + comparación con la inversa:
      1. Quedarse solo con las letras A–Z / a–z (se filtra con el rango ASCII,
         NO con str.isalpha(), que aceptaría letras de otros alfabetos).
      2. Pasar a minúsculas.
      3. Es palíndromo si la cadena resultante es igual a su reverso.
    Caso borde: si no queda ninguna letra (frase vacía o como ".---.-"), la
    cadena vacía es palíndromo → "Y" (así lo confirma el ejemplo).
    OJO: la lectura se hace por líneas y sin recortar espacios internos, pues
    la frase es la línea completa (puede empezar o terminar con espacios).

MACROALGORITMO
    1. Leer línea por línea; quitar solo el salto de línea final.
    2. Si la línea es "*", terminar.
    3. Filtrar letras inglesas y pasarlas a minúscula.
    4. Comparar con su reverso e imprimir Y/N.

COMPLEJIDAD
    Tiempo O(|S|) por frase, memoria O(|S|).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2025/J")
    - Fuerza bruta (comparación con dos punteros sobre la línea original):
      OK en 2000 líneas aleatorias.
    - Caso grande (20 000 líneas de 999 caracteres): ~1.3 s.
"""
import sys

LETRAS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def es_palindromo(frase):
    # Solo letras del alfabeto inglés, sin distinguir mayúsculas.
    limpia = [c.lower() for c in frase if c in LETRAS]
    return limpia == limpia[::-1]


def main():
    salida = []
    for linea in sys.stdin:
        frase = linea.rstrip("\r\n")
        if frase.strip() == "*":  # marcador de fin
            break
        salida.append("Y" if es_palindromo(frase) else "N")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
