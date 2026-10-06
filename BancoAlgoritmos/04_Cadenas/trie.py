"""
Cadenas — Trie o árbol de prefijos («Trie / prefix tree»)
Nivel: Intermedio
Ejecutar: python trie.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Guarda un diccionario de palabras como un árbol donde cada camino desde
    la raíz deletrea un prefijo. Responde en O(|palabra|) — sin importar
    cuántas palabras haya — «¿está esta palabra?», «¿cuántas palabras
    empiezan con este prefijo?», y permite recorrer un texto desde una
    posición encontrando TODAS las palabras del diccionario que empiezan
    allí (clave para DP de segmentar un texto en palabras).
    Señales en el enunciado: diccionario de miles de palabras + consultas
    por prefijo; «autocompletar»; «partir la cadena en palabras del
    diccionario»; «tokens»; inserciones y borrados intercalados.

FUNCIÓN
    Trie()
        .insertar(palabra)              agrega una aparición (se permiten repetidas)
        .eliminar(palabra) -> bool      quita una aparición; False si no estaba
        .contar_palabra(palabra) -> int cuántas veces fue insertada (y no borrada)
        .contar_prefijo(prefijo) -> int cuántas palabras insertadas empiezan así
                                        (prefijo vacío = total de palabras)
        .palabras_desde(s, i) -> list[int]
            Largos L de las palabras del trie que son s[i:i+L] (crecientes).
    formas_de_partir(s, diccionario, mod) -> int
        Cuántas maneras hay de escribir s como concatenación de palabras del
        diccionario (cada una se puede usar varias veces), módulo mod.

IDEA Y ALGORITMO
    Cada nodo representa un prefijo; sus hijos, ese prefijo más una letra.
    Dos palabras con el mismo comienzo comparten el camino: el trie tiene a
    lo más Σ|palabra| + 1 nodos. En cada nodo se guardan dos contadores:
        fin[v]   = cuántas palabras terminan exactamente en v
        pasan[v] = cuántas palabras pasan por v (terminan en v o debajo)
    insertar suma 1 a pasan en todo el camino y a fin al final; eliminar
    resta lo mismo. contar_prefijo es pasan del nodo del prefijo.
    Segmentar: formas[i] = número de maneras de partir s[:i]. Desde cada
    posición i con formas[i] > 0 se baja por el trie leyendo s[i], s[i+1],
    …; cada nodo con fin > 0 a profundidad L es una palabra s[i:i+L], así
    que formas[i+L] += formas[i]. El recorrido para en cuanto no hay hijo,
    por eso cuesta O(largo máximo de palabra) y no O(número de palabras).
    Representación: listas paralelas indexadas por número de nodo, con un
    dict de hijos por nodo (rápido en Python y sirve para cualquier alfabeto).

MACROALGORITMO
    1. Nodo 0 = raíz (prefijo vacío). hijos = [{}], fin = [0], pasan = [0].
    2. insertar: v = 0; pasan[0] += 1; por cada letra, crear el hijo si no
       existe, bajar y sumar 1 a pasan; al final fin[v] += 1.
    3. buscar / contar_prefijo: bajar letra por letra; si falta un hijo,
       la respuesta es 0; si no, fin[v] o pasan[v].
    4. eliminar: verificar que esté (fin > 0) y restar en el mismo camino.
    5. formas_de_partir: formas[0] = 1; para cada i, bajar por el trie desde
       la raíz con s[i:], sumando formas[i] en cada fin encontrado.

COMPLEJIDAD
    insertar / eliminar / contar: O(|palabra|). Memoria O(Σ|palabras|)
    nodos. formas_de_partir: O(|s|·Lmax). En Python, ~10^6 letras
    insertadas por segundo.

EJEMPLO A MANO
    insertar "a", "ab", "abc", "b":
      raíz(pasan 4) ─a→ v1(fin 1, pasan 3) ─b→ v2(fin 1, pasan 2) ─c→ v3(fin 1, pasan 1)
               └──b→ v4(fin 1, pasan 1)
    contar_prefijo("ab") = pasan[v2] = 2; contar_palabra("abc") = 1.
    formas_de_partir("abab", {a, b, ab}): formas = [1, 1, 2, 2, 4]
      (i=0: "a"→f[1]+=1, "ab"→f[2]+=1; i=1: "b"→f[2]+=1; i=2: "a"→f[3]+=2,
       "ab"→f[4]+=2; i=3: "b"→f[4]+=2) → 4: a|b|a|b, ab|a|b, a|b|ab, ab|ab

ERRORES TÍPICOS
    - Marcar el fin con un booleano y luego querer contar repetidas o
      eliminar: usar contadores.
    - Representar cada nodo como un objeto con 26 hijos: en Python gasta
      mucha memoria y tiempo; usar dicts o listas paralelas.
    - Recursión para recorrer el trie con palabras de 10^5 letras: usar
      pila explícita.
    - En la DP de segmentar, probar todas las palabras en cada posición
      (O(|s|·m·L)) en vez de bajar por el trie.

VARIANTES Y RELACIONADOS
    - Trie binario (bits de enteros): máximo XOR de un par en O(n·30).
    - Ordenar palabras = recorrido en preorden con hijos en orden.
    - Con enlaces de falla para buscar muchos patrones en un texto:
      aho_corasick.py. Prefijo común de todo el diccionario: prefijo_comun.py.

DÓNDE PRACTICAR
    - ICPC/Colombia 2024/E - Spacebar Tokenizer (DP sobre prefijos + trie de
      tokens)
    - CSES «Word Combinations» (formas_de_partir); LeetCode 208 «Implement
      Trie (Prefix Tree)»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (lista de palabras con count y
      startswith; DP probando cada palabra) en 600 secuencias aleatorias de
      operaciones (45000 consultas) + 1000 segmentaciones + casos borde
      (python trie.py)
"""
import random


class Trie:
    def __init__(self):
        self.hijos = [{}]       # hijos[v][letra] -> nodo
        self.fin = [0]          # palabras que terminan exactamente en v
        self.pasan = [0]        # palabras que pasan por v (prefijo = camino a v)

    def insertar(self, palabra):
        v = 0
        self.pasan[0] += 1
        for c in palabra:
            u = self.hijos[v].get(c)
            if u is None:
                u = len(self.hijos)
                self.hijos[v][c] = u
                self.hijos.append({})
                self.fin.append(0)
                self.pasan.append(0)
            v = u
            self.pasan[v] += 1
        self.fin[v] += 1

    def _nodo(self, prefijo):
        """Nodo al que lleva prefijo, o -1 si ese camino no existe."""
        v = 0
        for c in prefijo:
            v = self.hijos[v].get(c, -1)
            if v == -1:
                return -1
        return v

    def contar_palabra(self, palabra):
        v = self._nodo(palabra)
        return self.fin[v] if v != -1 else 0

    def contar_prefijo(self, prefijo):
        v = self._nodo(prefijo)
        return self.pasan[v] if v != -1 else 0

    def eliminar(self, palabra):
        """Quita una aparición de palabra; los nodos quedan (con pasan = 0)."""
        if self.contar_palabra(palabra) == 0:
            return False
        v = 0
        self.pasan[0] -= 1
        for c in palabra:
            v = self.hijos[v][c]
            self.pasan[v] -= 1
        self.fin[v] -= 1
        return True

    def palabras_desde(self, s, i):
        """Largos L (crecientes) tales que s[i:i+L] es palabra del trie."""
        res = []
        v = 0
        for j in range(i, len(s)):
            v = self.hijos[v].get(s[j], -1)
            if v == -1:
                break               # ninguna palabra continúa por aquí
            if self.fin[v] > 0:
                res.append(j - i + 1)
        return res


def formas_de_partir(s, diccionario, mod=10**9 + 7):
    """Maneras de escribir s como concatenación de palabras del diccionario."""
    t = Trie()
    for p in set(diccionario):          # repetidas no cuentan como formas distintas
        if p:
            t.insertar(p)
    n = len(s)
    formas = [0] * (n + 1)              # formas[i] = maneras de partir s[:i]
    formas[0] = 1
    for i in range(n):
        if formas[i]:
            for L in t.palabras_desde(s, i):
                formas[i + L] = (formas[i + L] + formas[i]) % mod
    return formas[n]


def demo():
    t = Trie()
    for p in ["a", "ab", "abc", "b"]:
        t.insertar(p)
    print("palabras: a, ab, abc, b")
    print("contar_prefijo('ab') =", t.contar_prefijo("ab"))        # 2
    print("contar_prefijo('') =", t.contar_prefijo(""))            # 4
    print("contar_palabra('abc') =", t.contar_palabra("abc"))      # 1
    print("palabras_desde('abcd', 0) =", t.palabras_desde("abcd", 0))  # [1, 2, 3]
    t.eliminar("ab")
    print("tras eliminar 'ab': contar_prefijo('ab') =", t.contar_prefijo("ab"))  # 1
    print("formas_de_partir('abab', [a, b, ab]) =", formas_de_partir("abab", ["a", "b", "ab"]))  # 4


def pruebas():
    random.seed(808)

    # Casos borde
    t = Trie()
    assert t.contar_prefijo("") == 0 and t.contar_palabra("") == 0
    assert not t.eliminar("x")
    t.insertar("")
    assert t.contar_palabra("") == 1 and t.contar_prefijo("") == 1
    assert formas_de_partir("", ["a"]) == 1
    assert formas_de_partir("abc", []) == 0
    assert formas_de_partir("aaaa", ["a", "aa"]) == 5      # Fibonacci

    # Secuencias aleatorias de operaciones contra una lista simple
    consultas = 0
    for _ in range(600):
        t = Trie()
        bolsa = []
        alfabeto = random.choice(["ab", "abc"])
        for _ in range(25):
            p = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 4)))
            op = random.random()
            if op < 0.5:
                t.insertar(p)
                bolsa.append(p)
            elif op < 0.7:
                esperado = p in bolsa
                assert t.eliminar(p) == esperado
                if esperado:
                    bolsa.remove(p)
            assert t.contar_palabra(p) == bolsa.count(p)
            assert t.contar_prefijo(p) == sum(1 for w in bolsa if w.startswith(p))
            s = "".join(random.choice(alfabeto) for _ in range(6))
            i = random.randint(0, 6)
            assert t.palabras_desde(s, i) == [L for L in range(1, 7 - i) if s[i:i + L] in bolsa]
            consultas += 3
    assert consultas == 45000

    # Segmentaciones contra DP que prueba cada palabra
    for _ in range(1000):
        alfabeto = random.choice(["a", "ab", "abc"])
        dic = ["".join(random.choice(alfabeto) for _ in range(random.randint(1, 3)))
               for _ in range(random.randint(0, 6))]
        s = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 12)))
        f = [1] + [0] * len(s)
        for i in range(1, len(s) + 1):
            f[i] = sum(f[i - len(w)] for w in set(dic) if s[:i].endswith(w))
        assert formas_de_partir(s, dic) == f[-1] % (10**9 + 7)

    # Grande: 100 palabras de hasta 100 letras y un texto de 5000 letras
    dic = ["a" * k for k in range(1, 101)]
    assert formas_de_partir("a" * 3, dic) == 4
    assert formas_de_partir("a" * 5000, dic) > 0


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
