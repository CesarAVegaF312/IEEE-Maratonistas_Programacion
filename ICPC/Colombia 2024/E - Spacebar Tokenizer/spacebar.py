"""
Colombia 2024 — E: Spacebar Tokenizer («El tokenizador de la barra espaciadora»)
Ejecutar: python spacebar.py < spacebar.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Una startup quiere que los programadores no pierdan tiempo pulsando la
    barra espaciadora: un tokenizador parte el texto pegado en tokens. Un
    modelo de lenguaje da una puntuación a cada token conocido (y 0 a los
    desconocidos); la mejor tokenización es la de mayor puntuación total.

QUÉ HAY QUE HACER
    Entrada: varios casos "m s" (1 ≤ m ≤ 1000, 1 ≤ s ≤ 100); m líneas
             "token puntuación" (token de 1..100 minúsculas, puntuación > 0)
             y s oraciones (1..1500 minúsculas). Termina con "0 0".
    Salida:  por cada oración, la puntuación de la tokenización óptima.

IDEA Y ALGORITMO
    Programación dinámica sobre prefijos + trie (árbol de prefijos).
        mejor[i] = máxima puntuación tokenizando los primeros i caracteres.
        mejor[0] = 0
        mejor[i+1] ≥ mejor[i]                (el carácter i queda dentro de un
                                              token desconocido: aporta 0)
        mejor[i+ℓ] ≥ mejor[i] + valor(t)     si el token conocido t, de
                                              longitud ℓ, empieza en i.
    ¿Por qué basta "avanzar un carácter con 0"? Un trozo desconocido de
    varios caracteres equivale a una cadena de pasos de 0; y si ese trozo
    resultara ser un token conocido, su valor es > 0, así que el máximo nunca
    se subestima ni se sobreestima (todas las puntuaciones son ≥ 0).
    Para encontrar los tokens que empiezan en i se recorre el trie desde la
    raíz siguiendo s[i], s[i+1], …; el recorrido se corta en cuanto no hay
    rama (y nunca supera 100 pasos), así que es mucho más rápido que probar
    los m tokens en cada posición.

MACROALGORITMO
    1. Leer los m tokens y construir un trie de diccionarios; el valor de un
       token se guarda en su nodo final (clave especial).
    2. Para cada oración a: mejor = [0]*(|a|+1), con -∞ no hace falta
       porque siempre se puede avanzar con 0.
    3. Para i = 0..|a|-1: propagar mejor[i] a mejor[i+1]; recorrer el trie
       desde a[i] y, por cada token completo encontrado de longitud ℓ,
       relajar mejor[i+ℓ].
    4. Imprimir mejor[|a|].

COMPLEJIDAD
    Tiempo O(|a| · min(100, profundidad útil del trie)) por oración; peor
    caso teórico 1500·100 = 1,5·10⁵ pasos por oración, 1,5·10⁷ por caso.
    Un caso adversario (tokens a, aa, …, a^100 y 100 oraciones de 1500 'a')
    tarda ~2,6 s en Python; con datos normales es instantáneo.

EJEMPLO A MANO
    "ilovespacebartokenizer": i(2) + love(4) + spacebar(13) + tokenizer(5)
    = 24 (supera a space(5)+bar(7) = 12 < 13).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2024/E")
    - Fuerza bruta: OK en 500 casos aleatorios (alfabeto {a,b,c}, oraciones
      ≤ 10) contra la enumeración de las 2^(n-1) formas de cortar la oración.
"""
import sys

FIN = ''   # clave del nodo del trie donde se guarda el valor del token


def construir_trie(tokens):
    """tokens: lista de (cadena, valor). Devuelve la raíz del trie."""
    raiz = {}
    for palabra, valor in tokens:
        nodo = raiz
        for ch in palabra:
            nodo = nodo.setdefault(ch, {})
        nodo[FIN] = valor
    return raiz


def mejor_puntuacion(oracion, raiz):
    n = len(oracion)
    mejor = [0] * (n + 1)          # mejor[i]: óptimo para el prefijo de longitud i
    for i in range(n):
        base = mejor[i]
        # Caso "carácter dentro de un token desconocido" (aporta 0).
        if base > mejor[i + 1]:
            mejor[i + 1] = base
        # Tokens conocidos que empiezan en i: caminar por el trie.
        nodo = raiz
        j = i
        while j < n:
            nodo = nodo.get(oracion[j])
            if nodo is None:
                break
            j += 1
            valor = nodo.get(FIN)
            if valor is not None and base + valor > mejor[j]:
                mejor[j] = base + valor
    return mejor[n]


def main():
    datos = sys.stdin.buffer.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        m, s = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if m == 0 and s == 0:
            break
        tokens = []
        for _ in range(m):
            tokens.append((datos[pos].decode(), int(datos[pos + 1])))
            pos += 2
        raiz = construir_trie(tokens)
        for _ in range(s):
            salida.append(str(mejor_puntuacion(datos[pos].decode(), raiz)))
            pos += 1
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
