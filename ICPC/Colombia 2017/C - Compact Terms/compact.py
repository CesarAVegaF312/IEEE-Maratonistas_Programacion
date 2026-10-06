"""
Colombia 2017 — C: Compact Terms («Términos compactos»)
Ejecutar: python compact.py < compact.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    Un término es un árbol: variables (empiezan en mayúscula), constantes
    (símbolos de función sin argumentos) y aplicaciones f(t1,...,tn). Para
    ahorrar espacio, los subtérminos iguales se pueden compartir y el árbol se
    convierte en un multigrafo acíclico dirigido (dam).

QUÉ HAY QUE HACER
    Entrada: varios casos hasta EOF; cada línea es la cadena de un término
             (longitud <= 10^5, a lo sumo 2000 símbolos).
    Salida:  por caso, el mínimo número de vértices de un dam que lo
             represente.
    Restricciones clave: <= 2000 símbolos por término (profundidad hasta
             ~2000: no usar recursión de Python).

IDEA Y ALGORITMO
    El dam mínimo comparte TODO subtérmino repetido: dos vértices con la misma
    etiqueta y los mismos hijos (en el mismo orden) se pueden fusionar, y dos
    subtérminos distintos nunca pueden ser el mismo vértice (representarían
    términos distintos). Por lo tanto la respuesta = número de SUBTÉRMINOS
    DISTINTOS. Se cuentan con HASH-CONSING (numeración canónica):
      - a cada subtérmino se le asigna un id entero;
      - la clave de un subtérmino es (nombre, tupla de ids de sus hijos);
      - un diccionario clave -> id da el mismo id a subtérminos iguales.
    Como los hijos ya tienen id canónico al cerrar el paréntesis, comparar
    claves es O(aridad) y no hay que comparar cadenas largas.
    El análisis sintáctico se hace con una PILA EXPLÍCITA (sin recursión):
    al ver "nombre(" se apila un marco nuevo; al ver ")" se cierra el marco,
    se calcula su id y se agrega como hijo del marco anterior.

MACROALGORITMO
    1. Por cada línea no vacía, quitar espacios.
    2. Recorrer la cadena leyendo tokens: nombre, '(', ',', ')'.
    3. Nombre seguido de '(': apilar marco [nombre, hijos=[]].
       Nombre sin '(' (variable o constante): id de (nombre, ()) y agregarlo
       como hijo del marco de la cima (o es el término completo).
    4. ')': desapilar el marco, id de (nombre, tupla(hijos)), agregarlo al
       marco de la cima.
    5. Respuesta = cantidad de claves distintas en el diccionario.

COMPLEJIDAD
    Tiempo O(|s|) por caso (cada símbolo se procesa una vez y su clave tiene
    tamaño aridad; la suma de aridades es <= número de símbolos).
    Memoria O(número de símbolos). Medido: 22 términos (cadena de
    profundidad 1000, 1900 argumentos de 20 letras, árboles aleatorios de
    ~2000 símbolos; 310 KB en total) en 0.11 s.

EJEMPLO A MANO
    f(g(a,X,a),g(a,X,a)): subtérminos distintos a, X, g(a,X,a), f(...) -> 4.
    f(g(a,X,a),g(a,a,X)): a, X, g(a,X,a), g(a,a,X), f(...) -> 5.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "Colombia 2017/C")
    - Fuerza bruta: OK en 1000 términos aleatorios: parser recursivo que
      guarda el TEXTO canónico de cada subtérmino en un conjunto.
"""
import sys


def contar_subterminos(s):
    ids = {}          # (nombre, tupla_ids_hijos) -> id canónico
    pila = []         # marcos abiertos: [nombre, lista_de_ids_hijos]
    raiz = []         # recibe el id del término completo
    i, n = 0, len(s)

    def id_de(clave):
        v = ids.get(clave)
        if v is None:
            v = len(ids)
            ids[clave] = v
        return v

    while i < n:
        ch = s[i]
        if ch.isalpha():
            j = i
            while j < n and s[j].isalpha():
                j += 1
            nombre = s[i:j]
            if j < n and s[j] == "(":
                # Aplicación f( ... ): se abre un marco y se esperan los hijos.
                pila.append([nombre, []])
                i = j + 1
            else:
                # Hoja: variable o constante (aridad 0).
                destino = pila[-1][1] if pila else raiz
                destino.append(id_de((nombre, ())))
                i = j
        elif ch == ")":
            nombre, hijos = pila.pop()
            destino = pila[-1][1] if pila else raiz
            destino.append(id_de((nombre, tuple(hijos))))
            i += 1
        else:
            # ',' separa argumentos; no hay que hacer nada más.
            i += 1
    return len(ids)


def main():
    salida = []
    for linea in sys.stdin.read().split("\n"):
        termino = "".join(linea.split())   # quita espacios / '\r'
        if termino:
            salida.append(str(contar_subterminos(termino)))
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
