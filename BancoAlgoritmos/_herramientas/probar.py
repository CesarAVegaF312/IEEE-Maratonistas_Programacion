"""Corre cada algoritmo del banco (demo + pruebas) y reporta el estado.

Uso (desde la carpeta BancoAlgoritmos/):
  python _herramientas/probar.py                  -> todo el banco
  python _herramientas/probar.py 05_Grafos        -> solo rutas que contengan ese texto
  python _herramientas/probar.py dijkstra kmp     -> varios filtros
  python _herramientas/probar.py -v ...           -> muestra el error cuando falla

Estados:
  OK       el archivo terminó con código 0 e imprimió "OK" al final
  FALLA    terminó sin imprimir "OK" (alguna prueba no se cumplió)
  ERROR    terminó con error (assert fallido, excepción…)
  TIEMPO   pasó del límite (60 s)
"""
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LIMITE = 60


def archivos(filtros):
    for f in sorted(RAIZ.glob("[0-9][0-9]_*/*.py")):
        ruta = f.relative_to(RAIZ).as_posix()
        if not filtros or any(x.lower() in ruta.lower() for x in filtros):
            yield f, ruta


def probar(f):
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, f.name], cwd=f.parent, capture_output=True,
                           timeout=LIMITE, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
    except subprocess.TimeoutExpired:
        return "TIEMPO", LIMITE, ""
    t = time.time() - t0
    salida = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0:
        return "ERROR", t, r.stderr.decode("utf-8", "replace")[-1500:]
    if salida.strip().splitlines()[-1:] != ["OK"]:
        return "FALLA", t, salida[-1500:]
    return "OK", t, ""


def main():
    args = sys.argv[1:]
    verbose = "-v" in args
    filtros = [a for a in args if a != "-v"]
    conteo = {}
    for f, ruta in archivos(filtros):
        estado, t, detalle = probar(f)
        conteo[estado] = conteo.get(estado, 0) + 1
        print(f"{estado:7} {t:6.2f}s  {ruta}")
        if verbose and detalle:
            print("    " + detalle.replace("\n", "\n    "))
    print("\nResumen:", ", ".join(f"{k}: {v}" for k, v in sorted(conteo.items())) or "sin archivos")
    sys.exit(0 if set(conteo) <= {"OK"} else 1)


if __name__ == "__main__":
    main()
