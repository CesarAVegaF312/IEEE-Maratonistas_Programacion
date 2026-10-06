"""
Base — Pila, cola y deque en Python («Stack, queue, deque»)
Nivel: Básico
Ejecutar: python pila_cola_deque.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Pila (LIFO, el último que entra sale primero): paréntesis, deshacer,
    evaluar expresiones, vías de tren sin salida, «el anterior menor».
    Cola (FIFO, el primero que entra sale primero): turnos, BFS, procesos
    en orden de llegada. Deque: ambas puntas en O(1) (rotar, ventanas).
    Señales en el enunciado: «el último que llegó sale primero», un andén
    o vía muerta, anidamiento (paréntesis, etiquetas), «en orden de
    llegada», «pasa al final de la fila», círculo de personas que se
    eliminan cada k.

FUNCIÓN
    rails(orden) -> bool
        UVa 514: los vagones 1..n llegan en ese orden desde A; la estación
        es una vía muerta (pila). ¿Pueden salir hacia B en el orden dado?
    balanceada(s) -> bool
        ¿Los ()[]{} de s están bien anidados? (ignora otros caracteres)
    anterior_menor(a) -> list
        Para cada i, el índice j < i más cercano con a[j] < a[i]; −1 si no hay.
    josefo(n, k) -> list
        Orden en que se eliminan las personas 1..n en círculo, contando de
        k en k (se elimina la k-ésima, y se sigue contando desde la siguiente).

IDEA Y ALGORITMO
    En Python:
      pila : lista;  push = append(x), pop = pop(), tope = p[-1]   (O(1))
      cola : collections.deque;  append(x) y popleft()             (O(1))
             (NUNCA lista.pop(0): mueve todo, es O(N))
      deque: append / appendleft / pop / popleft / rotate(k)
    Rails: el vagón que debe salir ahora es «objetivo». Si está en el tope
    de la estación, sale. Si no, hay que meter vagones de A hasta que
    llegue el objetivo; si ya entró y NO está en el tope, quedó tapado por
    otro que entró después y es imposible (en una pila solo se saca el
    tope). La simulación es forzada (no hay decisiones): por eso basta
    hacerla una vez.
    Pila monótona (anterior menor): se mantiene una pila de índices con
    valores crecientes. Al llegar a[i], se sacan los que tengan valor
    ≥ a[i]: nunca serán «el anterior menor» de nadie posterior, porque
    a[i] es menor o igual y está más cerca. Lo que queda en el tope es la
    respuesta. Cada índice entra y sale una vez: O(N).
    Josefo: deque con rotate(-(k-1)) lleva al frente al k-ésimo y popleft
    lo elimina. O(n·k) en total.

MACROALGORITMO
    (Rails)
    1. siguiente = 1 (próximo vagón que llega de A); estacion = [].
    2. Para cada objetivo del orden pedido:
    3.    Mientras siguiente <= objetivo: apilar siguiente; siguiente += 1.
    4.    Si el tope es objetivo: desapilar; si no: imposible.
    5. Si se procesaron todos: posible.

COMPLEJIDAD
    rails, balanceada, anterior_menor: O(N). josefo: O(n·k).
    Operaciones de pila/deque en Python: ~10^7 por segundo.

EJEMPLO A MANO
    rails([5, 4, 1, 2, 3]) con n = 5:
      objetivo 5: entran 1 2 3 4 5 → tope 5 ✓ sale → estación [1 2 3 4]
      objetivo 4: tope 4 ✓ sale → [1 2 3]
      objetivo 1: ya entró pero el tope es 3 ✗ → «No»
    rails([5, 4, 3, 2, 1]) → «Yes».
    josefo(7, 3) = [3, 6, 2, 7, 5, 1, 4]

ERRORES TÍPICOS
    - Usar lista.pop(0) o insert(0, x) como cola: O(N) por operación.
    - Leer el tope de una pila vacía (p[-1] lanza IndexError): comprobar antes.
    - En paréntesis, olvidar que al final la pila debe quedar VACÍA.
    - Rails: el formato de UVa 514 tiene bloques terminados en 0 y una
      línea vacía entre bloques en la salida.
    - Josefo: confundir el conteo desde 0 o desde 1 (probar con n pequeño).

VARIANTES Y RELACIONADOS
    - Siguiente mayor / área máxima en histograma: pila monótona.
    - Máximo en ventana: deque monótona (ventana_deslizante.py).
    - BFS: cola (deque); 0-1 BFS: deque con appendleft para peso 0.
    - Evaluar expresiones (shunting-yard) con dos pilas.
    - Simulación con cola: simulacion.py (UVa 12100).

DÓNDE PRACTICAR
    - 2026-1/problemas/514 - Rails.pdf (UVa 514 «Rails»)
    - 2025-2/maraton_problemas/p12100_printer_queue.py (cola con deque)
    - ICPC/Colombia 2017/C - Compact Terms (análisis con pila explícita)
    - ICPC/Colombia 2023/E - LISP Extravaganza (contador equivalente a una pila de '(')
    - UVa 673 «Parentheses Balance»; CSES «Nearest Smaller Values»,
      «Josephus Problem I»

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (rails: búsqueda exhaustiva de todas
      las secuencias de meter/sacar; paréntesis: borrar pares «()» hasta no
      poder; anterior menor: recorrido hacia atrás; Josefo: lista con pop)
      en 3000 casos aleatorios + casos borde (python pila_cola_deque.py)
"""
import itertools
import random
from collections import deque


def rails(orden):
    """¿Pueden salir los vagones 1..n en 'orden' usando una vía muerta (pila)?"""
    estacion = []               # pila: el tope es estacion[-1]
    siguiente = 1               # próximo vagón que llega desde A
    for objetivo in orden:
        while siguiente <= objetivo:
            estacion.append(siguiente)      # meter hasta que entre el objetivo
            siguiente += 1
        if estacion and estacion[-1] == objetivo:
            estacion.pop()                  # sale hacia B
        else:
            return False                    # está tapado por otro vagón
    return True


def balanceada(s):
    """¿Los paréntesis ()[]{} de s están bien anidados?"""
    pareja = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in s:
        if c in "([{":
            pila.append(c)
        elif c in pareja:
            if not pila or pila.pop() != pareja[c]:
                return False                # cierre sin apertura o de otro tipo
    return not pila                         # no deben quedar aperturas pendientes


def anterior_menor(a):
    """Para cada i, el j < i más cercano con a[j] < a[i]; -1 si no hay."""
    pila = []                   # índices con valores estrictamente crecientes
    res = []
    for i, v in enumerate(a):
        while pila and a[pila[-1]] >= v:
            pila.pop()          # v los tapa para todos los posteriores
        res.append(pila[-1] if pila else -1)
        pila.append(i)
    return res


def josefo(n, k):
    """Orden de eliminación de 1..n en círculo eliminando cada k-ésimo."""
    circulo = deque(range(1, n + 1))
    orden = []
    while circulo:
        circulo.rotate(-(k - 1))            # los k-1 primeros pasan al final
        orden.append(circulo.popleft())     # el k-ésimo sale
    return orden


def demo():
    for o in ([1, 2, 3, 4, 5], [5, 4, 1, 2, 3], [5, 4, 3, 2, 1], [3, 1, 2]):
        print("rails(", o, ") =", "Yes" if rails(o) else "No")
    print("balanceada('([]{})') =", balanceada("([]{})"), "  balanceada('([)]') =", balanceada("([)]"))
    print("anterior_menor([2, 5, 1, 4, 8, 3]) =", anterior_menor([2, 5, 1, 4, 8, 3]))
    print("josefo(7, 3) =", josefo(7, 3))                 # [3, 6, 2, 7, 5, 1, 4]


# ---------- fuerzas brutas ----------

def _rails_bruta(orden):
    """Explora TODAS las secuencias de acciones (meter de A / sacar a B)."""
    n = len(orden)
    pendientes = [((), 1, 0)]               # (estación, siguiente de A, cuántos salieron)
    while pendientes:
        est, sig, k = pendientes.pop()
        if k == n:
            return True
        if sig <= n:
            pendientes.append((est + (sig,), sig + 1, k))
        if est and est[-1] == orden[k]:
            pendientes.append((est[:-1], sig, k + 1))
    return False


def _balanceada_bruta(s):
    s = "".join(c for c in s if c in "()[]{}")
    antes = None
    while antes != s:
        antes = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""


def pruebas():
    random.seed(514)

    # Casos borde
    assert rails([]) and rails([1])
    assert rails([1, 2, 3]) and not rails([3, 1, 2])
    assert balanceada("") and not balanceada("(") and not balanceada(")(")
    assert anterior_menor([]) == [] and anterior_menor([3, 3, 3]) == [-1, -1, -1]
    assert josefo(1, 5) == [1] and josefo(5, 1) == [1, 2, 3, 4, 5]

    # Rails: todas las permutaciones de n <= 6
    for n in range(1, 7):
        for p in itertools.permutations(range(1, n + 1)):
            assert rails(list(p)) == _rails_bruta(list(p))

    for _ in range(3000):
        s = "".join(random.choice("()[]{}x") for _ in range(random.randint(0, 10)))
        assert balanceada(s) == _balanceada_bruta(s)

        n = random.randint(0, 15)
        a = [random.randint(0, 5) for _ in range(n)]
        bruta = [next((j for j in range(i - 1, -1, -1) if a[j] < a[i]), -1) for i in range(n)]
        assert anterior_menor(a) == bruta

        n, k = random.randint(1, 12), random.randint(1, 15)
        personas, pos, orden = list(range(1, n + 1)), 0, []
        while personas:
            pos = (pos + k - 1) % len(personas)
            orden.append(personas.pop(pos))
        assert josefo(n, k) == orden


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
