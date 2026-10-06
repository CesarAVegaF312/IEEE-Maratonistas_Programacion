"""
Cadenas — Paréntesis balanceados con pila («Balanced brackets / stack parsing»)
Nivel: Básico
Ejecutar: python parentesis_pila.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Todo lo que tiene estructura ANIDADA se procesa con una pila: verificar
    que los paréntesis cierren bien, encontrar la pareja de cada uno, medir
    la profundidad de anidamiento, evaluar expresiones aritméticas o
    reconstruir un árbol escrito como f(g(x), y).
    Señales en el enunciado: «paréntesis / corchetes / llaves», «bien
    formada», «anidado», «expresión», «término», «etiquetas que abren y
    cierran», profundidades de hasta 10^5 (la recursión de Python no aguanta).

FUNCIÓN
    balanceado(s) -> bool           con (), [] y {}; otros caracteres se ignoran
    emparejar(s) -> list[int] | None
        par[i] = índice del que cierra/abre a s[i] (-1 si s[i] no es
        paréntesis); None si s no está balanceada.
    profundidad_maxima(s) -> int    máximo de paréntesis '(' abiertos a la vez
    max_parejas(s) -> int           máximo de parejas '()' de una SUBSECUENCIA
                                    balanceada (borrando caracteres)
    evaluar(expr) -> int            enteros no negativos, + - * y paréntesis

IDEA Y ALGORITMO
    El paréntesis que cierra siempre corresponde al ÚLTIMO que se abrió y
    sigue sin cerrar: eso es exactamente una pila (LIFO). Al leer uno que
    abre se apila; al leer uno que cierra, el tope debe ser de su mismo
    tipo y se desapila. La cadena está balanceada si nunca se intentó
    desapilar una pila vacía (o de otro tipo) y al final la pila queda vacía.
    La profundidad es el tamaño de la pila; con un solo tipo basta un
    contador.
    max_parejas: voraz con contador. Cada ')' se empareja con cualquier '('
    abierto antes (si lo hay). Emparejar en cuanto se pueda nunca empeora:
    un ')' que se queda sin pareja no tenía ningún '(' libre a su izquierda.
    Expresiones (Dijkstra, «shunting-yard»): dos pilas, números y operadores.
    Antes de apilar un operador se aplican los del tope con precedencia
    mayor o igual (igual ⇒ asociatividad izquierda); '(' es una barrera y
    ')' aplica todo hasta su '('. Así se respeta * antes que + sin recursión.

MACROALGORITMO
    1. pila = []. Recorrer s de izquierda a derecha.
    2. Si c abre: apilar (c, posición).
    3. Si c cierra: si la pila está vacía o el tope no es su pareja → no
       balanceada; si no, desapilar y anotar la pareja de ambas posiciones.
    4. Al final: balanceada ⇔ la pila está vacía.
    5. Expresión: número → pila de valores; '(' → apilar; ')' → aplicar
       hasta '('; operador → aplicar mientras el tope tenga precedencia ≥,
       luego apilarlo. Al final aplicar todo lo que quede.

COMPLEJIDAD
    Todo O(n) en tiempo y O(n) de memoria (la pila). Sin recursión: aguanta
    anidamientos de 10^6. En Python, ~10^6 caracteres por segundo.

EJEMPLO A MANO
    s = "{[()()]}" (posiciones 0..7)
      '{' apila 0 | '[' apila 1 | '(' apila 2 | ')' desapila 2 → par 2-3
      '(' apila 4 | ')' desapila 4 → par 4-5 | ']' desapila 1 → par 1-6
      '}' desapila 0 → par 0-7; pila vacía → balanceada, profundidad 3.
    evaluar("2*(3+4)-5"): valores [2] ops [*] → '(' → [2,3] [*,(,+] →
      [2,3,4] → ')' aplica + → [2,7] [*] → '-' aplica * → [14] [-] →
      [14,5] → fin aplica - → 9

ERRORES TÍPICOS
    - Contar solo «abiertos == cerrados»: ")(" tiene la misma cantidad y no
      está balanceada (el contador nunca debe bajar de 0).
    - No verificar el TIPO del tope: "([)]" no está balanceada.
    - Olvidar revisar que la pila quede vacía al final: "((" no cierra.
    - Parsear con recursión en Python: con 10^5 niveles revienta la pila
      (o hay que subir el límite y aún así puede fallar).
    - En expresiones, olvidar que '-' es asociativo a la izquierda:
      8-3-2 = 3, no 7 (por eso se aplica también con precedencia IGUAL).

VARIANTES Y RELACIONADOS
    - Subcadena balanceada más larga: pila de índices con un -1 de base.
    - Mínimo de inserciones para balancear: abiertos sin cerrar + ')' sin pareja.
    - Contar secuencias balanceadas de largo 2n: números de Catalan.
    - Pila monótona (siguiente mayor, histograma) es otra familia de pila.
    - Árboles escritos con paréntesis: numeración canónica (hash-consing).

DÓNDE PRACTICAR
    - ICPC/Colombia 2023/E - LISP Extravaganza (emparejamiento voraz con
      contador = max_parejas)
    - ICPC/Colombia 2017/C - Compact Terms (análisis de términos con pila
      explícita)
    - UVa 673 «Parentheses Balance»; Codeforces 5C «Longest Regular Bracket
      Sequence»; LeetCode 20 «Valid Parentheses»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (borrar "()" repetidamente, buscar la
      pareja con un contador, probar todas las subsecuencias, eval de
      Python) en 3000 + 2000 casos aleatorios + casos borde
      (python parentesis_pila.py)
"""
import random

ABRE = {")": "(", "]": "[", "}": "{"}      # cierre -> su apertura


def emparejar(s):
    """par[i] = posición de la pareja de s[i] (-1 si no es paréntesis); None si no balancea."""
    par = [-1] * len(s)
    pila = []                       # posiciones de aperturas aún sin cerrar
    for i, c in enumerate(s):
        if c in "([{":
            pila.append(i)
        elif c in ABRE:
            # El que cierra debe corresponder a la ÚLTIMA apertura pendiente.
            if not pila or s[pila[-1]] != ABRE[c]:
                return None
            j = pila.pop()
            par[i], par[j] = j, i
    return par if not pila else None   # sobran aperturas sin cerrar


def balanceado(s):
    """True si (), [] y {} están bien anidados en s."""
    return emparejar(s) is not None


def profundidad_maxima(s):
    """Máximo de '(' abiertos simultáneamente (s se asume balanceada)."""
    prof = mejor = 0
    for c in s:
        if c == "(":
            prof += 1
            mejor = max(mejor, prof)
        elif c == ")":
            prof -= 1
    return mejor


def max_parejas(s):
    """Máximo de parejas en una subsecuencia balanceada de '(' y ')'."""
    abiertos = parejas = 0
    for c in s:
        if c == "(":
            abiertos += 1
        elif c == ")" and abiertos > 0:
            abiertos -= 1           # se empareja con cualquier '(' libre
            parejas += 1
    return parejas


PRIORIDAD = {"+": 1, "-": 1, "*": 2}


def evaluar(expr):
    """Evalúa enteros no negativos con + - * y paréntesis (shunting-yard)."""
    valores, ops = [], []

    def aplicar():
        b = valores.pop()
        a = valores.pop()
        op = ops.pop()
        valores.append(a + b if op == "+" else a - b if op == "-" else a * b)

    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c.isdigit():
            j = i
            while j < n and expr[j].isdigit():
                j += 1
            valores.append(int(expr[i:j]))
            i = j
            continue
        if c == "(":
            ops.append(c)
        elif c == ")":
            while ops[-1] != "(":
                aplicar()
            ops.pop()               # quitar el '('
        elif c in PRIORIDAD:
            # Precedencia >= (no solo >) para que - y + asocien a la izquierda.
            while ops and ops[-1] != "(" and PRIORIDAD[ops[-1]] >= PRIORIDAD[c]:
                aplicar()
            ops.append(c)
        i += 1                      # espacios y lo demás se ignoran
    while ops:
        aplicar()
    return valores[-1]


def demo():
    s = "{[()()]}"
    print("s =", s)
    print("balanceado:", balanceado(s))                    # True
    print("emparejar:", emparejar(s))                      # [7, 6, 3, 2, 5, 4, 1, 0]
    print("balanceado('([)]'):", balanceado("([)]"))       # False
    print("profundidad_maxima('(()(()))'):", profundidad_maxima("(()(()))"))  # 3
    print("max_parejas(')(()(('):", max_parejas(")(()(("))                     # 1
    print("evaluar('2*(3+4)-5') =", evaluar("2*(3+4)-5"))  # 9


def pruebas():
    random.seed(31)

    def balanceado_bruto(s):
        # Borrar parejas vecinas hasta que no cambie: queda "" ⇔ balanceada.
        s = "".join(c for c in s if c in "()[]{}")
        while True:
            t = s.replace("()", "").replace("[]", "").replace("{}", "")
            if t == s:
                return s == ""
            s = t

    def max_parejas_bruto(s):
        n, mejor = len(s), 0
        for mask in range(1 << n):
            t = "".join(s[i] for i in range(n) if mask >> i & 1)
            if balanceado_bruto(t):
                mejor = max(mejor, len(t) // 2)
        return mejor

    # Casos borde
    assert balanceado("") and emparejar("") == []
    assert not balanceado(")(") and not balanceado("((") and not balanceado("([)]")
    assert emparejar("a(b)c") == [-1, 3, -1, 1, -1]
    assert profundidad_maxima("") == 0 and max_parejas("") == 0
    assert evaluar("8-3-2") == 3 and evaluar("2+3*4") == 14 and evaluar("((7))") == 7

    for _ in range(3000):
        n = random.randint(0, 12)
        s = "".join(random.choice("()[]{}x" if random.random() < 0.5 else "()")
                    for _ in range(n))
        assert balanceado(s) == balanceado_bruto(s)
        par = emparejar(s)
        if par is not None and set(s) <= set("()"):
            prof = 0
            for i, c in enumerate(s):
                if c == "(":
                    # pareja = primer j > i donde el contador vuelve al nivel de i
                    k, j = 0, i
                    while True:
                        k += 1 if s[j] == "(" else -1
                        if k == 0:
                            break
                        j += 1
                    assert par[i] == j and par[j] == i
                    prof += 1
                else:
                    prof -= 1
            assert profundidad_maxima(s) == max([0] + [s[:i].count("(") - s[:i].count(")")
                                                      for i in range(n + 1)])
        t = "".join(random.choice("()") for _ in range(random.randint(0, 11)))
        assert max_parejas(t) == max_parejas_bruto(t)

    # Expresiones aleatorias contra eval de Python
    def expresion(prof):
        r = random.random()
        if prof == 0 or r < 0.3:
            return str(random.randint(0, 20))
        if r < 0.45:
            return "(" + expresion(prof - 1) + ")"
        return expresion(prof - 1) + random.choice(["+", "-", "*", " - ", " * "]) + expresion(prof - 1)

    for _ in range(2000):
        e = expresion(random.randint(0, 5))
        assert evaluar(e) == eval(e), e

    # Anidamiento enorme sin recursión
    s = "(" * 100000 + ")" * 100000
    assert balanceado(s) and profundidad_maxima(s) == 100000
    assert evaluar("(" * 50000 + "1+2" + ")" * 50000) == 3


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
