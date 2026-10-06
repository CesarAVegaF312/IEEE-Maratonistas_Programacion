"""
Base — Simulación paso a paso («Simulation / ad hoc»)
Nivel: Básico
Ejecutar: python simulacion.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Hacer exactamente lo que dice el enunciado, paso a paso, con estructuras
    de datos que hagan cada paso barato. No hay truco matemático: la
    dificultad está en modelar bien el ESTADO, no equivocarse en las reglas
    y estimar que el número de pasos alcanza.
    Señales en el enunciado: reglas detalladas de un proceso («en cada
    turno…», «mientras…», «si… entonces…»), un juego, una máquina, una
    cola; N pequeño (≤ 100–1000) o un número de pasos acotado.
    Ejemplo clásico: cola de impresora con prioridades (UVa 12100).

FUNCIÓN
    cola_impresora(prioridades, m) -> int
        prioridades[i] ∈ 1..9 del trabajo i (en orden de la cola).
        Devuelve el minuto en que se imprime el trabajo m (desde 0): cada
        impresión tarda 1 minuto y mover trabajos no toma tiempo.
    Regla (UVa 12100): se toma el trabajo del frente; si hay ALGUNO en la
    cola con prioridad mayor, se manda al final sin imprimir; si no, se
    imprime.

IDEA Y ALGORITMO
    1. ESTADO mínimo que determina el futuro: la cola de (índice, prioridad)
       y cuántos trabajos quedan de cada prioridad.
    2. PASO: mirar el frente, decidir, actualizar el estado.
    3. FIN: cuando se imprime el trabajo m.
    La pregunta «¿hay alguno con prioridad mayor?» hecha a lo ingenuo
    recorre la cola: O(N) por paso. Como las prioridades son 1..9, se
    guarda cuenta[p] = cuántos trabajos con prioridad p quedan, y la
    pregunta cuesta O(9). La cola es una deque (popleft y append O(1)).
    ¿Cuántos pasos? Antes de cada impresión hay a lo sumo N rotaciones
    (tras una vuelta completa, el de mayor prioridad llega al frente), y hay
    a lo sumo N impresiones: O(N²) pasos. Con N ≤ 100 son 10^4: sobra.
    Regla general: estimar el número de pasos ANTES de programar; si es
    enorme (10^9 turnos), buscar un ciclo o saltar varios pasos a la vez.

MACROALGORITMO
    1. Elegir la representación del estado (cola, tablero, contadores…).
    2. Armar el estado inicial a partir de la entrada.
    3. Mientras no se cumpla la condición de fin:
    4.    Leer lo necesario del estado (frente de la cola, máxima prioridad).
    5.    Aplicar la regla que corresponda (rotar o imprimir).
    6.    Actualizar contadores auxiliares (cuenta[p], minuto).
    7. Devolver lo pedido.
    8. Probar a mano con el ejemplo y con casos borde (un solo elemento,
       todos iguales).

COMPLEJIDAD
    Cola de impresora: O(N²·9) en el peor caso (todas rotaciones), memoria
    O(N). En general: (número de pasos) × (costo de un paso); en Python
    calcular con ~10^7 operaciones simples por segundo.

EJEMPLO A MANO
    prioridades = [1, 1, 9, 1, 1, 1], m = 0 (el primer 1):
      cola: 0(1) 1(1) 2(9) 3(1) 4(1) 5(1)
      0(1): hay 9 → al final;  1(1): hay 9 → al final
      2(9): no hay mayor → imprime (minuto 1)
      3(1), 4(1), 5(1) se imprimen (minutos 2, 3, 4)
      0(1) se imprime en el minuto 5   → respuesta 5

ERRORES TÍPICOS
    - Modelar mal una regla por leer rápido (¿«mayor» o «mayor o igual»?).
    - Contar el tiempo de los movimientos que no lo consumen (o al revés).
    - Perder la identidad del elemento buscado: guardar (índice, valor),
      no solo el valor (hay prioridades repetidas).
    - Simular cuando el número de pasos es astronómico: estimarlo antes.
    - Modificar una lista mientras se recorre con for.

VARIANTES Y RELACIONADOS
    - Simulación con detección de ciclo (estado repetido → saltar).
    - Simulación por eventos (ordenar eventos por tiempo con un heap).
    - Josefo con deque.rotate: pila_cola_deque.py.
    - Tablas de posiciones: ordenamiento_clave_compuesta.py.

DÓNDE PRACTICAR
    - 2025-2/maraton_problemas/p12100_printer_queue.py (UVa 12100 «Printer Queue»)
    - 2025-2/maraton_problemas/p10050_hartals.py (UVa 10050 «Hartals»)
    - ICPC/Colombia 2017/H - Hip-n (simulación con tablero aplanado)
    - ICPC/Colombia 2017/K - Soccer Championship (simulación + ordenamiento)
    - ICPC/Colombia 2018/A - All-star Three-point Contest (simulación + ordenamiento)
    - ICPC/OMP 2017 Murcia/G - Recomputing Dependencies (simulación directa)

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta (simulación literal con una lista,
      pop(0) y any() sobre toda la cola) en 2000 casos aleatorios + casos
      borde y el ejemplo del enunciado (python simulacion.py)
"""
import random
from collections import deque


def cola_impresora(prioridades, m):
    """Minuto en que se imprime el trabajo m (UVa 12100)."""
    cola = deque(enumerate(prioridades))      # (índice original, prioridad)
    cuenta = [0] * 10                         # cuenta[p] = trabajos pendientes con prioridad p
    for p in prioridades:
        cuenta[p] += 1
    minuto = 0
    while True:
        i, p = cola.popleft()
        # ¿queda algún trabajo con prioridad mayor? O(9) gracias a cuenta[]
        if any(cuenta[q] for q in range(p + 1, 10)):
            cola.append((i, p))               # al final, sin gastar tiempo
        else:
            minuto += 1                       # imprimir cuesta 1 minuto
            cuenta[p] -= 1
            if i == m:
                return minuto


def demo():
    print("Ejemplo del enunciado de UVa 12100:")
    for prios, m in [([5], 0), ([1, 2, 3, 4], 2), ([1, 1, 9, 1, 1, 1], 0)]:
        print("  prioridades =", prios, " m =", m, " → minuto", cola_impresora(prios, m))
    # salidas esperadas: 1, 2, 5


def _bruta(prioridades, m):
    """Simulación literal del enunciado, sin ninguna optimización."""
    cola = [(i, p) for i, p in enumerate(prioridades)]
    minuto = 0
    while True:
        i, p = cola.pop(0)
        hay_mayor = False
        for _, q in cola:
            if q > p:
                hay_mayor = True
        if hay_mayor:
            cola.append((i, p))
        else:
            minuto += 1
            if i == m:
                return minuto


def pruebas():
    random.seed(12100)

    # Ejemplo del enunciado y bordes
    assert cola_impresora([5], 0) == 1
    assert cola_impresora([1, 2, 3, 4], 2) == 2
    assert cola_impresora([1, 1, 9, 1, 1, 1], 0) == 5
    assert cola_impresora([3, 3, 3], 2) == 3          # todos iguales: orden de llegada
    assert cola_impresora([1, 9], 0) == 2

    for _ in range(2000):
        n = random.randint(1, 25)
        prios = [random.randint(1, random.choice([2, 9])) for _ in range(n)]
        m = random.randrange(n)
        assert cola_impresora(prios, m) == _bruta(prios, m)

    # Peor caso aproximado (N = 100) debe ser instantáneo
    prios = [random.randint(1, 9) for _ in range(100)]
    assert cola_impresora(prios, 0) == _bruta(prios, 0)


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
