"""Corre cada solución contra sus ejemplos (.in/.out) y compara la salida.

Uso (desde la carpeta ICPC/):
  python probar.py                      -> todos los problemas
  python probar.py "Colombia 2025"      -> solo carpetas cuyo nombre contenga ese texto
  python probar.py "2025/A" "2018/F"    -> varios filtros
  python probar.py -v ...               -> muestra la diferencia cuando falla

Estados:
  OK        salida idéntica (ignorando espacios al final de línea y líneas vacías finales)
  OK~       idéntica salvo números reales con diferencia <= 1e-6
  OK (ver)  aceptada por el verificador del problema (problemas con varias respuestas válidas:
            si la carpeta tiene verificar.py, se usa en lugar de comparar texto)
  FALLA     salida distinta
  TIEMPO    pasó del límite (30 s)
  ERROR     el programa terminó con error
  SIN .py   todavía no hay solución
"""
import json
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LIMITE = 30


def normalizar(s):
    lineas = [l.rstrip() for l in s.replace("\r\n", "\n").split("\n")]
    while lineas and not lineas[-1]:
        lineas.pop()
    return lineas


def casi_igual(a, b):
    ta, tb = " ".join(a).split(), " ".join(b).split()
    if len(ta) != len(tb):
        return False
    for x, y in zip(ta, tb):
        if x == y:
            continue
        try:
            fx, fy = float(x), float(y)
        except ValueError:
            return False
        if abs(fx - fy) > 1e-6 * max(1.0, abs(fy)):
            return False
    return True


def probar(p, verbose):
    d = AQUI / p["dir"]
    sol = d / f"{p['codigo']}.py"
    if not sol.exists():
        return "SIN .py", 0.0
    peor, total = "OK", 0.0
    for ent in sorted(d.glob("*.in")):
        esperado = ent.with_suffix(".out").read_text(encoding="utf-8")
        t0 = time.time()
        try:
            r = subprocess.run([sys.executable, sol.name], cwd=d, input=ent.read_bytes(),
                               capture_output=True, timeout=LIMITE)
        except subprocess.TimeoutExpired:
            return "TIEMPO", LIMITE
        total += time.time() - t0
        if r.returncode != 0:
            if verbose:
                print(r.stderr.decode("utf-8", "replace")[-800:])
            return "ERROR", total
        obtenido = r.stdout.decode("utf-8", "replace")
        verificador = d / "verificar.py"
        if verificador.exists():
            # Varias respuestas válidas: el verificador decide (código de salida 0 = aceptada).
            tmp = d / "_obtenido.tmp"
            tmp.write_text(obtenido, encoding="utf-8")
            v = subprocess.run([sys.executable, verificador.name, ent.name, ent.with_suffix(".out").name, tmp.name],
                               cwd=d, capture_output=True)
            tmp.unlink()
            if v.returncode != 0:
                if verbose:
                    print(v.stdout.decode("utf-8", "replace") + v.stderr.decode("utf-8", "replace"))
                return "FALLA", total
            peor = "OK (ver)"
            continue
        a, b = normalizar(obtenido), normalizar(esperado)
        if a == b:
            continue
        if casi_igual(a, b):
            peor = "OK~"
            continue
        if verbose:
            print(f"--- {ent.name}: esperado ---\n" + "\n".join(b[:30]))
            print("--- obtenido ---\n" + "\n".join(a[:30]))
        return "FALLA", total
    return peor, total


def main():
    args = sys.argv[1:]
    verbose = "-v" in args
    filtros = [a for a in args if a != "-v"]
    probs = json.loads((AQUI / "_herramientas" / "problemas.json").read_text(encoding="utf-8"))
    if filtros:
        probs = [p for p in probs if any(f.lower() in p["dir"].lower() for f in filtros)]
    cuenta = {}
    for p in probs:
        estado, t = probar(p, verbose)
        cuenta[estado] = cuenta.get(estado, 0) + 1
        print(f"{estado:8} {t:6.2f}s  {p['dir']}")
    print("\nResumen:", ", ".join(f"{k}: {v}" for k, v in sorted(cuenta.items())), f"(total {len(probs)})")


if __name__ == "__main__":
    main()
