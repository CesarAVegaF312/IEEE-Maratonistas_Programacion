"""Copia al warmup de 2026 las soluciones de los problemas que reutiliza.

El warmup de la XL Maratón (2026) repite, con el mismo enunciado y ejemplo,
cuatro problemas de maratones anteriores. Este script copia esas soluciones
cambiando solo la cabecera del docstring. Si se corrige la solución original,
vuelve a correrlo.
"""
from pathlib import Path

EJ = Path(__file__).resolve().parents[1]

# letra del warmup -> (carpeta de origen, letra de origen)
ORIGEN = {
    "A": ("Colombia 2025/A - Account Qualifying", "Colombia 2025", "A"),
    "B": ("Colombia 2025/B - Binary Dozens", "Colombia 2025", "B"),
    "C": ("Colombia 2018/F - A Fibonacci Family Formula", "Colombia 2018", "F"),
    "D": ("Colombia 2025/J - Just Palindromes!", "Colombia 2025", "J"),
}

for letra, (carpeta, set_origen, letra_origen) in ORIGEN.items():
    src = next((EJ / carpeta).glob("*.py"))
    destino_dir = next((EJ / "Colombia 2026 Warmup").glob(f"{letra} - *"))
    s = src.read_text(encoding="utf-8")
    viejo = f"{set_origen} — {letra_origen}:"
    assert viejo in s, f"no encontré la cabecera en {src}"
    s = s.replace(viejo, f"Colombia 2026 Warmup — {letra}:", 1)
    s = s.replace(f'probar.py "{set_origen}/{letra_origen}"', f'probar.py "Warmup/{letra}"')
    nota = (f"\nNOTA: problema idéntico (enunciado y ejemplo) a {set_origen} {letra_origen}; "
            f"esta solución es copia de\n    {carpeta}/{src.name} (generada con _herramientas/copiar_warmup.py).\n")
    # la nota va después de la cabecera (línea "Ejecutar:" y, si existe, la de autor)
    ancla = "Autor de la solución:" if "Autor de la solución:" in s else "Ejecutar:"
    fin_cabecera = s.index("\n", s.index(ancla))
    s = s[:fin_cabecera + 1] + nota + s[fin_cabecera + 1:]
    (destino_dir / src.name).write_text(s, encoding="utf-8")
    print(f"{carpeta}/{src.name} -> {destino_dir.relative_to(EJ)}/{src.name}")
