# ICPC — índice de problemas

Una carpeta por problema (`<Set>/<Letra> - <Título>/`) con:

| Archivo | Qué es |
|---|---|
| `<codigo>.py` | Solución en Python 3 comentada: CONTEXTO, QUÉ HAY QUE HACER, IDEA Y ALGORITMO, MACROALGORITMO, COMPLEJIDAD, VERIFICACIÓN |
| `<codigo>.in` / `<codigo>.out` | Ejemplo de entrada y salida del enunciado |
| `<codigo> (EN).pdf` | Enunciado original en inglés (solo las páginas de ese problema) |
| `<codigo> (ES).pdf` | Enunciado traducido al español |
| `verificar.py` | Solo en problemas con varias respuestas válidas (Colombia 2026 L) |

`<codigo>` es el nombre de archivo que exige el enunciado (en Guangzhou y OMP, que no lo traen, es un nombre descriptivo).

## Cómo probar

```
cd ICPC
python probar.py                    # todo
python probar.py "Colombia 2025"    # un set
python probar.py "2026/L" -v        # un problema, mostrando diferencias
cd "Colombia 2025/A - Account Qualifying" && python accountq.py < accountq.in
```

Estado actual: **86 OK, 1 OK con verificador, 2 FALLA documentadas** (ver «Puntos abiertos»).
Todas las soluciones se compararon además contra una fuerza bruta en casos aleatorios pequeños
(salvo Colombia 2018 A, que es simulación directa).

Herramientas en `_herramientas/`:
`copiar_warmup.py` (el warmup 2026 reutiliza 4 problemas: copia sus soluciones),
`GUIA_SOLUCIONES.md` (plantilla que siguen las soluciones), `problemas.json` (índice).

## Colombia 2017 — XXXI Maratón Nacional

| | Problema | Técnica |
|---|---|---|
| A | A Contest to Meet (`acm`) | Floyd–Warshall + diámetro / velocidad mínima |
| B | Balance Game (`balance`) | Ecuación diofántica lineal (Euclides extendido) |
| C | Compact Terms (`compact`) | Numeración canónica de subtérminos con pila |
| D | Rotating Drum (`drum`) | Secuencia de De Bruijn (palabras de Lyndon, FKM) |
| E | Rational Coins (`coins`) | Círculos de Ford, inverso modular |
| F | Fish (`fish`) | Envolventes convexas + teorema del eje separador |
| G | FujikoMine (`fujiko`) | DP en árbol tipo mochila |
| H | Hip-n (`hipn`) | Simulación con tablero aplanado |
| I | License Plates (`plates`) | Voraz + búsqueda binaria |
| J | Romeo and Juliet Secrets (`romeo`) | Función Z sobre prefijos y sufijos |
| K | Soccer Championship (`soccer`) | Simulación + ordenamiento por clave compuesta |

## Colombia 2018 — XXXII Maratón Nacional

| | Problema | Técnica |
|---|---|---|
| A | All-star Three-point Contest (`all`) | Simulación + ordenamiento |
| B | Forming Better Groups (`better`) | DP sobre máscaras de bits |
| C | Carrol's Scrabble (`carrol`) | BFS por capas sobre cubetas + union-find |
| D | Dominoes Magic Squares (`dominoes`) | Backtracking con poda por líneas |
| E | Extended Puzzle (`extended`) | Invariante de paridad de permutaciones |
| F | A Fibonacci Family Formula (`family`) | Recurrencia lineal + Kitamasa |
| G | Tron Garbage Collector (`garbage`) | DP de perfil (Slitherlink) con etiquetas de componentes |
| H | Ghost Hunting (`hunting`) | Envolvente convexa + dos punteros (triángulo de área máxima) |
| I | Impossible Communication (`impossible`) | Fuerte conexidad con dos BFS + nodos virtuales |
| J | Jawbreaking Candy (`jawbreaking`) | Sucesión de Farey / árbol de Stern–Brocot |
| K | kewl Texting (`kewl`) | Bigramas + grafo funcional con detección de ciclos |

## Colombia 2023 — XXXVII Maratón Nacional

| | Problema | Técnica |
|---|---|---|
| A | ASP (`asp`) | Circuito euleriano (fórmula N(N−1)+1) |
| B | Be Strong (`be`) | Prefijo común más largo |
| C | Knights (`knights`) | BFS + paridad (grafo bipartito) — **FALLA esperada, ver abajo** |
| D | Robot Arm (`arm`) | Geometría: alcance del brazo como anillo |
| E | LISP Extravaganza (`extravaganza`) | Emparejamiento voraz de paréntesis |
| F | Finding Common Passwords (`find`) | Búsqueda binaria + hashing polinomial |
| G | Grain Silos (`grain`) | A* sobre configuraciones — exponencial, ver abajo |
| H | Match Points (`matchp`) | Asignación húngara |
| I | Stack Solitaire (`stack`) | DP de intervalos con optimización de Knuth |
| J | TNumbers (`tnumbers`) | Ecuación de Pell negativa |

## Colombia 2024 — XXXVIII Maratón Nacional

| | Problema | Técnica |
|---|---|---|
| A | Arctic Virus (`arctic`) | DP por intervalos sobre una gramática |
| B | The Bridge at Night (`bridge`) | Voraz clásico «bridge and torch» |
| C | SquareDiff (`sqdf`) | Teoría de números (N ≢ 2 mód 4) |
| D | Drug Test (`drugtest`) | 2-coloración de un grafo |
| E | Spacebar Tokenizer (`spacebar`) | DP sobre prefijos + trie |
| F | Turnswitch (`turnswitch`) | Lights Out: enumerar primera fila y propagar |
| G | Signal Coverage (`signal`) | 2-SAT (Tarjan) con generación perezosa de restricciones |
| H | Only1s0s (`only1s0s`) | BFS sobre restos módulo N |
| I | Omens (`omens`) | Probabilidad geométrica (fórmula cerrada) |
| J | Lumina (`lumina`) | Componentes conexas (BFS) |
| K | Skyline (`skyline`) | Conteo de inversiones con Fenwick |

## Colombia 2025 — XXXIX Maratón Nacional

| | Problema | Técnica |
|---|---|---|
| A | Account Qualifying (`accountq`) | Sumas prefijas + primera aparición |
| B | Binary Dozens (`bindozens`) | Horner modular |
| C | Celestial Veins (`celestial`) | K vecinos más cercanos + BFS |
| D | Discrete Catalog (`discrete`) | Rango de una combinación |
| E | Efficient Encoding (`encoding`) | Huffman + concavidad por tramos |
| F | Fingerprints (`fingerprints`) | Rotación mínima (Booth) |
| G | Guard Deployment (`guard`) | Envolvente convexa + búsqueda binaria angular |
| H | Holy Network (`holy`) | Clique máxima (branch & bound, Tomita) |
| I | Impossible Primebox (`impossible`) | Teorema chino del resto + macro-pasos |
| J | Just Palindromes! (`just`) | Filtrado + comparación con el reverso |

## Colombia 2026 — XL Maratón Nacional

| | Problema | Técnica |
|---|---|---|
| A | Balanced System Reactor (`balsys`) | Factorización + enumeración acotada de divisores |
| B | Bankey (`bankey`) | Ventana deslizante con sumas prefijas |
| C | Into the Onion (`onion`) | Capas convexas + DP por capas |
| D | Bingwhenever (`bingwhenever`) | Diccionario valor → turno |
| E | Custom Keypad (`customkeypad`) | DP de partición + reconstrucción voraz |
| F | Heist (`heist`) | Celdas convexas + centro de Chebyshev |
| G | Math United FC (`mathunited`) | Voraz con montículo |
| H | HCubes Costs (`hcubes`) | XOR + suma de pesos por bit |
| I | Fair Workload Distribution (`fairworkload`) | Consultas offline con Fenwick |
| J | Courage is Contagious (`courage`) | Punto fijo de función monótona |
| K | Sample Median Preservation (`samplemedian`) | Combinatoria por complemento |
| L | Don't Ask Why 2D (`dont`) | Búsqueda exhaustiva con simetría — **varias respuestas válidas** (`verificar.py`) |
| M | Byte Flu (`flu`) | Distancia de edición bit-paralela (Myers) + corte mínimo (Dinic) |

**Warmup 2026**: A = 2025 A, B = 2025 B, C = 2018 F, D = 2025 J (mismo enunciado y ejemplo; soluciones copiadas).

## Guangzhou 2017 — ACM ICPC Summer Series (agosto)

| | Problema | Técnica |
|---|---|---|
| A | Alice's Travels II (`alicetravels`) | Mochila ilimitada + máximos en caminos de árbol (LCA) |
| B | Between Ceiling and Floor (`ceilingfloor`) | Suma de divisores σ(m) + Pollard-Rho |
| C | Count Equation Solutions (`countequation`) | Encuentro en el medio |
| D | Determinant Fun (`determinantfun`) | Matriz de rango ≤ 2 (lema de Sylvester) + sumas geométricas |
| E | Easy Tiling Problem (`easytiling`) | Matriz de transferencia + Berlekamp–Massey + Kitamasa |
| F | Finding Paths (`findingpaths`) | Inclusión–exclusión + multinomiales |
| G | Great Coin Game (`greatcoingame`) | Correlaciones de Conway + Gauss |
| H | Half the Polygon (`halfpolygon`) | Cortes antípodas + congruencia de secuencias cíclicas |
| I | Interesting Resister Graph (`resistergraph`) | Función de Green del Laplaciano — **FALLA documentada, ver abajo** |
| J | Journey through Gridland (`gridland`) | Función generatriz |
| K | Kid's Spiral Problem (`kidspiral`) | Fórmula cerrada por regiones + diferencias de Newton |

## OMP 2017 — Universidad de Murcia

| | Problema | Técnica |
|---|---|---|
| A | Blade Ranas 2040 (`bladeranas`) | Conteo por tramos entre muros |
| B | Pool Filling (`poolfilling`) | Sumas prefijas + búsqueda binaria |
| C | The Broken DNA of Jack the Ripper (`brokendna`) | Bitsets (enteros grandes) |
| D | Space Happiness (`spacehappiness`) | Fórmula cerrada |
| E | Prime Darts (`primedarts`) | Cambio de monedas (DP) |
| F | Chained Words (`chainedwords`) | Circuito euleriano (Hierholzer) |
| G | Recomputing Dependencies (`recomputingdeps`) | Reindexación con arreglo de posiciones |
| H | Rogue One: Time to Impact (`rogueone`) | Modelo de cámara estenopeica |

## Puntos abiertos

**Ejemplos del enunciado que no se pueden reproducir** (la solución sigue el texto; el porqué está en el docstring):
- **Colombia 2023 C (Knights)**: la lectura literal reproduce el ejemplo trabajado del texto y 2 de los 3 ejemplos;
  el ejemplo `8 0 0 5 4 → 2` es inconsistente (casillas de distinto color). Ninguna lectura alternativa cuadra con los tres.
- **Guangzhou I (Resister Graph)**: las salidas esperadas son irracionales, imposible con resistencias de 1 Ω.

**Lecturas ambiguas del enunciado** (se eligió la literal; el ejemplo no distingue):
Colombia 2017 G (botín como un solo subárbol), 2018 E (marcos 1×n), 2018 G (ruta vacía), 2018 K (apariciones de {start}/{end}),
2024 J (activación simétrica vs. dirigida), 2025 G (qué edificios cuentan para la altura), Guangzhou J (costo = producto de pasos, no suma, para que cuadre el ejemplo).

**Desempates no definidos** (cualquier respuesta óptima debería ser aceptada): Colombia 2026 A y F, OMP B.

**Pueden ser lentos en Python con la entrada máxima** (correctos, pero podrían pasar el límite del juez):
Colombia 2023 G (exponencial con silos muy llenos), 2026 A (6–10 s), 2026 E (casos diminutos masivos),
2025 E e I (5–15 s), 2018 C (~9 s adversario), 2024 G (5–8 s adversario),
Guangzhou A, B, C, G, H, J (con muchos casos grandes).
