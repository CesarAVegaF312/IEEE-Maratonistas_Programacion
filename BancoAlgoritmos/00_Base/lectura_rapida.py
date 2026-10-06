r"""
Base — Lectura rápida de la entrada («Fast I/O»)
Nivel: Básico
Ejecutar: python lectura_rapida.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Leer TODA la entrada de una vez y recorrerla por tokens. En Python,
    llamar input() 10^6 veces tarda varios segundos; leer de golpe tarda
    décimas. Además resuelve de forma uniforme los formatos típicos de
    maratón: «T casos», «hasta fin de archivo (EOF)», «hasta una línea con
    0», números repartidos en varias líneas.
    Señales: entrada grande (≥ 10^5 números), formato de casos múltiples,
    «la entrada termina con…», o un TLE con una solución que debería pasar.

FUNCIÓN (todas reciben los bytes de la entrada para poder probarlas)
    casos_con_t(datos) -> list[int]
        Formato: T, y por caso «N a1 … aN». Devuelve la suma de cada caso.
    hasta_eof(datos) -> list[int]
        Formato: pares «a b» hasta que se acabe la entrada. Devuelve a + b.
    hasta_cero(datos) -> list[int]
        Formato: «N a1 … aN» repetido; termina con N = 0. Devuelve el máximo.
    por_lineas(datos) -> list[tuple[str, int]]
        Formato con espacios dentro del dato: «nombre;puntos» por línea
        (líneas vacías se ignoran). Devuelve (nombre, puntos).
    resolver(datos) -> bytes
        Plantilla completa: lee, resuelve (casos_con_t) y arma la salida.
    main()   lee sys.stdin.buffer y escribe sys.stdout (no se llama en las
             pruebas: el archivo se ejecuta sin entrada).

IDEA Y ALGORITMO
    sys.stdin.buffer.read() devuelve TODA la entrada como bytes en una sola
    llamada al sistema. .split() sin argumentos separa por CUALQUIER
    espacio en blanco (espacios, tabs, \n, \r\n) y descarta vacíos: da igual
    cómo estén repartidos los números en líneas. Un iterador sobre los
    tokens (next(it)) reemplaza a input().
    int() acepta bytes directamente (int(b"42") == 42); para texto,
    .decode(). Ojo: los tokens son bytes, así que se comparan con b"0", no
    con "0".
    - T casos: leer T y hacer for _ in range(T).
    - Hasta EOF: iterar «for x in it» o capturar StopIteration; con pares,
      zip(it, it) toma dos tokens a la vez y se detiene solo al final.
    - Terminador 0: leer N; si es 0, break.
    - Si un dato tiene espacios (nombres), leer por LÍNEAS:
      datos.decode().splitlines().
    Salida: acumular las respuestas en una lista y escribir una sola vez
    con "\n".join(...). print() en un bucle de 10^5 iteraciones es lento.

MACROALGORITMO
    1. datos = sys.stdin.buffer.read()
    2. it = iter(datos.split())
    3. Leer cada número con int(next(it)) siguiendo el formato.
    4. Detectar el fin: T casos / EOF (StopIteration o zip) / terminador.
    5. Guardar cada respuesta como texto en una lista.
    6. sys.stdout.write("\n".join(salida) + "\n").

COMPLEJIDAD
    O(tamaño de la entrada). 10^6 enteros: read+split ~0,1 s, int() ~0,1 s.
    Con input() serían ~1 s solo de lectura. Memoria: toda la entrada en
    RAM (decenas de MB está bien; si son cientos, leer por partes).

EJEMPLO A MANO
    datos = b"2\n3 1 2 3\n2\n10 20\n"   (el segundo caso tiene los números
    en otra línea: split() no lo nota)
      tokens: [b'2', b'3', b'1', b'2', b'3', b'2', b'10', b'20']
      T=2; caso 1: N=3 → 1+2+3 = 6; caso 2: N=2 → 10+20 = 30
    → [6, 30]

ERRORES TÍPICOS
    - Comparar un token bytes con str: b"0" == "0" es False (bucle infinito
      o nunca termina).
    - Leer por líneas cuando los números de un caso pueden venir partidos
      en varias líneas (o al revés: usar split() con nombres que tienen
      espacios).
    - Windows: las líneas terminan en \r\n; split() lo maneja, pero
      split("\n") deja un \r pegado. Usar splitlines().
    - Imprimir con print dentro de un bucle enorme; o olvidar el \n final.
    - Mezclar input() con sys.stdin.read() en el mismo programa.

VARIANTES Y RELACIONADOS
    - input = sys.stdin.readline (más rápido que input(), pero hay que
      quitar el \n con .strip() o rstrip()).
    - Leer una matriz de caracteres: [next(it) for _ in range(n)] (bytes;
      fila[j] da un entero, el código ASCII).
    - map(int, datos.split()) para convertir todo de una vez si todo son
      números.
    - Todas las soluciones del repo usan este patrón.

DÓNDE PRACTICAR
    - ICPC/Colombia 2026/D - Bingwhenever (entrada de ~20 MB, lee caso por caso)
    - ICPC/Colombia 2025/A - Account Qualifying (casos hasta N = 0)
    - ICPC/Colombia 2018/A - All-star Three-point Contest (lectura por líneas,
      nombres con espacios y separador ';')
    - 2025-2/maraton_problemas/p11413_fill_containers.py (casos hasta EOF con zip)

VERIFICACIÓN
    - Pruebas: OK contra un lector «ingenuo» línea por línea (readline
      sobre io.StringIO, como haría input()) en 2000 entradas aleatorias,
      y contra la misma entrada con los espacios y saltos de línea
      reordenados al azar + casos borde (python lectura_rapida.py)
"""
import io
import random
import sys


def casos_con_t(datos):
    """T casos de «N a1 ... aN»; devuelve la suma de cada caso."""
    it = iter(datos.split())
    t = int(next(it))
    res = []
    for _ in range(t):
        n = int(next(it))
        res.append(sum(int(next(it)) for _ in range(n)))
    return res


def hasta_eof(datos):
    """Pares «a b» hasta el fin de la entrada; devuelve a + b de cada par."""
    it = iter(datos.split())
    # zip(it, it) toma dos tokens seguidos del MISMO iterador y para en EOF
    return [int(a) + int(b) for a, b in zip(it, it)]


def hasta_cero(datos):
    """Casos «N a1 ... aN» hasta N = 0; devuelve el máximo de cada caso."""
    it = iter(datos.split())
    res = []
    for tok in it:
        n = int(tok)            # int(b"0") == 0: comparar el NÚMERO, no el token
        if n == 0:
            break
        res.append(max(int(next(it)) for _ in range(n)))
    return res


def por_lineas(datos):
    """Líneas «nombre con espacios;puntos»; ignora líneas vacías."""
    res = []
    for linea in datos.decode().splitlines():      # splitlines maneja \r\n
        linea = linea.strip()
        if not linea:
            continue
        nombre, puntos = linea.rsplit(";", 1)
        res.append((nombre.strip(), int(puntos)))
    return res


def resolver(datos):
    """Plantilla: entrada (bytes) -> salida (bytes) del problema «T casos»."""
    salida = [str(s) for s in casos_con_t(datos)]
    return ("\n".join(salida) + "\n").encode()


def main():
    """Lo que se envía al juez (aquí no se ejecuta: no hay entrada)."""
    datos = sys.stdin.buffer.read()
    sys.stdout.write(resolver(datos).decode())


def demo():
    d1 = b"2\n3 1 2 3\n2\n10 20\n"
    print("casos_con_t:", casos_con_t(d1))                        # [6, 30]
    print("hasta_eof:", hasta_eof(b"1 2\n3 4\n5 6"))              # [3, 7, 11]
    print("hasta_cero:", hasta_cero(b"3 4 9 2\n1 -5\n0\n"))        # [9, -5]
    print("por_lineas:", por_lineas(b"Ana Maria;30\r\n\r\nJuan;12\r\n"))
    print("resolver:", resolver(d1))


# ---------- lector ingenuo (línea por línea, como input()) ----------

def _ingenuo_t(texto):
    f = io.StringIO(texto)
    t = int(f.readline())
    res = []
    for _ in range(t):
        n = int(f.readline())
        nums = list(map(int, f.readline().split()))   # con N = 0 la línea va vacía
        assert len(nums) == n
        res.append(sum(nums))
    return res


def _revolver(texto):
    """Mismos tokens con separadores aleatorios (espacios, tabs, \\r\\n...)."""
    seps = [" ", "  ", "\n", "\r\n", "\t", " \n "]
    return (random.choice(["", "\n"]) + "".join(tok + random.choice(seps) for tok in texto.split())).encode()


def pruebas():
    random.seed(2718)

    # Casos borde
    assert casos_con_t(b"0") == []
    assert casos_con_t(b"1\n0\n") == [0]
    assert hasta_eof(b"") == [] and hasta_eof(b"\n\n") == []
    assert hasta_cero(b"0") == [] and hasta_cero(b"0\n5 1 2 3 4 5") == []
    assert hasta_cero(b"1 7") == [7]                 # sin terminador: para en EOF
    assert por_lineas(b"") == []
    assert por_lineas(b"  a b ; 3  \n") == [("a b", 3)]
    assert b"0" != "0"                               # el error típico

    for _ in range(2000):
        casos = [[random.randint(-10**9, 10**9) for _ in range(random.randint(0, 6))]
                 for _ in range(random.randint(0, 5))]
        lineas = [str(len(casos))]
        for c in casos:
            lineas.append(str(len(c)))
            lineas.append(" ".join(map(str, c)))
        texto = "\n".join(lineas) + "\n"
        esperado = [sum(c) for c in casos]
        assert _ingenuo_t(texto) == esperado
        assert casos_con_t(texto.encode()) == esperado
        assert casos_con_t(_revolver(texto)) == esperado          # da igual el espaciado
        assert resolver(texto.encode()) == ("\n".join(map(str, esperado)) + "\n").encode()

        pares = [(random.randint(-99, 99), random.randint(-99, 99)) for _ in range(random.randint(0, 5))]
        tp = "\n".join(f"{a} {b}" for a, b in pares)
        assert hasta_eof(_revolver(tp) if tp else b"") == [a + b for a, b in pares]

        cz = [[random.randint(-50, 50) for _ in range(random.randint(1, 5))] for _ in range(random.randint(0, 4))]
        tz = "".join(f"{len(c)}\n{' '.join(map(str, c))}\n" for c in cz) + "0\n"
        assert hasta_cero(_revolver(tz)) == [max(c) for c in cz]

        regs = [(" ".join(random.choice(["Ana", "de", "la", "Cruz"]) for _ in range(random.randint(1, 3))),
                 random.randint(0, 99)) for _ in range(random.randint(0, 4))]
        fin = random.choice(["\n", "\r\n"])
        tl = fin.join(f"{n};{p}" + fin * random.randint(0, 1) for n, p in regs)
        assert por_lineas(tl.encode()) == regs


if __name__ == "__main__":
    demo()
    pruebas()
    print("OK")
