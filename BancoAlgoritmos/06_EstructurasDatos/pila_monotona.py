"""
Estructuras de datos — Pila monótona («Monotonic stack»)
Nivel: Intermedio
Ejecutar: python pila_monotona.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Para cada posición i de un arreglo, encontrar en O(N) TOTAL el primer
    elemento a la derecha (o izquierda) que es mayor (o menor) que a[i].
    Con eso salen: rectángulo de área máxima en un histograma, «cuántos
    días hasta una temperatura más alta», «qué edificio ve cada uno»,
    rango donde a[i] es el mínimo (suma de mínimos de subarreglos), etc.
    Señales en el enunciado: «el siguiente / el anterior mayor (menor)»,
    «hasta dónde se extiende», «visibilidad», histogramas, N hasta 10^6
    (descarta el O(N²) de buscar hacia la derecha desde cada i).

FUNCIÓN
    siguiente_mayor(a) -> list[int]
        sig[i] = menor j > i con a[j] > a[i]; -1 si no hay.
    anterior_menor(a) -> list[int]
        ant[i] = mayor j < i con a[j] < a[i]; -1 si no hay.
    rectangulo_maximo(h) -> int
        Área del mayor rectángulo dentro del histograma de alturas h
        (barras de ancho 1, alturas >= 0). 0 si h está vacío.

IDEA Y ALGORITMO
    SIGUIENTE MAYOR: recorrer de izquierda a derecha con una pila de
    índices «que aún esperan» a su siguiente mayor. Invariante: los valores
    en la pila son NO CRECIENTES de abajo hacia arriba (por eso «monótona»).
    Al llegar a[j], todo índice de la cima con valor < a[j] acaba de
    encontrar a su siguiente mayor (es j: es el primero, porque los que
    estaban en medio ya habían salido o no eran mayores); se desapilan y
    luego se apila j. Si la cima es >= a[j], nadie debajo puede ser menor
    (por la monotonía), así que se para.
    Por qué es O(N): cada índice entra y sale de la pila a lo sumo una vez;
    el while interno suma N iteraciones en total (análisis amortizado).
    RECTÁNGULO MÁXIMO: el rectángulo óptimo tiene la altura de alguna barra
    i (la más baja que contiene) y se extiende desde el anterior menor de
    i hasta el siguiente menor (exclusivos): ancho = der[i] - izq[i] - 1.
    Con una pila creciente se obtienen ambos en una sola pasada: cuando
    a[j] < a[cima], j es el siguiente menor de la cima y el nuevo tope de
    la pila es su anterior menor (o igual: con alturas repetidas solo el
    último de un grupo da el ancho completo, y basta con eso).
    Un centinela de altura 0 al final vacía la pila sin código extra.

MACROALGORITMO
    Siguiente mayor:
    1. sig = [-1]·N, pila vacía.
    2. Para j = 0..N-1: mientras pila y a[pila.top] < a[j]: sig[pop] = j.
    3. Apilar j.  (Los que quedan en la pila no tienen siguiente mayor.)
    Rectángulo máximo:
    1. Agregar altura 0 al final; pila vacía; mejor = 0.
    2. Para j: mientras pila y h[top] >= h[j]: i = pop;
       izquierda = nuevo top (o -1); mejor = max(mejor, h[i]·(j - izquierda - 1)).
    3. Apilar j. Devolver mejor.

COMPLEJIDAD
    O(N) tiempo y memoria (amortizado). En Python, N = 10^6 en ~0,5–1 s.

EJEMPLO A MANO
    a = [2, 1, 2, 4, 3]:  siguiente_mayor
      j=0 (2): pila [0]
      j=1 (1): 2 < 1 no → pila [0,1]
      j=2 (2): a[1]=1 < 2 → sig[1]=2; a[0]=2 < 2 no → pila [0,2]
      j=3 (4): sig[2]=3, sig[0]=3 → pila [3]
      j=4 (3): 4 < 3 no → pila [3,4]       → sig = [3, 2, 3, -1, -1]
    h = [2, 1, 5, 6, 2, 3]: rectángulo máximo = 10 (alturas 5 y 6, alto 5,
    ancho 2): al llegar el 2 (j=4) sale el 6 (área 6·1) y el 5 (área 5·2).

ERRORES TÍPICOS
    - Confundir < con <= en el while: cambia «estrictamente mayor» por
      «mayor o igual» (con valores repetidos da otro resultado).
    - Guardar VALORES en la pila en lugar de índices (luego no se puede
      calcular el ancho ni la posición).
    - Olvidar vaciar la pila al final (el centinela 0 lo evita).
    - En el histograma, calcular el ancho con j - i en vez de
      j - izquierda - 1.

VARIANTES Y RELACIONADOS
    - Recorrer de derecha a izquierda para «anterior mayor».
    - Suma de mínimos de todos los subarreglos: Σ a[i]·(i - izq)·(der - i)
      con desempate estricto en un lado y no estricto en el otro.
    - Mayor rectángulo de unos en una matriz binaria: histograma por fila.
    - Ventana deslizante de máximo: cola monótona (deque).
    - Pila monótona con «rollback» en un DFS (como en Alice's Travels II).
    - Para consultas de mínimo en rango arbitrarias:
      06_EstructurasDatos/sparse_table.py o segment_tree.py.

DÓNDE PRACTICAR
    - ICPC/Guangzhou 2017/A - Alice's Travels II (pilas monótonas por costo,
      con rollback durante un DFS)
    - CSES «Nearest Smaller Values»; CSES «Advertisement» (histograma).
    - LeetCode 84 «Largest Rectangle in Histogram»; LeetCode 739 «Daily
      Temperatures».

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta O(N²) / O(N³) en 2000 casos aleatorios
      con muchos valores repetidos (N <= 25), casos borde y N = 2·10^5
      monótono (peor caso de la pila) (python pila_monotona.py)
"""
import random


def siguiente_mayor(a):
    """sig[i] = primer j > i con a[j] > a[i], o -1."""
    sig = [-1] * len(a)
    pila = []                    # índices sin respuesta; valores no crecientes
    for j, x in enumerate(a):
        while pila and a[pila[-1]] < x:
            sig[pila.pop()] = j  # x es el primer mayor para la cima
        pila.append(j)
    return sig


def anterior_menor(a):
    """ant[i] = último j < i con a[j] < a[i], o -1."""
    ant = [-1] * len(a)
    pila = []                    # candidatos; valores estrictamente crecientes
    for i, x in enumerate(a):
        while pila and a[pila[-1]] >= x:
            pila.pop()           # nunca serán «anterior menor» de nadie a la derecha de i
        ant[i] = pila[-1] if pila else -1
        pila.append(i)
    return ant


def rectangulo_maximo(h):
    """Área máxima de un rectángulo dentro del histograma h."""
    mejor = 0
    pila = []                    # índices con alturas crecientes
    hs = list(h) + [0]           # centinela: vacía la pila al final
    for j, x in enumerate(hs):
        while pila and hs[pila[-1]] >= x:
            i = pila.pop()
            izq = pila[-1] if pila else -1     # anterior menor de i
            # j es el siguiente menor (o igual) de i: el rectángulo de altura
            # hs[i] cubre (izq, j) exclusivo.
            area = hs[i] * (j - izq - 1)
            if area > mejor:
                mejor = area
        pila.append(j)
    return mejor


def demo():
    a = [2, 1, 2, 4, 3]
    print("a =", a)
    print("siguiente_mayor =", siguiente_mayor(a))       # [3, 2, 3, -1, -1]
    print("anterior_menor  =", anterior_menor(a))        # [-1, -1, 1, 2, 2]
    h = [2, 1, 5, 6, 2, 3]
    print("histograma", h, "-> área máxima", rectangulo_maximo(h))   # 10


def pruebas():
    random.seed(84)

    # Casos borde
    assert siguiente_mayor([]) == [] and anterior_menor([]) == []
    assert rectangulo_maximo([]) == 0
    assert siguiente_mayor([5]) == [-1] and rectangulo_maximo([5]) == 5
    assert siguiente_mayor([3, 3, 3]) == [-1, -1, -1]   # estrictamente mayor
    assert rectangulo_maximo([3, 3, 3]) == 9
    assert rectangulo_maximo([0, 0]) == 0

    for _ in range(2000):
        n = random.randint(0, 25)
        a = [random.randint(0, 6) for _ in range(n)]
        assert siguiente_mayor(a) == [next((j for j in range(i + 1, n) if a[j] > a[i]), -1)
                                      for i in range(n)]
        assert anterior_menor(a) == [next((j for j in range(i - 1, -1, -1) if a[j] < a[i]), -1)
                                     for i in range(n)]
        bruta = max((min(a[i:j + 1]) * (j - i + 1) for i in range(n) for j in range(i, n)),
                    default=0)
        assert rectangulo_maximo(a) == bruta

    # Peor caso para la pila (monótono) con N grande
    n = 200000
    assert siguiente_mayor(list(range(n, 0, -1))) == [-1] * n
    assert rectangulo_maximo(list(range(1, n + 1))) == max(i * (n - i + 1) for i in range(1, n + 1))


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
