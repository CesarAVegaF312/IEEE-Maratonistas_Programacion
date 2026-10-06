# Banco de algoritmos — Semillero de Maratón de Programación

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


**149 algoritmos.**


## 00 · Base (11)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Arreglo de diferencias 1D y 2D («Difference array»)](00_Base/arreglo_diferencias.py) | Básico | Aplicar muchas actualizaciones «sumar v a todas las posiciones de l a r» (o a un rectángulo de una matriz) y al FINAL conocer el arreglo resultante. |
| [Búsqueda binaria («Binary search»)](00_Base/busqueda_binaria.py) | Básico | Encontrar en O(log N) la primera posición donde una condición pasa de falso a verdadero: en un arreglo ordenado («¿cuántos valores son ≤ x?», «¿dónde insertar x?») o sobre un rango de números («búsqueda binaria sobre la respuesta»). |
| [Conteo con diccionarios («Hash maps: frequency, first occurrence, grouping»)](00_Base/conteo_diccionarios.py) | Básico | Contar cuántas veces aparece cada valor, recordar DÓNDE apareció por primera vez algo, o agrupar elementos por una clave, todo en O(1) por operación (en promedio). |
| [Dos punteros («Two pointers»)](00_Base/dos_punteros.py) | Básico | Recorrer un arreglo con dos índices que SOLO AVANZAN, para resolver en O(N) problemas que a lo ingenuo serían O(N²) (probar todos los pares o todos los subarreglos). |
| [Lectura rápida de la entrada («Fast I/O»)](00_Base/lectura_rapida.py) | Básico | Leer TODA la entrada de una vez y recorrerla por tokens. |
| [Ordenamiento con clave compuesta («Custom sort / sort by key»)](00_Base/ordenamiento_clave_compuesta.py) | Básico | Ordenar registros por varios criterios con desempates: «ordenar por puntos de mayor a menor; si empatan, por diferencia de goles; si siguen empatados, por nombre alfabéticamente». |
| [Pila, cola y deque en Python («Stack, queue, deque»)](00_Base/pila_cola_deque.py) | Básico | Pila (LIFO, el último que entra sale primero): paréntesis, deshacer, evaluar expresiones, vías de tren sin salida, «el anterior menor». |
| [Simulación paso a paso («Simulation / ad hoc»)](00_Base/simulacion.py) | Básico | Hacer exactamente lo que dice el enunciado, paso a paso, con estructuras de datos que hagan cada paso barato. |
| [Sumas prefijas 1D y 2D («Prefix sums»)](00_Base/sumas_prefijas.py) | Básico | Responder en O(1) «¿cuánto suman los elementos de la posición l a la r?» (o de un rectángulo de una matriz), después de un precálculo O(N). |
| [Ventana deslizante («Sliding window»; deque monótona)](00_Base/ventana_deslizante.py) | Básico/Intermedio | Calcular algo sobre TODOS los subarreglos contiguos de tamaño K (ventana fija) o encontrar el mejor subarreglo que cumple una condición (ventana variable), actualizando el resultado al entrar un elemento por la derecha y salir otro por la izquierda, en vez de recalcular cada ventana. |
| [Búsqueda ternaria («Ternary search»)](00_Base/busqueda_ternaria.py) | Intermedio | Encontrar el máximo (o mínimo) de una función UNIMODAL: sube hasta un pico y luego baja (o baja hasta un valle y luego sube), sin conocer una fórmula para el pico. |

## 01 · BusquedaCompleta (8)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Fuerza bruta con bucles anidados («Iterative complete search»)](01_BusquedaCompleta/fuerza_bruta_bucles.py) | Básico | Probar TODAS las posibilidades con bucles anidados y quedarse con las que cumplen. |
| [Permutaciones («Permutations / next_permutation»)](01_BusquedaCompleta/permutaciones.py) | Básico | Probar todos los ÓRDENES posibles de N elementos (N! en total) cuando el problema pide el mejor orden, o generar la permutación siguiente en orden lexicográfico (incluso con elementos repetidos). |
| [Subconjuntos con máscaras de bits («Bitmask subset enumeration»)](01_BusquedaCompleta/subconjuntos_mascaras.py) | Básico | Recorrer los 2^N subconjuntos de N elementos representando cada uno con un entero: el bit i encendido significa «el elemento i está». |
| [Backtracking con poda («Backtracking with pruning»)](01_BusquedaCompleta/backtracking_poda.py) | Intermedio | Construir una solución decisión por decisión (fila por fila, elemento por elemento) y RETROCEDER apenas una decisión parcial ya no puede terminar en una solución válida. |
| [Búsqueda binaria sobre la respuesta («Binary search the answer»)](01_BusquedaCompleta/busqueda_sobre_respuesta.py) | Intermedio | Convertir un problema de OPTIMIZACIÓN («el mínimo T tal que…») en muchas preguntas de DECISIÓN («¿se puede con T?»), cuando la decisión es fácil de responder y MONÓTONA: si se puede con T, también con T + 1. |
| [Encuentro en el medio («Meet in the middle»)](01_BusquedaCompleta/meet_in_the_middle.py) | Intermedio | Bajar una búsqueda de 2^N a ~2·2^(N/2): partir los elementos en dos mitades, enumerar TODO lo de cada mitad por separado y combinar las dos listas con un diccionario, ordenamiento + búsqueda binaria o dos punteros. |
| [A* e IDA* sobre espacios de estados («A* search, IDA*»)](01_BusquedaCompleta/a_estrella.py) | Avanzado | Encontrar el camino MÁS CORTO desde un estado inicial a un estado meta en un grafo de estados enorme (rompecabezas, configuraciones), usando una HEURÍSTICA h(estado) que estima lo que falta. |
| [Ramificación y poda: clique máxima («Branch and bound, Bron–Kerbosch»)](01_BusquedaCompleta/branch_and_bound.py) | Avanzado | Resolver EXACTAMENTE problemas de optimización NP-difíciles con N moderado (≈ 40–60) explorando un árbol de decisiones y cortando cada rama cuya COTA (lo mejor que podría lograr) no supera la mejor solución ya encontrada. |

## 02 · Voraz (8)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Cambio de monedas voraz («Greedy coin change» y sistemas canónicos)](02_Voraz/cambio_monedas_voraz.py) | Básico | Pagar una cantidad X con el MENOR número de monedas (monedas ilimitadas de cada denominación). |
| [Mochila fraccionaria («Fractional knapsack»)](02_Voraz/mochila_fraccionaria.py) | Básico | Llenar una mochila de capacidad W con objetos de valor v_i y peso w_i maximizando el valor, cuando se puede tomar una FRACCIÓN de cada objeto (polvo de oro, litros de combustible, kilos de especias). |
| [Selección de actividades («Activity selection / interval scheduling»)](02_Voraz/seleccion_actividades.py) | Básico | Dado un conjunto de intervalos [inicio, fin), elegir la MAYOR cantidad posible que no se solapen entre sí (una sola sala, un solo cine, una sola máquina). |
| [Argumento de intercambio y regla de Smith («Exchange argument», «Smith's rule»)](02_Voraz/argumento_intercambio.py) | Intermedio | Técnica para DESCUBRIR y DEMOSTRAR el orden óptimo cuando la respuesta es «poner los elementos en algún orden»: se mira qué pasa al intercambiar dos elementos VECINOS y de ahí sale el criterio de ordenamiento (un comparador). |
| [Cruzar el puente de noche («Bridge and torch problem»)](02_Voraz/bridge_and_torch.py) | Intermedio | N personas deben cruzar un puente de noche. |
| [Código de Huffman («Huffman coding»)](02_Voraz/huffman.py) | Intermedio | Dadas las frecuencias f_i de N símbolos, construir un código binario LIBRE DE PREFIJOS (ninguna palabra es prefijo de otra) que minimice la longitud total Σ f_i · /código_i/. |
| [Problemas clásicos de intervalos («Merge intervals, interval stabbing, interval covering»)](02_Voraz/intervalos.py) | Intermedio | Tres problemas de intervalos CERRADOS [a, b] que salen muchísimo y se resuelven ordenando y barriendo una vez: 1. |
| [Voraz con montículo y «arrepentimiento» («Greedy with a heap / regret greedy»)](02_Voraz/voraz_con_monticulo.py) | Intermedio | Elegir el mejor subconjunto de tareas con PLAZOS recorriéndolas en orden y, cuando el conjunto deja de ser válido, «arrepentirse» sacando la PEOR tarea elegida hasta ahora (la tiene a mano un montículo). |

## 03 · ProgramacionDinamica (20)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Cambio de monedas («Coin change»)](03_ProgramacionDinamica/cambio_monedas_dp.py) | Básico | Con monedas de ciertos valores (cada una se puede usar las veces que se quiera) se quiere formar exactamente la cantidad x: (1) con el MÍNIMO número de monedas; (2) contar de cuántas FORMAS, donde 2+1 y 1+2 son la misma (no importa el orden: se cuentan multiconjuntos); (3) contar de cuántas formas si 2+1 y 1+2 son distintas (importa el orden: se cuentan secuencias). |
| [Caminos en grilla («Grid paths»)](03_ProgramacionDinamica/caminos_grilla.py) | Básico | En una grilla n×m con obstáculos, moviéndose solo a la DERECHA o hacia ABAJO desde la esquina superior izquierda hasta la inferior derecha: (1) contar cuántos caminos hay (normalmente módulo 10^9+7); (2) encontrar el camino de suma mínima (cada celda tiene un costo) y mostrarlo. |
| [Distancia de edición («Levenshtein distance / edit distance»)](03_ProgramacionDinamica/distancia_edicion.py) | Básico | Mínimo número de operaciones para convertir la cadena a en la cadena b, donde cada operación es INSERTAR un carácter, BORRAR uno o CAMBIAR uno por otro (cada una cuesta 1). |
| [Memoización vs tabulación («Top-down / bottom-up»)](03_ProgramacionDinamica/memoizacion.py) | Básico | Toda DP se puede escribir de dos formas: TOP-DOWN (recursión + memoria: la función se llama a sí misma y guarda cada resultado la primera vez que lo calcula) o BOTTOM-UP (una tabla que se llena en un orden en el que los subproblemas que se necesitan ya están listos). |
| [Mochila 0/1 («0/1 knapsack»)](03_ProgramacionDinamica/mochila_01.py) | Básico | Hay n objetos, cada uno con peso p_i y valor v_i, y una mochila de capacidad W. |
| [Mochila ilimitada («Unbounded knapsack»)](03_ProgramacionDinamica/mochila_ilimitada.py) | Básico | Hay n TIPOS de objetos (peso p_i, valor v_i) y de cada tipo se pueden tomar todas las copias que se quiera. |
| [Subsecuencia común más larga («Longest Common Subsequence», LCS)](03_ProgramacionDinamica/lcs.py) | Básico | Dadas dos secuencias a y b, encontrar la secuencia más larga que es subsecuencia de ambas (se pueden saltar elementos pero no reordenar), y mostrarla. |
| [Subsecuencia creciente más larga («Longest Increasing Subsequence», LIS)](03_ProgramacionDinamica/lis.py) | Básico/Intermedio | Dado un arreglo, encontrar la subsecuencia (no necesariamente contigua, respetando el orden) estrictamente creciente más larga, y mostrarla. |
| [DP de dígitos («Digit DP»)](03_ProgramacionDinamica/dp_digitos.py) | Intermedio | Contar cuántos enteros x en [0, N] (o en [a, b]) cumplen una propiedad que depende de sus DÍGITOS: suma de dígitos igual a S, sin dos dígitos vecinos iguales, sin el dígito 4, divisible por K, cantidad de unos en binario… con N hasta 10^18 (imposible recorrerlos uno por uno). |
| [DP de intervalos: cadena de matrices («Interval DP / Matrix chain multiplication»)](03_ProgramacionDinamica/dp_intervalos.py) | Intermedio | Problemas donde la respuesta para un tramo contiguo [i, j] se arma eligiendo DÓNDE partirlo (o qué elemento queda último/primero) y combinando las respuestas de los dos pedazos. |
| [DP en árboles, iterativa («Tree DP / rerooting»)](03_ProgramacionDinamica/dp_arboles.py) | Intermedio | Calcular algo para cada subárbol de un árbol combinando lo de sus hijos: tamaños, el conjunto independiente de peso máximo (elegir nodos sin elegir dos vecinos), emparejamientos, mochila en árbol… Y con «rerooting», calcular una respuesta para CADA posible raíz en O(n) en vez de O(n²) (p. |
| [DP sobre máscaras de bits: TSP y asignación («Bitmask DP»)](03_ProgramacionDinamica/dp_mascaras.py) | Intermedio | Cuando el estado natural es «qué SUBCONJUNTO de elementos ya usé» y n es pequeño (n ≤ 20 en C++, ≤ ~15–17 en Python), el subconjunto se guarda como un entero de n bits (máscara) y se hace DP sobre las 2^n máscaras. |
| [DP sobre un DAG con orden topológico («DP on DAG»)](03_ProgramacionDinamica/dp_dag.py) | Intermedio | Toda DP es, en el fondo, un cálculo sobre un grafo dirigido ACÍCLICO (DAG): los estados son nodos y «el estado v depende de u» es una arista u -> v. |
| [Partición en piezas sobre prefijos («Word break / partition DP»)](03_ProgramacionDinamica/dp_particion_prefijos.py) | Intermedio | Partir una cadena (o un arreglo) en pedazos CONTIGUOS que cumplan alguna condición, y decir si se puede, de cuántas formas, o con el mínimo / máximo de algo. |
| [Reconstrucción de la solución óptima («Solution reconstruction»)](03_ProgramacionDinamica/reconstruccion_solucion.py) | Intermedio | La DP da el VALOR óptimo; muchos problemas además piden «muestre una solución», «imprima los objetos elegidos», o «si hay varias, la lexicográficamente menor». |
| [Convex hull trick y árbol de Li Chao («CHT / Li Chao tree»)](03_ProgramacionDinamica/convex_hull_trick.py) | Avanzado | Acelerar DP del tipo dp[i] = min_{j < i} ( dp[j] + b_j · x_i + c_j ) + d_i donde el término que mezcla i y j es un PRODUCTO (algo de j) · (algo de i). |
| [DP de perfil / perfil roto («Broken profile DP»)](03_ProgramacionDinamica/dp_perfil.py) | Avanzado | Contar formas de llenar una grilla n×m (con m pequeño, m ≤ ~10–12) con piezas que se tocan solo entre celdas vecinas: el clásico es contar los embaldosados con dominós 1×2 (horizontales o verticales), con o sin celdas bloqueadas. |
| [Optimización de Knuth para DP de intervalos («Knuth–Yao optimization»)](03_ProgramacionDinamica/optimizacion_knuth.py) | Avanzado | Bajar de O(n³) a O(n²) las DP de intervalos de la forma dp[i][j] = min_{i ≤ k < j} (dp[i][k] + dp[k+1][j]) + w(i, j) cuando el costo w cumple ciertas desigualdades. |
| [Optimización divide y vencerás («Divide and conquer DP optimization»)](03_ProgramacionDinamica/dp_divide_venceras.py) | Avanzado | Acelerar DP de partición en K grupos de la forma dp[g][i] = min_{j < i} dp[g-1][j] + C(j, i) (partir los primeros i elementos en g grupos contiguos; el último grupo es a[j:i]) de O(K·n²) a O(K·n log n), cuando el corte óptimo es MONÓTONO: opt[g][i] ≤ opt[g][i+1]. |
| [Suma sobre subconjuntos («Sum over Subsets, SOS DP»)](03_ProgramacionDinamica/sos_dp.py) | Avanzado | Dado un valor f[mask] para cada máscara de B bits, calcular para TODAS las máscaras a la vez g[mask] = Σ_{sub ⊆ mask} f[sub] (suma sobre subconjuntos) o la versión sobre superconjuntos, en O(B · 2^B) en vez de O(3^B) o O(4^B). |

## 04 · Cadenas (15)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Frecuencias de letras y anagramas («Anagrams»)](04_Cadenas/frecuencias_anagramas.py) | Básico | Contar cuántas veces aparece cada letra resuelve todo lo que «no depende del orden»: decidir si dos palabras son anagramas, agrupar palabras con las mismas letras, encontrar ventanas de un texto que son permutación de un patrón, o saber si se puede formar una palabra con otras letras. |
| [Palíndromos: verificar y expansión desde el centro («Expand around center»)](04_Cadenas/palindromos.py) | Básico | Decidir si una cadena se lee igual al derecho y al revés, y encontrar la subcadena palíndroma más larga (o contar todas) en O(n²) sin estructuras raras: suficiente para n ≤ ~3000 en Python. |
| [Paréntesis balanceados con pila («Balanced brackets / stack parsing»)](04_Cadenas/parentesis_pila.py) | Básico | Todo lo que tiene estructura ANIDADA se procesa con una pila: verificar que los paréntesis cierren bien, encontrar la pareja de cada uno, medir la profundidad de anidamiento, evaluar expresiones aritméticas o reconstruir un árbol escrito como f(g(x), y). |
| [Prefijo común más largo de varias cadenas («Longest common prefix»)](04_Cadenas/prefijo_comun.py) | Básico | Encontrar el prefijo más largo que comparten TODAS las cadenas de una lista (o el mayor que comparte algún par). |
| [Algoritmo de Manacher («Manacher's algorithm»)](04_Cadenas/manacher.py) | Intermedio | Calcula en O(n), para cada centro de la cadena, el radio del palíndromo más largo centrado allí. |
| [Función prefijo y búsqueda KMP («Knuth–Morris–Pratt, prefix function»)](04_Cadenas/kmp.py) | Intermedio | Encontrar TODAS las apariciones de un patrón P en un texto T en O(/T/ + /P/), y responder preguntas de estructura de una cadena: bordes (prefijos que también son sufijos), periodo mínimo, si la cadena es una potencia u^k, cuántas veces aparece cada prefijo. |
| [Función Z y búsqueda de patrones («Z-function / Z-algorithm»)](04_Cadenas/funcion_z.py) | Intermedio | Calcula, para CADA posición i de una cadena, cuánto coincide s[i:] con el comienzo de s. |
| [Hashing polinomial con doble módulo («Rolling hash / polynomial hashing»)](04_Cadenas/hashing_polinomial.py) | Intermedio | Convierte cada subcadena s[i:j] en un número, calculable en O(1) tras un preproceso O(n). |
| [Trie o árbol de prefijos («Trie / prefix tree»)](04_Cadenas/trie.py) | Intermedio | Guarda un diccionario de palabras como un árbol donde cada camino desde la raíz deletrea un prefijo. |
| [Aho–Corasick: muchos patrones a la vez («Aho–Corasick automaton»)](04_Cadenas/aho_corasick.py) | Avanzado | Buscar MUCHOS patrones en un texto en una sola pasada: cuántas veces aparece cada patrón, o dónde aparece cada uno. |
| [Arreglo de sufijos + LCP de Kasai («Suffix array, prefix doubling + Kasai»)](04_Cadenas/suffix_array.py) | Avanzado | El arreglo de sufijos es la lista de posiciones de inicio de todos los sufijos de s, ordenados lexicográficamente. |
| [Autómata de sufijos («Suffix automaton, SAM»)](04_Cadenas/suffix_automaton.py) | Avanzado | Es el autómata determinista más pequeño que acepta exactamente las subcadenas de s (tiene ≤ 2n-1 estados). |
| [Distancia de edición bit-paralela de Myers («Myers' bit-vector algorithm»)](04_Cadenas/myers_bit_paralelo.py) | Avanzado | Calcula la distancia de Levenshtein (mínimo de inserciones, borrados y sustituciones para convertir a en b) guardando una COLUMNA ENTERA de la tabla de programación dinámica en dos enteros de bits, y procesando cada letra de b con ~15 operaciones de bits. |
| [Rotación mínima (Booth / dos punteros) y factorización de Lyndon (Duval)](04_Cadenas/rotacion_minima.py) | Avanzado | Para una cadena CIRCULAR (collar, huella, polígono descrito por su secuencia de lados) da su representante canónico: la rotación lexicográficamente menor, en O(n). |
| [Secuencia de De Bruijn con palabras de Lyndon («De Bruijn sequence, FKM algorithm»)](04_Cadenas/de_bruijn.py) | Avanzado | Una secuencia de De Bruijn B(k, n) es una cadena CIRCULAR de largo k^n sobre un alfabeto de k símbolos en la que cada palabra de largo n aparece exactamente una vez como ventana. |

## 05 · Grafos (27)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Búsqueda en anchura («Breadth-First Search, BFS»)](05_Grafos/bfs.py) | Básico | Calcular la distancia mínima (en NÚMERO DE ARISTAS) desde un vértice a todos los demás en un grafo SIN pesos (o con todos los pesos iguales), y reconstruir un camino más corto. |
| [Búsqueda en profundidad iterativa («Depth-First Search, DFS»)](05_Grafos/dfs.py) | Básico | Recorrer un grafo yendo «lo más hondo posible» antes de retroceder. |
| [Componentes conexas («Connected components»)](05_Grafos/componentes_conexas.py) | Básico | Partir un grafo NO dirigido en sus «pedazos»: dos vértices están en la misma componente si hay un camino entre ellos. |
| [Grafo bipartito / 2-coloración («Bipartite check, 2-coloring»)](05_Grafos/bipartito.py) | Básico | Decidir si los vértices de un grafo se pueden pintar con DOS colores de modo que toda arista una vértices de distinto color (equivalente: partir los vértices en dos grupos sin aristas dentro de un grupo), y dar la coloración. |
| [Relleno por inundación en grillas («Flood fill»)](05_Grafos/flood_fill.py) | Básico | Pintar / marcar toda la región conectada de una grilla que contiene una celda dada (el «balde de pintura» de un editor de imágenes), y con eso contar regiones: islas, lagos, cuartos, manchas de petróleo, y medir su tamaño. |
| [Representación de grafos («Graph representation»)](05_Grafos/representacion_grafos.py) | Básico | Antes de correr cualquier algoritmo de grafos hay que GUARDAR el grafo en una estructura. |
| [Bellman-Ford y ciclos negativos («Bellman-Ford algorithm»)](05_Grafos/bellman_ford.py) | Intermedio | Distancias mínimas desde un origen cuando hay pesos NEGATIVOS (donde Dijkstra falla), detectando además los ciclos negativos: si se puede dar vueltas en un ciclo de costo total < 0, algunas distancias son −∞. |
| [BFS 0-1 con deque («0-1 BFS»)](05_Grafos/bfs_01.py) | Intermedio | Distancias mínimas desde un origen cuando cada arista cuesta 0 o 1. |
| [BFS sobre espacio de estados («State-space BFS»)](05_Grafos/bfs_estados.py) | Intermedio | Muchos problemas de «mínimo número de operaciones» no traen un grafo explícito: los VÉRTICES son las configuraciones posibles (estados) y las ARISTAS son las operaciones permitidas. |
| [Detección de ciclos (dirigido y no dirigido) («Cycle detection»)](05_Grafos/deteccion_ciclos.py) | Intermedio | Decidir si un grafo tiene un ciclo y, si lo tiene, ENTREGAR uno (la lista de vértices). |
| [Dijkstra con montículo («Dijkstra's algorithm»)](05_Grafos/dijkstra.py) | Intermedio | Distancias mínimas desde un origen a todos los vértices en un grafo (dirigido o no) con pesos NO NEGATIVOS, y reconstrucción del camino. |
| [Diámetro de un árbol con dos BFS y centro del árbol («Tree diameter», «tree center»)](05_Grafos/diametro_arbol.py) | Intermedio | Diámetro: el camino más largo entre dos nodos de un árbol (en número de aristas o en suma de pesos no negativos). |
| [Floyd–Warshall y clausura transitiva («Floyd–Warshall algorithm»)](05_Grafos/floyd_warshall.py) | Intermedio | Distancias mínimas entre TODOS los pares de vértices (admite pesos negativos y detecta ciclos negativos) con un código de 4 líneas. |
| [Grafos funcionales: ciclos, liebre y tortuga de Floyd, k-ésimo sucesor](05_Grafos/grafo_funcional.py) | Intermedio/Avanzado | Un grafo funcional es uno donde cada nodo tiene EXACTAMENTE una arista de salida: v → f(v). |
| [Orden topológico con el algoritmo de Kahn («Topological sort, Kahn»)](05_Grafos/orden_topologico.py) | Intermedio | Ordenar los vértices de un grafo DIRIGIDO de modo que toda arista u→v quede con u antes que v (tareas con prerrequisitos). |
| [Puentes y puntos de articulación («Bridges and articulation points»)](05_Grafos/puentes_articulacion.py) | Intermedio | En un grafo NO dirigido: · PUENTE: arista cuya eliminación aumenta el número de componentes conexas (desconecta algo). |
| [Union-Find / conjuntos disjuntos («Disjoint Set Union, DSU»)](05_Grafos/union_find.py) | Intermedio | Mantener una partición de n elementos en grupos que solo se UNEN (nunca se separan), respondiendo «¿a y b están en el mismo grupo?» y «¿qué tamaño tiene el grupo de a?» en tiempo casi constante. |
| [Árbol de expansión mínima: Kruskal y Prim («Minimum Spanning Tree»)](05_Grafos/mst.py) | Intermedio | En un grafo NO dirigido y ponderado, elegir n−1 aristas que conecten a todos los vértices con el menor costo total (un árbol: sin ciclos). |
| [2-SAT con componentes fuertemente conexas («2-satisfiability»)](05_Grafos/dos_sat.py) | Avanzado | Decidir si n variables booleanas pueden tomar valores que cumplan un conjunto de cláusulas de la forma (a ∨ b), donde a y b son literales (x_i o ¬x_i), y construir una asignación válida si existe. |
| [Ancestro común más bajo con binary lifting («Lowest Common Ancestor»)](05_Grafos/lca.py) | Avanzado | En un árbol con raíz, el LCA de u y v es el ancestro común más profundo. |
| [Asignación de costo mínimo: algoritmo húngaro O(n³) («Hungarian algorithm»)](05_Grafos/hungaro.py) | Avanzado | Dada una matriz de costos a[i][j] (trabajador i hace la tarea j), asignar a cada fila una columna DISTINTA minimizando la suma de costos (o maximizando la ganancia, cambiando signos). |
| [Camino y circuito euleriano con Hierholzer («Eulerian path / circuit»)](05_Grafos/euler_hierholzer.py) | Avanzado | Recorrer TODAS las aristas de un grafo exactamente una vez (camino euleriano), volviendo al inicio si se pide un circuito. |
| [Componentes fuertemente conexas («Strongly Connected Components»: Tarjan y Kosaraju)](05_Grafos/scc.py) | Avanzado | En un grafo DIRIGIDO, partir los vértices en grupos maximales donde cada uno llega a cada otro (u →* v y v →* u). |
| [Corte mínimo s-t a partir del flujo máximo («Min s-t cut»)](05_Grafos/corte_minimo.py) | Avanzado | Encontrar el conjunto de aristas (o de vértices) de costo total mínimo cuya eliminación deja a t inalcanzable desde s, y decir CUÁLES son. |
| [Emparejamiento bipartito máximo: Kuhn y Hopcroft–Karp; teorema de König](05_Grafos/emparejamiento_bipartito.py) | Avanzado | Dado un grafo bipartito (izquierda L, derecha R; p. |
| [Flujo máximo con Dinic («Dinic's algorithm»)](05_Grafos/dinic.py) | Avanzado | Lo mismo que Edmonds–Karp (flujo máximo de s a t con capacidades, y por el teorema max-flow min-cut, el corte mínimo), pero mucho más rápido: es el algoritmo de flujo que conviene tener en la libreta. |
| [Flujo máximo con Edmonds–Karp («Max flow, Edmonds–Karp»)](05_Grafos/edmonds_karp.py) | Avanzado | Calcular cuánto «material» (agua, datos, personas) puede pasar como máximo de una fuente s a un sumidero t en una red donde cada arista tiene una capacidad. |

## 06 · EstructurasDatos (10)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Montículo con heapq («Binary heap / priority queue»)](06_EstructurasDatos/monticulo_heapq.py) | Básico | Mantener una colección que cambia y responder rápido «¿cuál es el mínimo (o el máximo)?»: insertar y sacar el mínimo en O(log N), ver el mínimo en O(1). |
| [Consultas offline con Fenwick («Offline queries + BIT»)](06_EstructurasDatos/consultas_offline.py) | Intermedio | Cuando TODAS las consultas se conocen de antemano (se leen todas antes de responder), se pueden reordenar como convenga y procesarlas junto con los datos en un barrido, con un Fenwick que mantiene «lo que ya pasó». |
| [Enteros de Python como bitsets («Bitset with Python big ints»)](06_EstructurasDatos/bitsets.py) | Intermedio | Un int de Python tiene tamaño arbitrario: un entero de N bits ES un conjunto de {0..N-1} (bit i encendido = i pertenece). |
| [Pila monótona («Monotonic stack»)](06_EstructurasDatos/pila_monotona.py) | Intermedio | Para cada posición i de un arreglo, encontrar en O(N) TOTAL el primer elemento a la derecha (o izquierda) que es mayor (o menor) que a[i]. |
| [Segment tree iterativo («Segment tree, bottom-up»)](06_EstructurasDatos/segment_tree.py) | Intermedio | Mantener un arreglo con actualizaciones PUNTUALES y consultas de RANGO de cualquier operación asociativa (suma, mínimo, máximo, gcd, xor, composición de funciones…) en O(log N) cada una. |
| [Sparse table para RMQ estático («Sparse table, range minimum query»)](06_EstructurasDatos/sparse_table.py) | Intermedio | Responder en O(1) muchas consultas «mínimo (o máximo, gcd, AND, OR) de a[l..r-1]» sobre un arreglo que NO cambia, tras un preprocesamiento O(N log N). |
| [Árbol de Fenwick («Fenwick tree / Binary Indexed Tree, BIT»)](06_EstructurasDatos/fenwick.py) | Intermedio | Mantener un arreglo que cambia con dos operaciones en O(log N): «sumar delta a la posición i» y «suma de los primeros i elementos» (y por resta, la suma de cualquier rango). |
| [Algoritmo de Mo («Mo's algorithm»)](06_EstructurasDatos/algoritmo_mo.py) | Avanzado | Responder Q consultas OFFLINE sobre rangos a[l..r-1] de un arreglo fijo cuando la respuesta se puede mantener al AGREGAR o QUITAR un elemento en un extremo en O(1), pero no se puede combinar a partir de dos mitades (por eso no sirve un segment tree). |
| [Descomposición en raíz cuadrada («Sqrt decomposition»)](06_EstructurasDatos/descomposicion_raiz.py) | Avanzado | Partir el arreglo en ~√N bloques de ~√N elementos y guardar un resumen por bloque (suma, mínimo, arreglo ordenado, etiqueta perezosa…). |
| [Segment tree con propagación perezosa («Lazy propagation»)](06_EstructurasDatos/segment_tree_lazy.py) | Avanzado | Actualizaciones de RANGO y consultas de RANGO, ambas en O(log N). |

## 07 · Matematicas (33)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Aritmética modular («Modular arithmetic»)](07_Matematicas/aritmetica_modular.py) | Básico | Hacer cuentas con números que serían gigantes guardando solo su resto módulo m. |
| [Combinatoria básica: factoriales, variaciones, combinaciones y Pascal](07_Matematicas/combinatoria_basica.py) | Básico | Contar de cuántas formas se pueden ordenar o escoger objetos sin enumerarlos: permutaciones (n!), variaciones (ordenar k de n), combinaciones (escoger k de n sin orden), con y sin repetición, y permutaciones de multiconjuntos (multinomial). |
| [Contar por complemento: buenos = total − malos («complementary counting»)](07_Matematicas/conteo_complemento.py) | Básico | Cuando contar directamente los objetos «buenos» es difícil (muchos casos, condiciones de «al menos uno») pero contar el TOTAL y los «malos» es fácil. |
| [Criba de Eratóstenes, criba lineal (SPF) y criba segmentada («Sieve of Eratosthenes»)](07_Matematicas/criba_eratostenes.py) | Básico (criba lineal y segmentada: Intermedio) | Saber de golpe cuáles números hasta N son primos (N hasta ~10^7 en Python), obtener la lista de primos, o el MENOR FACTOR PRIMO de cada número (para factorizar muchos números en O(log n) cada uno). |
| [Exponenciación rápida («Binary exponentiation», «exponentiation by squaring»)](07_Matematicas/exponenciacion_rapida.py) | Básico | Calcular a^b (normalmente módulo m) con b hasta 10^18 o más en O(log b) multiplicaciones, en vez de b multiplicaciones. |
| [Máximo común divisor y mínimo común múltiplo («GCD / LCM», algoritmo de Euclides)](07_Matematicas/gcd_lcm.py) | Básico | Calcular el mayor entero que divide a dos (o más) números (gcd = mcd) y el menor entero positivo que es múltiplo de todos ellos (lcm = mcm), en O(log) pasos aunque los números sean de 10^18. |
| [Prueba de primalidad por división hasta √n («Trial division», forma 6k ± 1)](07_Matematicas/primalidad.py) | Básico | Decidir si UN número n es primo, sin precalcular nada, en O(√n). |
| [Trucos de bits y XOR: x & -x, popcount, submáscaras, contribución por bit](07_Matematicas/trucos_bits.py) | Básico/Intermedio | Operar con enteros como conjuntos de bits (máscaras) en O(1), y resolver sumas sobre XOR (o AND/OR) separando la cuenta POR BIT: cada bit se comporta de forma independiente. |
| [C(n, k) módulo un primo: factoriales precomputados y teorema de Lucas](07_Matematicas/ncr_modular.py) | Intermedio | Responder MUCHAS consultas C(n, k) mód p (p primo, típicamente 10^9+7 o 998244353) en O(1) cada una tras un precálculo O(N). |
| [Divisores: enumerar, contar y sumar («Divisors», funciones d(n) y σ(n))](07_Matematicas/divisores.py) | Intermedio | Listar todos los divisores de n, o saber cuántos tiene (d(n)) y cuánto suman (σ(n)) sin listarlos, a partir de la factorización. |
| [Ecuación diofántica lineal a·x + b·y = c («Linear Diophantine equation»)](07_Matematicas/diofantica_lineal.py) | Intermedio | Encontrar soluciones ENTERAS de a·x + b·y = c: decidir si existen, dar todas (familia con un parámetro t) y contar cuántas caen en un rango x1 ≤ x ≤ x2, y1 ≤ y ≤ y2 en O(log), sin recorrer el rango. |
| [Eliminación gaussiana: exacta (Fraction), módulo p y en GF(2) («Gaussian elimination»)](07_Matematicas/eliminacion_gaussiana.py) | Intermedio/Avanzado | Resolver un sistema lineal A·x = b de m ecuaciones y n incógnitas y decir si no tiene solución, tiene una única o infinitas; calcular el rango y el determinante. |
| [Estrellas y barras, con cotas inferiores y superiores («stars and bars»)](07_Matematicas/estrellas_barras.py) | Intermedio | Contar de cuántas formas se reparten n objetos IDÉNTICOS en k cajas DISTINTAS, o equivalentemente cuántas soluciones enteras tiene x_1 + x_2 + … + x_k = n con x_i ≥ 0 (o con mínimos y máximos por caja). |
| [Euclides extendido e inverso modular («Extended Euclidean algorithm», «modular inverse»)](07_Matematicas/euclides_extendido.py) | Intermedio | Además de g = gcd(a, b), encontrar enteros x, y con a·x + b·y = g (identidad de Bézout). |
| [Exponenciación de matrices: Fibonacci y recurrencias lineales («matrix exponentiation»)](07_Matematicas/exponenciacion_matrices.py) | Intermedio | Calcular el término n-ésimo de un proceso lineal (recurrencia lineal, número de caminos de largo n en un grafo, DP cuya transición es la misma en cada paso) cuando n es ENORME (10^9–10^18), en O(k³ log n) con k el tamaño del estado. |
| [Factorización en primos: división de prueba y menor factor primo («Prime factorization», «trial division», «SPF»)](07_Matematicas/factorizacion.py) | Intermedio | Escribir n = p1^e1 · p2^e2 · … · pk^ek. |
| [Función φ de Euler y teorema de Euler («Euler's totient function»)](07_Matematicas/phi_euler.py) | Intermedio | φ(n) = cuántos k en 1..n son coprimos con n. |
| [Invariantes y paridad: paridad de permutaciones y resolubilidad del 15-puzzle](07_Matematicas/invariantes_paridad.py) | Intermedio | Probar que una configuración NO se puede alcanzar (o que sí) sin explorar el espacio de estados: se busca una cantidad que ninguna jugada cambia (INVARIANTE), típicamente una paridad o un resto módulo algo. |
| [Juegos: DP de posiciones ganadoras/perdedoras y minimax («winning/losing positions»)](07_Matematicas/posiciones_ganadoras.py) | Intermedio | Decidir quién gana un juego de dos jugadores con información completa y sin azar, jugando ambos óptimamente, calculando para CADA posición si es ganadora (G) o perdedora (P) para quien mueve; o, si hay puntaje, la mejor diferencia de puntos que puede asegurar (minimax). |
| [Nim y teorema de Sprague–Grundy (números de Grundy, suma de juegos)](07_Matematicas/nim_sprague_grundy.py) | Intermedio/Avanzado | Decidir quién gana un juego IMPARCIAL (las mismas jugadas para ambos jugadores, información completa, sin azar, pierde quien no puede jugar) cuando el juego es la SUMA de varios juegos independientes: en cada turno se elige uno de los subjuegos y se juega en él. |
| [Números de Catalan: fórmula, recurrencia y qué cuentan («Catalan numbers»)](07_Matematicas/catalan.py) | Intermedio | La sucesión 1, 1, 2, 5, 14, 42, 132, 429, 1430, … (C_0, C_1, …) aparece en muchísimos conteos de estructuras «anidadas» o «que no se cruzan». |
| [Principio de inclusión–exclusión («inclusion–exclusion principle»)](07_Matematicas/inclusion_exclusion.py) | Intermedio | Contar elementos de una UNIÓN de conjuntos que se solapan, sabiendo contar fácilmente las INTERSECCIONES: /A1 ∪ … ∪ Am/. |
| [Probabilidad y esperanza: linealidad, DP de probabilidad, Fraction y mód p](07_Matematicas/probabilidad_esperanza.py) | Intermedio | Calcular probabilidades y valores esperados de procesos aleatorios discretos sin simular: contando casos favorables / totales, con DP sobre estados (probabilidad de llegar a cada estado) o con la LINEALIDAD DE LA ESPERANZA (sumar la contribución de cada pieza). |
| [Rango y des-rango de combinaciones y permutaciones («ranking / unranking»)](07_Matematicas/rango_combinacion.py) | Intermedio | Pasar de un objeto combinatorio (un k-subconjunto, una permutación) a su POSICIÓN en orden lexicográfico (rango) y al revés (des-rango), sin generar la lista completa, que puede tener 10^17 elementos. |
| [Teorema chino del resto, con módulos no coprimos («Chinese Remainder Theorem», CRT)](07_Matematicas/teorema_chino_resto.py) | Intermedio | Resolver un sistema x ≡ r1 (mód m1), x ≡ r2 (mód m2), …, x ≡ rk (mód mk) devolviendo la solución como UNA congruencia x ≡ r (mód mcm(m1, …, mk)), o informar que es incompatible. |
| [Berlekamp–Massey: la recurrencia lineal mínima de una sucesión mód p](07_Matematicas/berlekamp_massey.py) | Avanzado | Dados los primeros N términos s_0..s_{N−1} de una sucesión (mód p primo), encontrar la recurrencia lineal MÁS CORTA s_i = c_1·s_{i−1} + … + c_L·s_{i−L} (para todo L ≤ i < N) en O(N²). |
| [Ecuación de Pell x² − D·y² = ±1 con fracciones continuas («Pell's equation»)](07_Matematicas/pell.py) | Avanzado | Encontrar los enteros positivos x, y con x² − D·y² = 1 (o = −1), D > 0 no cuadrado perfecto. |
| [Funciones generatrices con polinomios truncados («generating functions»)](07_Matematicas/funciones_generatrices.py) | Avanzado | Codificar un problema de conteo como una serie A(x) = Σ a_n x^n donde a_n es la respuesta para el tamaño n. |
| [Kitamasa: n-ésimo término de una recurrencia lineal en O(k² log n) («Kitamasa method»)](07_Matematicas/kitamasa.py) | Avanzado | Calcular f(n) mód p para una recurrencia lineal homogénea de orden k f(i) = c_1·f(i−1) + c_2·f(i−2) + … + c_k·f(i−k) con n hasta 10^18, en O(k² log n) en vez del O(k³ log n) de la exponenciación de matrices. |
| [Lema de Burnside: collares, pulseras y coloreos bajo simetría («Burnside's lemma»)](07_Matematicas/burnside.py) | Avanzado | Contar objetos «distintos salvo simetría»: dos coloreos se consideran iguales si uno se obtiene del otro rotando (o reflejando, girando la cuadrícula…). |
| [Logaritmo discreto: paso de bebé, paso de gigante («Baby-step giant-step», BSGS)](07_Matematicas/logaritmo_discreto.py) | Avanzado | Hallar el menor x ≥ 0 con a^x ≡ b (mód m), en O(√m) en vez de O(m). |
| [Miller–Rabin determinista y Pollard-Rho («Miller–Rabin primality test», «Pollard's rho»)](07_Matematicas/miller_rabin_pollard.py) | Avanzado | Decidir si n ≤ 2^64 (y bastante más) es primo en O(log n) multiplicaciones modulares, y factorizar n ≈ 10^18 en ~O(n^(1/4)) pasos, cuando la división de prueba (O(√n) = 10^9) es imposible. |
| [Árbol de Stern–Brocot y sucesión de Farey: mejor aproximación racional](07_Matematicas/stern_brocot_farey.py) | Avanzado | Trabajar con fracciones de denominador acotado: listar todas las fracciones irreducibles en [0, 1] con denominador ≤ N en orden (Farey), encontrar la fracción con denominador ≤ N más cercana por arriba o por abajo a un racional x (mejor aproximación), o recorrer/codificar racionales como caminos L/R en el árbol de Stern–Brocot. |

## 08 · Geometria (17)

| Algoritmo | Nivel | Para qué sirve |
|---|---|---|
| [Orientación de tres puntos y punto sobre segmento («CCW test»)](08_Geometria/orientacion_ccw.py) | Básico | Decidir si al ir de A a B y luego a C se gira a la izquierda (antihorario, CCW), a la derecha (horario, CW) o se sigue derecho (colineales). |
| [Precisión: epsilon, enteros, Fraction y redondeo de salida](08_Geometria/precision_flotantes.py) | Básico | Evitar el error más común en geometría: decidir mal una comparación porque 0.1 + 0.2 != 0.3. |
| [Vectores, producto punto y producto cruz («dot / cross product»)](08_Geometria/vectores_productos.py) | Básico | Es el «alfabeto» de toda la geometría computacional: casi cualquier pregunta (¿gira a la izquierda?, ¿son perpendiculares?, ¿qué ángulo forman?, ¿qué área tiene?, ¿dónde cae la proyección?) se responde con sumas, restas, producto punto y producto cruz de vectores 2D. |
| [Área de un polígono: fórmula del zapato («shoelace formula»)](08_Geometria/area_poligono.py) | Básico | Calcular en O(n) el área de un polígono simple (sin autointersecciones, convexo o no) dados sus vértices en orden, saber si está orientado en sentido antihorario u horario, y hallar su centroide (centro de masa de la lámina). |
| [Círculos: intersecciones, tangencias y punto en anillo («circles»)](08_Geometria/circulos.py) | Intermedio | Resolver las preguntas típicas con círculos: ¿dónde se cortan dos círculos? ¿dónde corta una recta a un círculo? ¿son tangentes, uno contiene al otro? ¿un punto está dentro de un anillo (corona)? Señales en el enunciado: «radio», «alcance», «cobertura de una antena», «brazo/cuerda de longitud L», «tangentes», «zona entre dos círculos», «¿el disparo/trayectoria toca el obstáculo circular?». |
| [Envolvente convexa: cadena monótona de Andrew («convex hull, monotone chain»)](08_Geometria/envolvente_convexa.py) | Intermedio | Hallar el menor polígono convexo que contiene a un conjunto de puntos (la «liga elástica» que los rodea), en O(n log n). |
| [Intersección de segmentos y de rectas («segment intersection»)](08_Geometria/interseccion_segmentos.py) | Intermedio | Saber si dos segmentos se tocan (incluyendo tocarse en un extremo o solaparse sobre la misma recta) y, si se cortan, en qué punto; y hallar el punto de corte de dos rectas. |
| [Proyección y distancias punto–recta, punto–segmento («projection»)](08_Geometria/proyeccion_distancias.py) | Intermedio | Encontrar el punto de una recta (o de un segmento) más cercano a un punto dado, su distancia, el reflejo de un punto respecto a una recta, y la distancia entre dos segmentos. |
| [Punto en polígono: dentro, fuera o borde («ray casting / winding number»)](08_Geometria/punto_en_poligono.py) | Intermedio | Decidir si un punto está dentro, fuera o sobre el borde de un polígono simple (convexo o NO convexo) en O(n). |
| [Teorema de Pick y puntos enteros en el borde («Pick's theorem»)](08_Geometria/teorema_pick.py) | Intermedio | Contar en O(n log C) cuántos puntos de coordenadas enteras hay dentro y sobre el borde de un polígono simple cuyos vértices son enteros, sin recorrerlos uno a uno (el polígono puede medir 10^9 × 10^9). |
| [Calibradores rotatorios: diámetro y triángulo de área máxima («rotating calipers»)](08_Geometria/rotating_calipers.py) | Avanzado | Resolver problemas de «los puntos más alejados» sobre un conjunto de puntos recorriendo su envolvente convexa con dos (o tres) punteros que solo avanzan: el DIÁMETRO (par de puntos más lejanos) en O(n log n) y el TRIÁNGULO DE ÁREA MÁXIMA con vértices en el conjunto en O(n log n + h²). |
| [Capas convexas: «pelar la cebolla» («convex layers / onion peeling»)](08_Geometria/capas_convexas.py) | Avanzado | Partir un conjunto de puntos en capas: la capa 1 es el borde de la envolvente convexa; se quitan esos puntos y la capa 2 es el borde de la envolvente de los que quedan; y así hasta vaciar. |
| [Intersección de semiplanos y recorte de convexos («half-plane intersection»)](08_Geometria/semiplanos.py) | Avanzado | Hallar la región (convexa) de puntos que cumplen a la vez muchas restricciones lineales del tipo «estar a la izquierda de la recta a→b». |
| [Línea de barrido: máximo de intervalos solapados y área de la unión de rectángulos («sweep line»)](08_Geometria/linea_de_barrido.py) | Avanzado | Convertir un problema 2D (o de intervalos) en una secuencia ORDENADA de eventos que una recta imaginaria va encontrando al barrer el plano de izquierda a derecha, manteniendo una estructura con «lo que la recta está cortando ahora». |
| [Par de puntos más cercano en O(n log n) («closest pair, divide and conquer»)](08_Geometria/par_mas_cercano.py) | Avanzado | Encontrar los dos puntos más cercanos entre n puntos del plano en O(n log n), cuando comparar todos los pares (O(n²)) no alcanza. |
| [Punto en polígono convexo en O(log n) («point in convex polygon, binary search»)](08_Geometria/punto_en_convexo_logn.py) | Avanzado | Responder MUCHAS consultas «¿el punto p está dentro, en el borde o fuera del polígono convexo?» en O(log n) cada una, en vez de O(n). |
| [Teorema del eje separador: ¿se intersecan dos convexos? («SAT»)](08_Geometria/eje_separador.py) | Avanzado | Decidir si dos polígonos CONVEXOS se tocan o están separados, y con eso si dos conjuntos de puntos se pueden separar con una recta (separabilidad lineal): basta mirar sus envolventes convexas. |
