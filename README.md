# Maratonistas de Programación — Semillero

Material de entrenamiento del semillero para la Maratón Nacional de
Programación (ICPC). Todo está en **Python 3** y en español.

| Carpeta | Qué hay |
|---|---|
| [`BancoAlgoritmos/`](BancoAlgoritmos/README.md) | 149 algoritmos, uno por archivo, organizados por tema (base, búsqueda completa, voraz, programación dinámica, cadenas, grafos, estructuras de datos, matemáticas, geometría). Cada uno explica para qué sirve, cómo reconocerlo en un enunciado, la idea, la complejidad, errores típicos y dónde practicarlo. |
| [`ICPC/`](ICPC/README.md) | 89 problemas de maratones reales (Colombia 2017, 2018, 2023–2026, Guangzhou 2017, OMP Murcia 2017): enunciado en inglés y en español, ejemplos de entrada/salida y solución comentada. |

## Cómo descargarlo

Con git (recomendado, así puedes traer las actualizaciones con `git pull`):

```
git clone https://github.com/CesarAVegaF312/IEEE-Maratonistas_Programacion.git
cd IEEE-Maratonistas_Programacion
```

Sin git: botón verde **Code → Download ZIP** en GitHub.

Necesitas **Python 3.10 o más nuevo** (`python --version`). No hay que
instalar librerías.

## Cómo usarlo

**Estudiar un algoritmo.** Abre el archivo y lee el comentario de arriba;
luego córrelo para ver el ejemplo y las pruebas:

```
cd BancoAlgoritmos
python 00_Base/sumas_prefijas.py
```

**Practicar un problema.** Lee el enunciado `(ES).pdf` o `(EN).pdf` de la
carpeta del problema, escribe **tu propia** solución y pruébala con el ejemplo:

```
cd "ICPC/Colombia 2025/A - Account Qualifying"
python mi_solucion.py < accountq.in
```

Compara tu salida con `accountq.out`. Solo cuando lo hayas intentado en serio,
abre la solución (`accountq.py`): leer la solución antes de pelear el problema
enseña mucho menos.

**Probar todo de una vez:**

```
cd BancoAlgoritmos && python _herramientas/probar.py
cd ICPC && python probar.py "Colombia 2025"
```

## Por dónde empezar

1. Los algoritmos de nivel **Básico** de `BancoAlgoritmos/00_Base` (lectura
   rápida, sumas prefijas, búsqueda binaria, dos punteros, ordenamiento).
2. Problemas de `ICPC/` cuya técnica sea simulación, ordenamiento o voraz
   (la tabla del [índice de ICPC](ICPC/README.md) dice la técnica de cada uno).
3. Programación dinámica y grafos básicos (BFS, DFS, Dijkstra, union-find).
4. Cada algoritmo del banco trae una sección **DÓNDE PRACTICAR** con problemas
   de esta misma carpeta `ICPC/`.

## Autor

César A. Vega F. — <cesar.a.vega.f@gmail.com>
