"""Genera BancoAlgoritmos/README.md a partir del docstring de cada algoritmo.

Uso (desde la carpeta BancoAlgoritmos/):
  python _herramientas/indice.py

De cada archivo toma la primera línea («<Tema> — <Nombre>»), la línea
«Nivel: …» y la primera oración de PARA QUÉ SIRVE. Si un archivo no sigue
la plantilla, lo avisa por consola y lo lista igual.
"""
import ast
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ORDEN_NIVEL = {"Básico": 0, "Intermedio": 1, "Avanzado": 2}

ENCABEZADO = """# Banco de algoritmos — Semillero de Maratón de Programación

Un archivo `.py` por algoritmo, organizado por tema. Cada archivo trae, en su
docstring: PARA QUÉ SIRVE (y cómo reconocerlo en un enunciado), FUNCIÓN, IDEA Y
ALGORITMO (por qué funciona), MACROALGORITMO, COMPLEJIDAD, EJEMPLO A MANO,
ERRORES TÍPICOS, VARIANTES, DÓNDE PRACTICAR y VERIFICACIÓN; y debajo, la
implementación lista para copiar, un `demo()` y `pruebas()` contra fuerza bruta.

## Cómo usarlo

```
cd BancoAlgoritmos
python 05_Grafos/dijkstra.py              # ver el ejemplo y correr sus pruebas
python _herramientas/probar.py            # probar todo el banco
python _herramientas/probar.py 04_Cadenas # probar un tema
python _herramientas/indice.py            # regenerar este README
```

Para escribir un algoritmo nuevo: `_herramientas/GUIA_ALGORITMOS.md` (plantilla)
y `00_Base/busqueda_binaria.py` (modelo).

Niveles: **Básico** (problemas fáciles y medios), **Intermedio** (lo que separa
equipos en el nacional), **Avanzado** (problemas difíciles).
"""


def leer(f):
    doc = ast.get_docstring(ast.parse(f.read_text(encoding="utf-8"))) or ""
    lineas = doc.splitlines()
    titulo = lineas[0].strip() if lineas else f.stem
    nombre = titulo.split("—", 1)[1].strip() if "—" in titulo else titulo
    m = re.search(r"^Nivel:\s*(.+)$", doc, re.M)
    nivel = m.group(1).strip() if m else "?"
    m = re.search(r"PARA QUÉ SIRVE\s*\n(.*?)(?:\n\s*\n|\n[A-ZÁÉÍÓÚ ]{5,}\n)", doc, re.S)
    resumen = " ".join(m.group(1).split()) if m else ""
    resumen = re.split(r"(?<=\.)\s", resumen, maxsplit=1)[0]
    if "?" in nivel or not resumen:
        print(f"aviso: {f.relative_to(RAIZ).as_posix()} no sigue la plantilla del todo")
    return nombre, nivel, resumen


def clave_nivel(nivel):
    return min((v for k, v in ORDEN_NIVEL.items() if k in nivel), default=3)


def main():
    partes = [ENCABEZADO]
    total = 0
    for carpeta in sorted(p for p in RAIZ.iterdir() if p.is_dir() and re.match(r"\d\d_", p.name)):
        filas = []
        for f in sorted(carpeta.glob("*.py")):
            nombre, nivel, resumen = leer(f)
            filas.append((clave_nivel(nivel), nombre.lower(), f.name, nombre, nivel, resumen))
        if not filas:
            continue
        total += len(filas)
        tema = carpeta.name[3:].replace("_", " ")
        partes.append(f"\n## {carpeta.name[:2]} · {tema} ({len(filas)})\n")
        partes.append("| Algoritmo | Nivel | Para qué sirve |\n|---|---|---|")
        for *_, archivo, nombre, nivel, resumen in sorted(filas):
            ruta = f"{carpeta.name}/{archivo}"
            partes.append(f"| [{nombre}]({ruta}) | {nivel} | {resumen.replace('|', '/')} |")
    partes.insert(1, f"\n**{total} algoritmos.**\n")
    (RAIZ / "README.md").write_text("\n".join(partes) + "\n", encoding="utf-8")
    print(f"README.md generado con {total} algoritmos")


if __name__ == "__main__":
    main()
