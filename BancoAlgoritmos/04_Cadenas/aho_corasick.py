"""
Cadenas — Aho–Corasick: muchos patrones a la vez («Aho–Corasick automaton»)
Nivel: Avanzado
Ejecutar: python aho_corasick.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Buscar MUCHOS patrones en un texto en una sola pasada: cuántas veces
    aparece cada patrón, o dónde aparece cada uno. Es «KMP sobre un trie»:
    cuesta O(|texto| + Σ|patrones|) (más el número de apariciones si se
    listan), en lugar de una búsqueda KMP por patrón.
    Señales en el enunciado: «un diccionario de k palabras prohibidas /
    virus / genes» y un texto largo; «cuántas veces aparece cada una»;
    «el texto no debe contener ninguna de estas palabras» (DP sobre los
    estados del autómata); Σ|patrones| y |texto| hasta 10^5–10^6.

FUNCIÓN
    AhoCorasick(patrones)               patrones NO vacíos (pueden repetirse)
        .contar(texto) -> list[int]
            cnt[k] = apariciones (solapadas) de patrones[k] en texto, en
            O(|texto| + nodos), sin importar cuántas apariciones haya.
        .buscar_todas(texto) -> list[(inicio, k)]
            Todas las apariciones, ordenadas por posición final y, en la
            misma posición final, de patrón más largo a más corto.
        .contiene_alguno(texto) -> bool

IDEA Y ALGORITMO
    1) Trie de los patrones: cada nodo es un prefijo de algún patrón.
    2) Enlace de falla fail[v]: el nodo del SUFIJO PROPIO más largo de v
       que también es prefijo de algún patrón (igual que pi de KMP, pero
       saltando entre ramas del trie). Se calcula por BFS (por niveles):
       para el hijo u = v + c, se sigue la cadena de fallas de v hasta un
       nodo f que tenga hijo c; fail[u] = ese hijo (o la raíz). Funciona
       porque todos los nodos de menor profundidad ya tienen su falla.
    3) Recorrido del texto: el estado actual es el prefijo de patrón más
       largo que es sufijo de lo leído. Al leer c, si no hay hijo c se
       baja por fallas (como en KMP) y luego se avanza.
    4) En un estado v terminan TODOS los patrones que son sufijo de v: los
       de v y los de su cadena de fallas. Para contar sin recorrer esa
       cadena en cada paso: se suma 1 a visitas[v] y al final se propaga
       visitas[v] a visitas[fail[v]] en orden de BFS inverso (de lo más
       profundo a la raíz). Para listar, se usa el enlace de salida
       salida[v] = el nodo más cercano en la cadena de fallas donde
       termina algún patrón, y así solo se visitan nodos útiles.
    Ingenuo: buscar cada patrón por separado, O(k·|texto|) aunque cada
    búsqueda sea lineal: con k = 10^4 patrones ya no alcanza.

MACROALGORITMO
    1. Insertar todos los patrones en un trie; anotar el nodo final de cada uno.
    2. BFS desde la raíz: hijos de la raíz tienen falla 0.
    3. Para cada hijo u = v·c: f = fail[v]; mientras f ≠ 0 y no hay hijo c en
       f: f = fail[f]. fail[u] = hijo c de f (si existe y no es u), si no 0.
    4. salida[u] = fail[u] si allí termina un patrón, si no salida[fail[u]].
    5. Recorrer el texto con las transiciones (bajando por fallas si falta
       el hijo) y sumar 1 a visitas del estado.
    6. Contar: en BFS inverso, visitas[fail[v]] += visitas[v]; la respuesta
       del patrón k es visitas[nodo_final[k]].

COMPLEJIDAD
    Construcción O(Σ|p|) (con dict de hijos; O(Σ|p|·Σ) con tabla completa).
    contar: O(|texto| + nodos). buscar_todas: O(|texto| + apariciones).
    Memoria O(Σ|p|). En Python, ~10^6 caracteres de texto por segundo.

EJEMPLO A MANO
    patrones = ["he", "she", "his", "hers"]; texto = "ushers"
      nodos: h(1) he(2) s(3) sh(4) she(5) hi(6) his(7) her(8) hers(9)
      fallas: sh→h, she→he, his→s, hers→s, demás→raíz
      u: raíz | s: s(3) | h: sh(4) | e: she(5) → termina "she" y por falla
      "he" | r: she no tiene 'r' → falla he(2) → her(8) | s: hers(9) ✓
    contar = [1, 1, 0, 1]; buscar_todas = [(1, 1), (2, 0), (2, 3)]

ERRORES TÍPICOS
    - Calcular las fallas con DFS: el nodo de falla puede no estar listo.
      Debe ser BFS (por profundidad).
    - Al encontrar un estado, contar solo los patrones que terminan en él y
      olvidar los de su cadena de fallas ("he" dentro de "she").
    - Recorrer la cadena de fallas completa en cada carácter para contar:
      O(|texto|·profundidad). Propagar al final o usar enlaces de salida.
    - Patrones repetidos: guardar una LISTA de índices por nodo, no uno solo.

VARIANTES Y RELACIONADOS
    - Autómata completo (goto[v][c] para todo c) para DP: «cadenas de largo
      n que no contienen ningún patrón» = DP sobre (posición, estado).
    - Árbol de fallas: las apariciones de p son los estados en el
      subárbol de su nodo (consultas con Euler tour + Fenwick).
    - Un solo patrón: kmp.py. Solo el trie: trie.py.
    - Muchos patrones como subcadenas: también suffix_automaton.py.

DÓNDE PRACTICAR
    - CSES «Finding Patterns», «Counting Patterns», «Pattern Positions»
    - (Ningún problema del repo ICPC lo necesita: Colombia 2024/E usa
      solo el trie, porque basta bajar desde cada posición.)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (buscar cada patrón en cada posición)
      en 2000 casos aleatorios con patrones repetidos y anidados + casos
      borde + un caso grande (python aho_corasick.py)
"""
import random
from collections import deque


class AhoCorasick:
    def __init__(self, patrones):
        self.hijos = [{}]           # trie: hijos[v][c] -> nodo
        self.fin = [[]]             # índices de patrones que terminan en v
        self.nodo_de = []           # nodo final de cada patrón
        for k, p in enumerate(patrones):
            assert p, "los patrones deben ser no vacíos"
            v = 0
            for c in p:
                u = self.hijos[v].get(c)
                if u is None:
                    u = len(self.hijos)
                    self.hijos[v][c] = u
                    self.hijos.append({})
                    self.fin.append([])
                v = u
            self.fin[v].append(k)
            self.nodo_de.append(v)
        self.largo = [len(p) for p in patrones]

        n = len(self.hijos)
        self.fail = [0] * n
        self.salida = [0] * n       # siguiente nodo en la cadena de fallas con fin no vacío
        self.orden = []             # nodos en orden BFS (sin la raíz)
        cola = deque(self.hijos[0].values())    # hijos de la raíz: falla = raíz
        while cola:
            v = cola.popleft()
            self.orden.append(v)
            for c, u in self.hijos[v].items():
                # Sufijo propio más largo de u que es prefijo: extender una falla de v.
                f = self.fail[v]
                while f and c not in self.hijos[f]:
                    f = self.fail[f]
                self.fail[u] = self.hijos[f].get(c, 0)
                g = self.fail[u]
                self.salida[u] = g if self.fin[g] else self.salida[g]
                cola.append(u)

    def _estados(self, texto):
        """Estado del autómata después de leer cada carácter del texto."""
        hijos, fail = self.hijos, self.fail
        v = 0
        for c in texto:
            while v and c not in hijos[v]:
                v = fail[v]             # como KMP: probar un sufijo más corto
            v = hijos[v].get(c, 0)
            yield v

    def contar(self, texto):
        """Apariciones de cada patrón, propagando visitas por el árbol de fallas."""
        visitas = [0] * len(self.hijos)
        for v in self._estados(texto):
            visitas[v] += 1
        # De lo más profundo a la raíz: todo lo que termina en v también
        # termina en su falla (que es sufijo de v).
        for v in reversed(self.orden):
            visitas[self.fail[v]] += visitas[v]
        return [visitas[v] for v in self.nodo_de]

    def buscar_todas(self, texto):
        """Lista de (inicio, índice de patrón) de todas las apariciones."""
        res = []
        for i, v in enumerate(self._estados(texto)):
            u = v if self.fin[v] else self.salida[v]
            while u:                    # solo nodos donde termina algún patrón
                for k in self.fin[u]:
                    res.append((i - self.largo[k] + 1, k))
                u = self.salida[u]
        return res

    def contiene_alguno(self, texto):
        return any(self.fin[v] or self.salida[v] for v in self._estados(texto))


def demo():
    patrones = ["he", "she", "his", "hers"]
    texto = "ushers"
    ac = AhoCorasick(patrones)
    print("patrones =", patrones, " texto =", repr(texto))
    print("contar:", ac.contar(texto))                   # [1, 1, 0, 1]
    print("buscar_todas:", ac.buscar_todas(texto))       # [(1, 1), (2, 0), (2, 3)]
    print("contiene_alguno('hola'):", ac.contiene_alguno("hola"))   # False


def pruebas():
    random.seed(1975)

    def ocurrencias(t, p):
        return [i for i in range(len(t) - len(p) + 1) if t[i:i + len(p)] == p]

    # Casos borde
    ac = AhoCorasick(["a"])
    assert ac.contar("") == [0] and ac.buscar_todas("") == []
    assert ac.contar("aaa") == [3]
    ac = AhoCorasick(["aa", "aa", "a"])     # repetidos
    assert ac.contar("aaa") == [2, 2, 3]
    assert AhoCorasick([]).contar("abc") == []

    for _ in range(2000):
        alfabeto = random.choice(["a", "ab", "abc"])
        patrones = ["".join(random.choice(alfabeto) for _ in range(random.randint(1, 4)))
                    for _ in range(random.randint(1, 8))]
        texto = "".join(random.choice(alfabeto) for _ in range(random.randint(0, 25)))
        ac = AhoCorasick(patrones)
        assert ac.contar(texto) == [len(ocurrencias(texto, p)) for p in patrones]
        todas = sorted(ac.buscar_todas(texto))
        assert todas == sorted((i, k) for k, p in enumerate(patrones) for i in ocurrencias(texto, p))
        assert ac.contiene_alguno(texto) == bool(todas)

    # Grande: 2000 patrones, texto de 2·10^5
    patrones = ["".join(random.choice("ab") for _ in range(random.randint(1, 12))) for _ in range(2000)]
    texto = "".join(random.choice("ab") for _ in range(200000))
    cnt = AhoCorasick(patrones).contar(texto)
    for k in random.sample(range(2000), 20):
        p = patrones[k]
        assert cnt[k] == sum(1 for i in range(len(texto) - len(p) + 1) if texto.startswith(p, i))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
