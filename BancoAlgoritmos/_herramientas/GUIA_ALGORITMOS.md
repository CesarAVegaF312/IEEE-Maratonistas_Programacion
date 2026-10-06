# Guía para escribir el banco de algoritmos (léela completa antes de empezar)

El banco vive en `BancoAlgoritmos/<NN_Tema>/<archivo>.py`: **un archivo por
algoritmo**. Es material de estudio para un semillero de maratón de
programación (estudiantes universitarios, principiantes a intermedios). El
objetivo es **aprender**: cada archivo explica qué problema resuelve el
algoritmo, cómo reconocerlo en un enunciado, por qué funciona y cómo se
implementa, y trae la implementación lista para copiar en una competencia.

El modelo a imitar es `00_Base/busqueda_binaria.py`. Léelo antes de escribir.

## 1. Plantilla obligatoria (docstring al inicio del archivo, en español)

```python
"""
<Tema> — <Nombre del algoritmo> («<nombre en inglés si es el usual>»)
Nivel: Básico | Intermedio | Avanzado
Ejecutar: python <archivo>.py   (muestra el ejemplo y corre las pruebas)
Autor: César A. Vega F. <cesar.a.vega.f@gmail.com>

PARA QUÉ SIRVE
    Qué problema resuelve, en 2–4 líneas.
    Cómo reconocerlo en un enunciado: señales concretas (palabras clave,
    tamaño de N, forma de la pregunta).

FUNCIÓN
    firma(...) -> ...
    Qué recibe, qué devuelve, convenciones (índices desde 0, -1 si no hay…).

IDEA Y ALGORITMO
    La observación clave y POR QUÉ es correcta (argumento breve, no solo
    "se hace así"). Si hay fórmula, de dónde sale. Si existe un enfoque
    ingenuo, por qué no alcanza.

MACROALGORITMO
    1. Paso de alto nivel.
    2. …
    (4–10 pasos que se puedan seguir sin leer el código.)

COMPLEJIDAD
    Tiempo O(…), memoria O(…). Tamaño práctico en Python en ~1 s.

EJEMPLO A MANO
    Traza corta con un caso pequeño.

ERRORES TÍPICOS
    - 2–5 errores frecuentes al implementarlo en competencia.

VARIANTES Y RELACIONADOS
    - Variantes comunes y algoritmos del banco relacionados (por nombre de archivo).

DÓNDE PRACTICAR
    - Problemas del repo que lo usan, con ruta: ICPC/Colombia 2024/D - Drug Test
    - Externos: SOLO si estás seguro del nombre/ID (CSES por nombre, UVa o
      Codeforces por número). Nunca inventes un ID; si dudas, omítelo.

VERIFICACIÓN
    - Pruebas: OK contra fuerza bruta en N casos aleatorios (python <archivo>.py)
"""
```

## 2. El código

- Python 3.12, **solo biblioteca estándar**.
- La implementación va en funciones reutilizables con nombres claros en
  español o el nombre estándar (`dijkstra`, `kmp_prefijo`, `criba`…), con
  comentarios en español en cada bloque relevante (qué representa cada
  estructura, qué invariante se mantiene, por qué ese caso borde). Ni un
  comentario por línea trivial, ni bloques sin explicar.
- Debe ser el código que el estudiante copiaría en una maratón: corto,
  iterativo cuando la recursión pueda pasar de ~1000 niveles (pila
  explícita), sin dependencias entre archivos del banco (cada archivo es
  autocontenido; si necesita otro algoritmo, lo copia).
- Al final del archivo:
  ```python
  def demo():         # imprime el EJEMPLO A MANO resuelto por el código
  def pruebas():      # fuerza bruta + casos aleatorios + casos borde; usa assert
  if __name__ == "__main__":
      demo()
      pruebas()
      print("OK")
  ```
- `pruebas()` usa `random.seed(...)` fija, cientos de casos pequeños contra
  una fuerza bruta independiente (escrita de la forma más obvia posible) y
  casos borde (vacío, un elemento, todos iguales, valores máximos…). Debe
  tardar menos de ~5 s. Si de verdad no hay fuerza bruta posible, comparar
  contra propiedades verificables o resultados conocidos y decirlo en
  VERIFICACIÓN.
- Si el archivo cubre una técnica más que un algoritmo (p. ej. «argumento
  de intercambio», «comparar flotantes con epsilon»), igual lleva función
  de ejemplo sobre un problema clásico, demo y pruebas.

## 3. Prohibido

- No tocar nada fuera de los archivos que te asignaron (otros agentes
  escriben en las mismas carpetas al mismo tiempo). No modificar
  `_herramientas/`, `README.md` ni la carpeta `ICPC/` (solo leerla para
  citar problemas en DÓNDE PRACTICAR; el índice de técnicas por problema
  está en `ICPC/README.md`).
- No entregar un archivo cuyas pruebas no pasen. Si algo no funciona,
  repórtalo con el estado real.

## 4. Verificación (obligatoria)

1. `python <archivo>.py` termina con código 0 e imprime `OK`.
2. `python _herramientas/probar.py <NN_Tema>` desde `BancoAlgoritmos/`
   muestra tus archivos en `OK`.

En Bash usa `export PYTHONIOENCODING=utf-8`. Escribe archivos con la
herramienta Write (los heredocs de Bash pueden alterar las barras invertidas).

## 5. Reporte final

Tabla con: archivo, nombre del algoritmo, nivel, cuántos casos de prueba
corre, estado, y dudas. Nada más.
