"""
Voraz — Mochila fraccionaria («Fractional knapsack»)
Nivel: Básico
Ejecutar: python mochila_fraccionaria.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Llenar una mochila de capacidad W con objetos de valor v_i y peso w_i
    maximizando el valor, cuando se puede tomar una FRACCIÓN de cada objeto
    (polvo de oro, litros de combustible, kilos de especias).
    Señales en el enunciado: «se puede tomar cualquier cantidad / parte»,
    mercancía divisible, respuesta con decimales o como fracción. Si los
    objetos son indivisibles («se toma o no se toma») es la mochila 0/1 y
    el voraz NO sirve (hace falta DP).

FUNCIÓN
    mochila_fraccionaria(objetos, capacidad) -> (Fraction, list[Fraction])
        objetos: lista de pares (valor, peso) con peso > 0 y valor >= 0,
        enteros (o Fraction). Devuelve el valor máximo EXACTO y, por objeto
        (en el orden de entrada), la fracción tomada en [0, 1].

IDEA Y ALGORITMO
    Ordenar por valor por unidad de peso (v_i / w_i) de mayor a menor y
    llenar: tomar completos los objetos mientras quepan y del primero que
    no quepa, la fracción que llena exactamente la mochila.
    Por qué es óptimo (argumento de intercambio): supongamos una solución
    que deja espacio usado por un objeto de densidad menor d_b mientras
    queda sin tomar parte de un objeto de densidad mayor d_a. Cambiar ε de
    peso de b por ε de peso de a no altera el peso total y sube el valor en
    ε·(d_a − d_b) >= 0. Repitiendo, cualquier óptimo se transforma en la
    solución voraz sin perder valor.
    Por qué Fraction: con flotantes, v/w se redondea y dos densidades
    iguales pueden «desempatar» mal, y la respuesta acumula error. Con
    fractions.Fraction todo es exacto (más lento, pero N suele ser pequeño;
    para N grande se compara v_a·w_b > v_b·w_a con enteros al ordenar).
    El ingenuo de probar subconjuntos es O(2^N) y además no cubre las
    fracciones; el voraz es O(N log N).

MACROALGORITMO
    1. Ordenar índices por v_i / w_i decreciente.
    2. restante = W, total = 0.
    3. Para cada objeto en ese orden, mientras restante > 0:
       a. Si w_i <= restante: tomarlo entero (total += v_i, restante -= w_i).
       b. Si no: tomar restante / w_i de él (total += v_i · restante / w_i)
          y parar.
    4. Devolver total y las fracciones.

COMPLEJIDAD
    O(N log N) por el ordenamiento, O(N) memoria. Con Fraction, unas
    10^5 operaciones por segundo; con comparación entera, N = 10^6 en ~1 s.

EJEMPLO A MANO
    W = 50; objetos (valor, peso): A (60, 10), B (100, 20), C (120, 30)
    densidades: A = 6, B = 5, C = 4 → orden A, B, C
      A entero: total 60,  restante 40
      B entero: total 160, restante 20
      C: 20/30 = 2/3 → total 160 + 120·2/3 = 240.          Respuesta: 240.
    (En la mochila 0/1 el óptimo sería B + C = 220, y el voraz por
    densidad daría A + B = 160: por eso ahí no sirve.)

ERRORES TÍPICOS
    - Usarlo para la mochila 0/1 (ver ejemplo: da 160 en vez de 220).
    - Ordenar por valor o por peso en lugar de por densidad v/w.
    - Densidades con flotantes y comparar con ==; mejor Fraction o
      multiplicación cruzada v_a·w_b vs v_b·w_a.
    - Objetos de peso 0 (si el enunciado los permite): tomarlos siempre
      antes del ordenamiento, para no dividir entre 0.

VARIANTES Y RELACIONADOS
    - Mochila 0/1 y acotada: programación dinámica
      (03_ProgramacionDinamica/mochila_01.py).
    - Branch & bound de la mochila 0/1: la cota superior de cada nodo es
      justamente esta mochila fraccionaria.
    - «Máxima densidad media» con restricción de tamaño: búsqueda binaria
      sobre la respuesta (00_Base/busqueda_binaria.py).
    - 02_Voraz/argumento_intercambio.py: la técnica de prueba usada aquí.

DÓNDE PRACTICAR
    - (No hay problemas del repo ICPC/ que usen esta técnica.)
    - Es la base de la cota del branch & bound para mochila 0/1.

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta en 1500 casos aleatorios (N <= 7):
      se prueba todo subconjunto que cabe completo más, a lo sumo, un objeto
      fraccionado (el óptimo de un programa lineal de este tipo siempre
      tiene esa forma); además se valida que las fracciones sumen el valor
      y respeten la capacidad (python mochila_fraccionaria.py)
"""
import random
from fractions import Fraction


def mochila_fraccionaria(objetos, capacidad):
    """Valor máximo (Fraction exacta) y fracción tomada de cada objeto."""
    n = len(objetos)
    # Densidad exacta v/w como Fraction: el orden y los empates son exactos.
    orden = sorted(range(n), key=lambda i: Fraction(objetos[i][0], objetos[i][1]),
                   reverse=True)
    fracciones = [Fraction(0)] * n
    total = Fraction(0)
    restante = Fraction(capacidad)
    for i in orden:
        if restante <= 0:
            break
        v, w = objetos[i]
        if w <= restante:               # cabe entero
            fracciones[i] = Fraction(1)
            total += v
            restante -= w
        else:                           # solo cabe una parte: la mochila queda llena
            fracciones[i] = restante / w
            total += v * fracciones[i]
            restante = Fraction(0)
    return total, fracciones


def demo():
    objetos = [(60, 10), (100, 20), (120, 30)]
    total, fr = mochila_fraccionaria(objetos, 50)
    print("objetos (valor, peso) =", objetos, " W = 50")
    print("fracciones =", [str(f) for f in fr])          # 1, 1, 2/3
    print("valor máximo =", total)                       # 240


def _fuerza_bruta(objetos, capacidad):
    n = len(objetos)
    mejor = Fraction(0)
    for mascara in range(1 << n):
        peso = sum(objetos[i][1] for i in range(n) if mascara >> i & 1)
        if peso > capacidad:
            continue
        valor = Fraction(sum(objetos[i][0] for i in range(n) if mascara >> i & 1))
        mejor = max(mejor, valor)
        libre = capacidad - peso
        for j in range(n):              # a lo sumo un objeto fraccionado
            if not mascara >> j & 1:
                v, w = objetos[j]
                mejor = max(mejor, valor + v * min(Fraction(1), Fraction(libre, w)))
    return mejor


def pruebas():
    random.seed(99)

    # Casos borde
    assert mochila_fraccionaria([], 10) == (0, [])
    assert mochila_fraccionaria([(5, 3)], 0)[0] == 0
    assert mochila_fraccionaria([(5, 3)], 100)[0] == 5
    assert mochila_fraccionaria([(7, 3)], 1)[0] == Fraction(7, 3)
    assert mochila_fraccionaria([(4, 2), (4, 2), (4, 2)], 3)[0] == 6   # todos iguales
    assert mochila_fraccionaria([(60, 10), (100, 20), (120, 30)], 50)[0] == 240

    # Aleatorios contra fuerza bruta
    for _ in range(1500):
        n = random.randint(0, 7)
        objetos = [(random.randint(0, 20), random.randint(1, 10)) for _ in range(n)]
        cap = random.randint(0, 40)
        total, fr = mochila_fraccionaria(objetos, cap)
        assert total == _fuerza_bruta(objetos, cap)
        # Coherencia de las fracciones devueltas
        assert all(0 <= f <= 1 for f in fr)
        assert sum(f * w for f, (v, w) in zip(fr, objetos)) <= cap
        assert sum(f * v for f, (v, w) in zip(fr, objetos)) == total


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
