"""Verificador de L - Don't Ask Why 2D (lo usa probar.py).

El enunciado acepta CUALQUIER secuencia y plegado que logren el máximo de
contactos, así que no se puede comparar el texto con el .out. Para cada pedido
se comprueba que:
  1. el número de contactos impreso es el máximo (el del .out esperado);
  2. la secuencia tiene largo N, solo letras H/P y exactamente B letras H;
  3. el plegado tiene N-1 direcciones de {R, L, U, D} y es autoevitante;
  4. los contactos recontados sobre el plegado coinciden con el número impreso.

Uso: python verificar.py <entrada> <salida_esperada> <salida_obtenida>
Sale con código 0 si es válida; si no, explica el error y sale con 1.
"""
import sys

PASO = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}


def contactos(secuencia, plegado):
    """Cuenta pares H-H vecinos en la cuadrícula que no son consecutivos en la cadena.
    Devuelve None si el camino se cruza consigo mismo."""
    x = y = 0
    pos = {(0, 0): 0}
    for i, d in enumerate(plegado, 1):
        dx, dy = PASO[d]
        x, y = x + dx, y + dy
        if (x, y) in pos:
            return None
        pos[(x, y)] = i
    total = 0
    for (x, y), i in pos.items():
        if secuencia[i] != "H":
            continue
        for dx, dy in ((1, 0), (0, 1)):          # cada par se cuenta una sola vez
            j = pos.get((x + dx, y + dy))
            if j is not None and abs(i - j) > 1 and secuencia[j] == "H":
                total += 1
    return total


def main():
    entrada, esperada, obtenida = (open(f, encoding="utf-8").read().split("\n") for f in sys.argv[1:4])
    pedidos = []
    for linea in entrada:
        n, b = map(int, linea.split())
        if n == 0 and b == 0:
            break
        pedidos.append((n, b))
    esperada = [l.split() for l in esperada if l.strip()]
    obtenida = [l.split() for l in obtenida if l.strip()]
    if len(obtenida) != len(pedidos):
        sys.exit(f"se esperaban {len(pedidos)} líneas y hay {len(obtenida)}")
    for k, ((n, b), esp, obt) in enumerate(zip(pedidos, esperada, obtenida), 1):
        maximo = int(esp[0])
        if len(obt) != (2 if n == 1 else 3):
            sys.exit(f"línea {k}: número de tokens incorrecto: {' '.join(obt)}")
        if int(obt[0]) != maximo:
            sys.exit(f"línea {k}: contactos {obt[0]}, el máximo es {maximo}")
        seq = obt[1]
        if len(seq) != n or set(seq) - {"H", "P"} or seq.count("H") != b:
            sys.exit(f"línea {k}: secuencia inválida {seq} para N={n}, B={b}")
        if n == 1:
            continue
        pleg = obt[2]
        if len(pleg) != n - 1 or set(pleg) - set(PASO):
            sys.exit(f"línea {k}: plegado inválido {pleg}")
        c = contactos(seq, pleg)
        if c is None:
            sys.exit(f"línea {k}: el plegado {pleg} se cruza consigo mismo")
        if c != maximo:
            sys.exit(f"línea {k}: el plegado logra {c} contactos, no {maximo}")


if __name__ == "__main__":
    main()
