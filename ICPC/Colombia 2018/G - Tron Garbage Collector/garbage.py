"""
Colombia 2018 — G: Tron Garbage Collector («El recolector de basura Tron»)
Ejecutar: python garbage.py < garbage.in
Autor de la solución: César A. Vega F. <cesar.a.vega.f@gmail.com>

CONTEXTO
    La memoria es «Squareland», una cuadrícula R×C: las líneas son calles y
    cada casilla tiene basura. Un carro recorre calles; una casilla con
    número d (0..4) debe tener EXACTAMENTE d de sus 4 lados recorridos
    (0 = no se puede tocar), y una casilla «.» no tiene restricción. La ruta
    empieza y termina en la misma esquina y no repite esquinas: es un ciclo
    simple sobre las calles. (Es el rompecabezas «Slitherlink».)

QUÉ HAY QUE HACER
    Entrada: casos «R C» + R líneas de C símbolos (dígito 0..4 o «.»),
             hasta «0 0».
    Salida:  «YES» si existe un ciclo simple que cumpla todos los números,
             «NO» si no.
    Restricciones clave: 0 < R, C < 6 → hasta 25 casillas, 36 esquinas y
             60 calles. Una cuadrícula de 6×6 esquinas tiene ~1.2·10^6
             ciclos simples: enumerarlos en Python es demasiado lento cuando
             la respuesta es NO.

IDEA Y ALGORITMO
    1) Cambio de modelo: ciclo ⇔ conjunto de casillas «adentro».
       Un ciclo simple de la cuadrícula encierra un conjunto I de casillas
       (el resto, junto con el exterior de la cuadrícula, está «afuera»), y
       las calles del ciclo son EXACTAMENTE los lados entre una casilla de
       adentro y una de afuera (o el borde exterior). Recíprocamente, un
       conjunto I es el interior de un ciclo simple ⇔
         (a) I no es vacío y es 4-conexo;
         (b) el afuera (casillas fuera de I + exterior) es 4-conexo, o sea,
             I no tiene «huecos»;
         (c) no hay un «tablero de ajedrez» 2×2 (dos casillas de adentro
             que sólo se tocan en diagonal): ahí la frontera pasaría dos
             veces por la misma esquina, cosa prohibida.
       (Sin (c), la frontera de I es unión disjunta de ciclos; con (a) y
       (b) es uno solo, porque #ciclos de frontera = #componentes de I +
       #componentes del afuera − 1.)
       Con este modelo, el número de una casilla = cuántos de sus 4 vecinos
       (contando el exterior) tienen distinto color que ella.
    2) DP de perfil roto (broken profile / «plug DP») con conectividad:
       se colorean las casillas en orden fila por fila. El estado guarda la
       «frontera»: la última casilla coloreada de cada columna, con
         - su color (adentro/afuera),
         - una etiqueta de componente conexa (normalizada; la etiqueta 0
           significa «afuera conectado al exterior»),
         - cuántos de sus lados distintos lleva contados (sólo si tiene
           número), para verificarlo cuando se completen sus 4 vecinos;
       más el color de la casilla diagonal superior-izquierda (para la
       regla (c)) y una bandera «el adentro ya se cerró».
       Al colorear la casilla (f, c):
         - se suman los lados distintos con arriba/izquierda/exterior; la
           casilla de arriba queda completa (ya tiene sus 4 vecinos) y se
           verifica su número; en la última fila la de la izquierda también;
         - se unen etiquetas con arriba e izquierda si son del mismo color;
           una casilla de afuera en el borde se une al exterior (etiqueta 0);
         - la casilla de arriba sale de la frontera: si su etiqueta ya no
           aparece en ella, esa componente se cerró para siempre. Si era de
           afuera y no tocaba el exterior → es un hueco → estado inválido.
           Si era de adentro → el adentro está terminado: no puede haber
           otra casilla de adentro ni en la frontera ni después.
       Al final se acepta si el adentro existe y es una sola componente.
       Los estados se guardan en un diccionario (se fusionan los iguales),
       así que el número de estados está acotado por las combinaciones de
       frontera, no por los ~2^25 coloreos.
    Interpretación: se exige un recorrido NO vacío (el carro debe salir y
    volver). Con casillas sólo «0» y «.» cerca, un ciclo puede no existir
    y se responde NO; el enunciado no aclara si la «ruta vacía» valdría.

MACROALGORITMO
    1. Leer R, C y la cuadrícula (dígito o None por «.»).
    2. Estado inicial: frontera de C casillas «exteriores» (afuera, etiqueta
       0), sin cierre.
    3. Para cada casilla en orden fila por fila y cada estado, probar los dos
       colores:
       a. regla del tablero de ajedrez con diagonal/arriba/izquierda;
       b. contar lados distintos y verificar los números que se completan
          (y podar si una cuenta parcial ya supera su número);
       c. unir componentes y detectar componentes que se cierran;
       d. normalizar etiquetas y guardar el nuevo estado.
    4. Aceptar si algún estado final tiene exactamente una componente de
       adentro (o el adentro cerrado y ninguna casilla de adentro abierta).
    5. Imprimir YES/NO.

COMPLEJIDAD
    O(R·C·#estados·C). Con C ≤ 5 hay muy pocos estados de frontera (95 como
    máximo en el 5×5 todo «.», que es el caso con menos poda). 500 casos
    5×5 aleatorios: ~2 s en total (~4 ms por caso). Memoria O(#estados).

VERIFICACIÓN
    - Ejemplo del enunciado: OK (python probar.py "Colombia 2018/G")
    - Fuerza bruta: OK contra la enumeración por DFS de TODOS los ciclos
      simples del grafo de esquinas, verificando directamente cuántos lados
      de cada casilla usa el ciclo (modelo independiente del de
      adentro/afuera):
        * 1 200 tableros aleatorios de hasta 12 casillas (mitad SÍ, mitad NO);
        * 1 200 tableros de hasta 16 casillas con pistas tomadas de un
          poliominó aleatorio (sesgados a SÍ);
        * 60 tableros 4×5 y 5×5 (27 NO, que obligan a la fuerza bruta a
          recorrer todos los ciclos).
"""
import sys

AFUERA, ADENTRO = 0, 1
EXT = 0   # etiqueta reservada: componente de afuera conectada al exterior


def normalizar(etiquetas):
    """Renombra las etiquetas por orden de aparición (EXT se queda en 0)."""
    mapa = {EXT: EXT}
    nuevas = []
    for e in etiquetas:
        if e not in mapa:
            mapa[e] = len(mapa)
        nuevas.append(mapa[e])
    return tuple(nuevas)


def resolver(R, C, grid):
    # Estado: (colores, etiquetas, cuentas, color_diagonal, cerrado)
    # La «fila −1» es el exterior: afuera, etiqueta EXT, sin número.
    inicial = ((AFUERA,) * C, (EXT,) * C, (0,) * C, AFUERA, False)
    estados = {inicial}
    for f in range(R):
        for c in range(C):
            num = grid[f][c]
            num_arriba = grid[f - 1][c] if f > 0 else None
            num_izq = grid[f][c - 1] if c > 0 else None
            borde = f == 0 or c == 0 or f == R - 1 or c == C - 1
            nuevos = set()
            for (cols, etqs, cnts, diag, cerrado) in estados:
                col_ar, etq_ar, cnt_ar = cols[c], etqs[c], cnts[c]
                if c > 0:
                    col_iz, etq_iz, cnt_iz = cols[c - 1], etqs[c - 1], cnts[c - 1]
                else:
                    col_iz, etq_iz, cnt_iz = AFUERA, EXT, 0   # exterior
                    diag = AFUERA   # en la columna 0 la diagonal es exterior
                for x in (AFUERA, ADENTRO):
                    if x == ADENTRO and cerrado:
                        continue          # el único interior ya se cerró
                    # (c) tablero de ajedrez en la esquina superior-izquierda.
                    if diag == x and col_ar == col_iz and col_ar != x:
                        continue
                    # --- Conteo de lados distintos ---------------------
                    cuenta = (x != col_ar) + (x != col_iz)
                    if c == C - 1:
                        cuenta += (x != AFUERA)      # exterior derecho
                    if f == R - 1:
                        cuenta += (x != AFUERA)      # exterior inferior
                    if num is not None and cuenta > num:
                        continue
                    ok = True
                    # La casilla de arriba recibe su vecino de abajo: completa.
                    if num_arriba is not None and cnt_ar + (x != col_ar) != num_arriba:
                        ok = False
                    # La de la izquierda recibe su vecino derecho.
                    nueva_cnt_iz = cnt_iz + (x != col_iz)
                    if c > 0 and num_izq is not None:
                        if f == R - 1:
                            # En la última fila ya tenía abajo (exterior): completa.
                            if nueva_cnt_iz != num_izq:
                                ok = False
                        elif nueva_cnt_iz > num_izq:
                            ok = False
                    if not ok:
                        continue
                    if f == R - 1 and c == C - 1 and num is not None and cuenta != num:
                        continue
                    # --- Conectividad ----------------------------------
                    etq_lista = list(etqs)
                    nueva = max(etq_lista) + 1     # etiqueta fresca (≥ 1)
                    # Etiquetas a fusionar con la casilla nueva.
                    unir = set()
                    if x == col_ar:
                        unir.add(etq_ar)
                    if x == col_iz:
                        unir.add(etq_iz)
                    if x == AFUERA and borde:
                        unir.add(EXT)
                    # min(unir) = EXT (0) si el afuera toca el exterior; una
                    # casilla de adentro nunca tiene EXT en `unir`.
                    destino = min(unir) if unir else nueva
                    # Reemplazar en la frontera la casilla de arriba por la nueva.
                    cols_n = list(cols)
                    cnts_n = list(cnts)
                    cols_n[c] = x
                    etq_lista[c] = destino
                    cnts_n[c] = cuenta if num is not None else 0
                    if c > 0:
                        cnts_n[c - 1] = nueva_cnt_iz if num_izq is not None else 0
                    # Aplicar la fusión: toda etiqueta en `unir` (del mismo
                    # color que x) pasa a ser `destino`.
                    for j in range(C):
                        if j != c and cols_n[j] == x and etq_lista[j] in unir:
                            etq_lista[j] = destino
                    # ¿La componente de la casilla de arriba se cerró?
                    cerrado_n = cerrado
                    if f > 0 and x != col_ar:
                        # (si x == col_ar, la de arriba se fusionó con la
                        #  nueva y su componente sigue viva)
                        if etq_ar not in [etq_lista[j] for j in range(C) if cols_n[j] == col_ar]:
                            if col_ar == AFUERA:
                                if etq_ar != EXT:
                                    continue   # hueco: afuera encerrado
                            else:
                                # El interior terminó: no debe quedar otra
                                # casilla de adentro en la frontera.
                                if ADENTRO in cols_n:
                                    continue
                                cerrado_n = True
                    estado = (tuple(cols_n), normalizar(etq_lista),
                              tuple(cnts_n), col_ar, cerrado_n)
                    nuevos.add(estado)
            estados = nuevos
            if not estados:
                return False
    # Estados finales: la última fila es la frontera.
    for (cols, etqs, cnts, diag, cerrado) in estados:
        interiores = {etqs[j] for j in range(C) if cols[j] == ADENTRO}
        if cerrado and not interiores:
            return True
        if not cerrado and len(interiores) == 1:
            return True
    return False


def main():
    datos = sys.stdin.read().split()
    pos = 0
    salida = []
    while pos + 1 < len(datos):
        R, C = int(datos[pos]), int(datos[pos + 1])
        pos += 2
        if R == 0 and C == 0:
            break
        grid = []
        for _ in range(R):
            fila = datos[pos]
            pos += 1
            grid.append([None if ch == "." else int(ch) for ch in fila])
        salida.append("YES" if resolver(R, C, grid) else "NO")
    sys.stdout.write("\n".join(salida) + ("\n" if salida else ""))


if __name__ == "__main__":
    main()
