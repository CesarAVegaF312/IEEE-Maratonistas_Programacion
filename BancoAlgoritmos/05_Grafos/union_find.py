"""
Grafos — Union-Find / conjuntos disjuntos («Disjoint Set Union, DSU»)
Nivel: Intermedio
Ejecutar: python union_find.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Mantener una partición de n elementos en grupos que solo se UNEN (nunca
    se separan), respondiendo «¿a y b están en el mismo grupo?» y «¿qué
    tamaño tiene el grupo de a?» en tiempo casi constante.
    Señales en el enunciado: «se van agregando conexiones / amistades /
    carreteras» y entre medio preguntan conectividad; «cuántos grupos quedan
    después de cada operación»; Kruskal (mst.py); «A es amigo de B y B de C ⇒
    A de C»; equivalencias que se propagan. Si hay que BORRAR aristas,
    procesar al revés (agregando) si se puede.

FUNCIÓN
    class DSU(n):
        encontrar(x) -> int     representante (raíz) del grupo de x
        unir(a, b) -> bool      une los grupos; False si ya estaban juntos
        mismo(a, b) -> bool     ¿mismo grupo?
        tamano(x) -> int        tamaño del grupo de x
        grupos                  cantidad actual de grupos
    Elementos 0..n-1.

IDEA Y ALGORITMO
    Cada grupo es un árbol; padre[x] apunta hacia la raíz y la raíz es el
    representante. Dos elementos están juntos ⇔ tienen la misma raíz. Unir
    = colgar una raíz de la otra.
    Sin cuidado los árboles degeneran en caminos (O(n) por consulta). Dos
    mejoras:
      · Unión por tamaño: colgar el árbol PEQUEÑO del grande. Un elemento
        baja un nivel solo cuando su grupo al menos se duplica, así que la
        altura es ≤ log2 n.
      · Compresión de caminos: al buscar la raíz de x, hacer que todos los
        nodos del camino apunten DIRECTO a la raíz. Las búsquedas siguientes
        son casi O(1).
    Juntas dan O(α(n)) amortizado por operación (α = inversa de Ackermann,
    ≤ 4 para cualquier n real). Se implementa ITERATIVO (dos pasadas: subir
    a la raíz, luego reapuntar): la versión recursiva de encontrar puede
    pasar de 1000 niveles antes de comprimirse si no se une por tamaño.

MACROALGORITMO
    1. padre[i] = i, tam[i] = 1, grupos = n.
    2. encontrar(x): subir por padre hasta la raíz r; volver a recorrer el
       camino poniendo padre[·] = r; devolver r.
    3. unir(a, b): ra, rb = raíces; si son iguales, False.
    4. Si tam[ra] < tam[rb], intercambiar; padre[rb] = ra; tam[ra] += tam[rb];
       grupos −= 1; True.

COMPLEJIDAD
    O(α(n)) amortizado por operación, O(n) memoria. En Python ~10^6
    operaciones por segundo.

EJEMPLO A MANO
    n = 6. unir(0,1): raíz 0, tam 2. unir(2,3): raíz 2. unir(1,3): raíces
    0 y 2, mismo tamaño → padre[2] = 0, tam[0] = 4. unir(0,2): ya juntos →
    False. Grupos: {0,1,2,3}, {4}, {5} → 3 grupos; tamano(3) = 4;
    encontrar(3) sube 3→2→0 y deja padre[3] = 0 (comprimido).

ERRORES TÍPICOS
    - Hacer padre[a] = b en vez de padre[raíz(a)] = raíz(b): no une los grupos.
    - Leer tam[x] de un elemento que no es raíz (tam solo es válido en raíces).
    - encontrar recursivo sin unión por tamaño: RecursionError con cadenas largas.
    - Querer «separar» grupos: el DSU no lo soporta (procesar offline al
      revés o usar DSU con rollback).

VARIANTES Y RELACIONADOS
    - DSU con paridad / pesos: guardar la diferencia con el padre (bipartición
      en línea, restricciones «a − b = c»).
    - DSU con rollback (sin compresión) para dividir y conquistar offline.
    - Kruskal: mst.py. Componentes estáticas: componentes_conexas.py.
    - Ciclo en no dirigido: unir(u, v) devuelve False ⇒ la arista cierra un
      ciclo (deteccion_ciclos.py).

DÓNDE PRACTICAR
    - ICPC/Colombia 2018/C - Carrol's Scrabble (union-find sobre cubetas)
    - ICPC/Colombia 2024/J - Lumina (alternativa a BFS para contar componentes)
    - CSES «Road Construction» (grupos y tamaño máximo tras cada arista)
    - UVa 10583 «Ubiquitous Religions», UVa 11503 «Virtual Friends»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (arreglo de etiquetas que se reescribe
      completo en cada unión) en 1000 secuencias aleatorias de 60 operaciones,
      más una cadena de 200000 uniones sin recursión (python union_find.py)
"""
import random


class DSU:
    def __init__(self, n):
        self.padre = list(range(n))   # padre[i] == i  ⇔  i es raíz
        self.tam = [1] * n            # válido solo en las raíces
        self.grupos = n

    def encontrar(self, x):
        padre = self.padre
        r = x
        while padre[r] != r:          # 1) subir hasta la raíz
            r = padre[r]
        while padre[x] != r:          # 2) compresión: todo el camino apunta a r
            padre[x], x = r, padre[x]
        return r

    def unir(self, a, b):
        ra, rb = self.encontrar(a), self.encontrar(b)
        if ra == rb:
            return False
        if self.tam[ra] < self.tam[rb]:   # colgar el pequeño del grande
            ra, rb = rb, ra
        self.padre[rb] = ra
        self.tam[ra] += self.tam[rb]
        self.grupos -= 1
        return True

    def mismo(self, a, b):
        return self.encontrar(a) == self.encontrar(b)

    def tamano(self, x):
        return self.tam[self.encontrar(x)]


def demo():
    d = DSU(6)
    for a, b in [(0, 1), (2, 3), (1, 3), (0, 2)]:
        print(f"unir({a}, {b}) ->", d.unir(a, b))      # True True True False
    print("grupos:", d.grupos)                           # 3
    print("tamano(3):", d.tamano(3))                     # 4
    print("¿0 y 5 juntos?", d.mismo(0, 5))               # False
    print("padre tras comprimir:", d.padre)


def pruebas():
    random.seed(11503)
    casos = 0

    d = DSU(1)
    assert d.encontrar(0) == 0 and not d.unir(0, 0) and d.grupos == 1 and d.tamano(0) == 1

    # Cadena larga: unir siempre el nuevo con el anterior (sin recursión)
    n = 200000
    d = DSU(n)
    for i in range(1, n):
        assert d.unir(i - 1, i)
    assert d.grupos == 1 and d.tamano(n - 1) == n and d.mismo(0, n - 1)

    for _ in range(1000):
        n = random.randint(1, 12)
        d = DSU(n)
        etiqueta = list(range(n))       # fuerza bruta: etiqueta de grupo explícita
        for _ in range(60):
            a, b = random.randrange(n), random.randrange(n)
            if random.random() < 0.5:
                juntos = etiqueta[a] == etiqueta[b]
                assert d.unir(a, b) == (not juntos)
                if not juntos:
                    viejo, nuevo = etiqueta[b], etiqueta[a]
                    etiqueta = [nuevo if e == viejo else e for e in etiqueta]
            else:
                assert d.mismo(a, b) == (etiqueta[a] == etiqueta[b])
                assert d.tamano(a) == etiqueta.count(etiqueta[a])
            assert d.grupos == len(set(etiqueta))
        casos += 1
    return casos


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
