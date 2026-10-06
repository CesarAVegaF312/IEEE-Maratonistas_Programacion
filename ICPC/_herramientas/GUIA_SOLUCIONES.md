# Guía para escribir las soluciones (léela completa antes de empezar)

Cada problema vive en `ICPC/<Set>/<Letra> - <Título>/` y ya contiene:
`<codigo>.in`, `<codigo>.out` (ejemplo del enunciado), `<codigo> (EN).pdf` y
`<codigo> (ES).pdf`. Tú agregas **`<codigo>.py`** (el `codigo` está en
`_herramientas/problemas.json` y es el nombre que ya tienen los .in/.out).

El usuario quiere **aprender** de estas soluciones: el código debe explicar
cómo se desarrolla el ejercicio, qué algoritmo usa, el contexto, un resumen de
lo que hay que hacer y el macroalgoritmo.

## 1. Plantilla obligatoria (docstring al inicio del archivo, en español)

```python
"""
<Nombre del set> — <Letra>: <Título original> («<título en español>»)
Ejecutar: python <codigo>.py < <codigo>.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La historia del enunciado en 2–4 líneas (quién, qué situación).

QUÉ HAY QUE HACER
    Entrada: formato resumido (cómo termina la entrada, casos múltiples…).
    Salida:  qué se imprime y con qué formato exacto.
    Restricciones clave: N ≤ …, valores ≤ … (las que deciden el algoritmo).

IDEA Y ALGORITMO
    Técnica(s) usadas, nombradas con su nombre estándar (p. ej. "búsqueda
    binaria sobre la respuesta", "DP de mochila", "Dijkstra", "barrido con
    pila monótona", "exponenciación de matrices").
    La observación clave y POR QUÉ es correcta (argumento breve, no solo "se
    hace así"). Si hay una fórmula, explicar de dónde sale.
    Si el enfoque ingenuo no alcanza, decir por qué (complejidad) y qué lo
    reemplaza.

MACROALGORITMO
    1. Paso de alto nivel.
    2. Paso de alto nivel.
    3. …
    (5–10 pasos que se puedan seguir sin leer el código.)

COMPLEJIDAD
    Tiempo O(…), memoria O(…). Si en el peor caso Python puede ser lento
    para el límite del juez, dilo explícitamente.

EJEMPLO A MANO (opcional pero recomendado si ayuda)
    Traza corta del ejemplo del enunciado con el algoritmo.

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python ../../probar.py "<Set>/<Letra>")
    - Fuerza bruta: OK en N casos aleatorios pequeños / no aplica (por qué)
"""
```

## 2. El código

- Python 3, solo biblioteca estándar. Lee de stdin y escribe a stdout.
  Lectura rápida: `sys.stdin.buffer.read().split()` cuando el formato lo
  permite; `sys.stdin.readline` cuando importan las líneas/espacios.
- Comentarios en español **dentro del código** en cada bloque relevante
  (qué representa cada estructura, qué invariante se mantiene, por qué ese
  caso borde). Ni un comentario por línea trivial, ni bloques sin explicar.
- Nombres de variables claros; funciones pequeñas (`leer_casos`, `resolver`,
  …) y un `main()` con `if __name__ == "__main__": main()`.
- Recursión profunda: evitarla (pila explícita) o `sys.setrecursionlimit` +
  `threading` con stack grande si es inevitable.
- Formato de salida EXACTO (decimales, espacios, mayúsculas, líneas tipo
  `Case 1:`).

## 3. Prohibido

- **Nunca** imprimir respuestas fijas ni detectar el caso de ejemplo. La
  solución debe resolver el problema general.
- No modificar los `.in`, `.out`, PDFs, `probar.py`, `problemas.json` ni
  nada fuera de tus carpetas asignadas. No tocar archivos de la carpeta raíz
  `40icpc/` (allí hay soluciones del usuario: solo léelas si te las indican).

## 4. Verificación (obligatoria)

1. Desde `ICPC/`: `python probar.py "<Set>/<Letra>"` debe dar `OK`
   (u `OK~` si hay reales). Usa `-v` para ver diferencias.
2. Para todo problema no trivial escribe una **fuerza bruta** (en tu
   carpeta temporal, NO en la carpeta del problema) y compárala con tu
   solución en cientos de casos aleatorios pequeños. Si no es posible
   (p. ej. no hay fuerza bruta razonable), explica por qué en VERIFICACIÓN.
3. Prueba de rendimiento: genera un caso grande cerca de los límites y mide
   el tiempo. Anota el resultado en COMPLEJIDAD si es lento.
4. Si no logras una solución correcta, NO entregues algo que "pase el
   ejemplo" por casualidad sin decirlo: deja en VERIFICACIÓN el estado real
   ("solución parcial: … / no verificada contra fuerza bruta / falla en …")
   y repórtalo.
5. Si encuentras que el enunciado o el ejemplo es inconsistente, explícalo en
   el docstring (sección IDEA o VERIFICACIÓN) y en tu reporte.

En Bash usa `export PYTHONIOENCODING=utf-8`. Escribe archivos con la
herramienta Write (los heredocs de Bash pueden alterar las barras invertidas).

## 5. Reporte final

Tabla con: problema, técnica principal, estado (`OK ejemplo + fuerza bruta`,
`OK ejemplo`, `parcial`, `sin resolver`), tiempo en el caso grande y cualquier
duda o inconsistencia del enunciado.
