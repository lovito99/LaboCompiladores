#!/usr/bin/env python3
"""
ejercicio2.py
Cálculo del conjunto Siguiente/Follow para Gramáticas Libres de Contexto (GLC)

Laboratorio 5 - Conjuntos Primeros y Siguientes
Curso: IF454AIN - Compiladores
Profesor: Victor Dario Sosa Jauregui
UNSAAC - Escuela Profesional de Ingeniería Informática y de Sistemas
"""


# ─── Lectura de la gramática ────────────────────────────────────────────────

def leerGramatica():
    """Lee una gramática libre de contexto desde la entrada estándar."""
    gramatica = {}
    orden = []
    print("Ingrese la gramática (formato: A -> alfa | beta)")
    print("Símbolo vacío (ε) se representa como 'eps'.")
    print("Deje una línea vacía para terminar.\n")
    while True:
        try:
            linea = input("  ").strip()
        except EOFError:
            break
        if not linea:
            break
        if '->' not in linea:
            print("  [!] Use el formato: A -> alfa | beta")
            continue
        izq, der = linea.split('->', 1)
        nt = izq.strip()
        if not nt:
            continue
        if nt not in gramatica:
            gramatica[nt] = []
            orden.append(nt)
        gramatica[nt] += [alt.split() for alt in der.split('|') if alt.strip()]
    return gramatica, orden


# ─── Obtener terminales y no terminales ─────────────────────────────────────

def obtenerNoTerminales(gramatica):
    """Retorna el conjunto de no terminales de la gramática."""
    return set(gramatica.keys())


def obtenerTerminales(gramatica):
    """Retorna el conjunto de terminales de la gramática."""
    noTerminales = obtenerNoTerminales(gramatica)
    terminales = set()
    for producciones in gramatica.values():
        for produccion in producciones:
            for simbolo in produccion:
                if simbolo not in noTerminales and simbolo not in ('eps', 'ε'):
                    terminales.add(simbolo)
    return terminales


def esTerminal(simbolo, noTerminales):
    """Verifica si un símbolo es terminal."""
    return simbolo not in noTerminales and simbolo not in ('eps', 'ε')


# ─── Algoritmo Primero/First ───────────────────────────────────────────────

def calcularPrimero(gramatica, simbolo, noTerminales, tablaPrimeros, enProceso):
    """
    Calcula el conjunto Primero/First de un símbolo dado.

    Reglas:
    1. Si X es terminal → Primero(X) = {X}
    2. Si X → eps  → agregar eps a Primero(X)
    3. Si X → Y1 Y2 ... Yk:
       - Agregar Primero(Y1) - {eps} a Primero(X)
       - Si eps ∈ Primero(Y1), agregar Primero(Y2) - {eps}
       - Si eps ∈ Primero(Y1) ... Primero(Yk), agregar eps
    """
    if simbolo in tablaPrimeros:
        return tablaPrimeros[simbolo]

    if esTerminal(simbolo, noTerminales):
        tablaPrimeros[simbolo] = {simbolo}
        return {simbolo}

    if simbolo in enProceso:
        return set()
    enProceso.add(simbolo)

    resultado = set()

    for produccion in gramatica.get(simbolo, []):
        if produccion == ['eps'] or produccion == ['ε']:
            resultado.add('eps')
            continue

        todosConEps = True
        for sim in produccion:
            primeroDeSim = calcularPrimero(gramatica, sim, noTerminales,
                                          tablaPrimeros, enProceso)
            resultado.update(primeroDeSim - {'eps'})
            if 'eps' not in primeroDeSim:
                todosConEps = False
                break

        if todosConEps:
            resultado.add('eps')

    tablaPrimeros[simbolo] = resultado
    enProceso.discard(simbolo)
    return resultado


def calcularPrimeroDeCadena(cadena, noTerminales, tablaPrimeros):
    """
    Calcula Primero de una cadena de símbolos (α = X1 X2 ... Xn).
    """
    resultado = set()

    if not cadena:
        resultado.add('eps')
        return resultado

    todosConEps = True
    for simbolo in cadena:
        if simbolo in ('eps', 'ε'):
            continue
        primeroDelSimbolo = tablaPrimeros.get(simbolo, set())
        resultado.update(primeroDelSimbolo - {'eps'})
        if 'eps' not in primeroDelSimbolo:
            todosConEps = False
            break

    if todosConEps:
        resultado.add('eps')

    return resultado


def calcularTodosPrimeros(gramatica, orden):
    """
    Calcula los conjuntos Primero/First para todos los símbolos
    de la gramática.
    """
    noTerminales = obtenerNoTerminales(gramatica)
    tablaPrimeros = {}

    terminales = obtenerTerminales(gramatica)
    for t in terminales:
        tablaPrimeros[t] = {t}

    # Inicializar no terminales con conjunto vacío
    for nt in orden:
        tablaPrimeros[nt] = set()

    cambio = True
    while cambio:
        cambio = False
        for nt in orden:
            anterior = set(tablaPrimeros.get(nt, set()))
            del tablaPrimeros[nt]
            enProceso = set()
            calcularPrimero(gramatica, nt, noTerminales,
                           tablaPrimeros, enProceso)
            if tablaPrimeros.get(nt, set()) != anterior:
                cambio = True

    return tablaPrimeros


# ─── Algoritmo Siguiente/Follow ───────────────────────────────────────────

def calcularTodosSiguientes(gramatica, orden, tablaPrimeros):
    """
    Calcula los conjuntos Siguiente/Follow para todos los no terminales
    de la gramática.

    Reglas:
    1. Agregar $ a Siguiente(S), donde S es el símbolo inicial.
    2. Si hay una producción A → αBβ:
       - Agregar Primero(β) - {eps} a Siguiente(B)
    3. Si hay una producción A → αB, o A → αBβ donde eps ∈ Primero(β):
       - Agregar Siguiente(A) a Siguiente(B)
    """
    noTerminales = obtenerNoTerminales(gramatica)
    inicio = orden[0]

    # Inicializar tabla de siguientes
    tablaSiguientes = {}
    for nt in orden:
        tablaSiguientes[nt] = set()

    # Regla 1: Agregar $ al símbolo inicial
    tablaSiguientes[inicio].add('$')

    # Iterar hasta punto fijo
    cambio = True
    while cambio:
        cambio = False
        for ntIzq in orden:
            for produccion in gramatica[ntIzq]:
                for i, simbolo in enumerate(produccion):
                    # Solo procesar no terminales
                    if simbolo not in noTerminales:
                        continue
                    if simbolo in ('eps', 'ε'):
                        continue

                    # β = lo que sigue después de simbolo
                    beta = produccion[i + 1:]

                    # Filtrar eps de beta
                    betaFiltrada = [s for s in beta if s not in ('eps', 'ε')]

                    if betaFiltrada:
                        # Regla 2: Agregar Primero(β) - {eps} a Siguiente(B)
                        primeroBeta = calcularPrimeroDeCadena(
                            betaFiltrada, noTerminales, tablaPrimeros)
                        nuevos = primeroBeta - {'eps'} - tablaSiguientes[simbolo]
                        if nuevos:
                            tablaSiguientes[simbolo].update(nuevos)
                            cambio = True

                        # Regla 3: Si eps ∈ Primero(β), agregar Siguiente(A)
                        if 'eps' in primeroBeta:
                            nuevos = tablaSiguientes[ntIzq] - tablaSiguientes[simbolo]
                            if nuevos:
                                tablaSiguientes[simbolo].update(nuevos)
                                cambio = True
                    else:
                        # Regla 3: A → αB (B está al final)
                        nuevos = tablaSiguientes[ntIzq] - tablaSiguientes[simbolo]
                        if nuevos:
                            tablaSiguientes[simbolo].update(nuevos)
                            cambio = True

    return tablaSiguientes


# ─── Mostrar resultados ───────────────────────────────────────────────────

def mostrarPrimeros(tablaPrimeros, orden):
    """Muestra los conjuntos Primero/First."""
    print("\n── Conjuntos Primero/First ──────────────────────────────────\n")
    for nt in orden:
        elementos = tablaPrimeros.get(nt, set())
        elementosOrdenados = sorted(elementos, key=lambda x: (x == 'eps', x))
        cadena = ", ".join(elementosOrdenados)
        print(f"  Primero({nt}) = {{ {cadena} }}")


def mostrarSiguientes(tablaSiguientes, orden):
    """Muestra los conjuntos Siguiente/Follow."""
    print("\n── Conjuntos Siguiente/Follow ───────────────────────────────\n")
    for nt in orden:
        elementos = tablaSiguientes.get(nt, set())
        elementosOrdenados = sorted(elementos, key=lambda x: (x == '$', x))
        cadena = ", ".join(elementosOrdenados)
        print(f"  Siguiente({nt}) = {{ {cadena} }}")


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  EJERCICIO 2: Cálculo de Primero/First y Siguiente/Follow")
    print("=" * 60 + "\n")

    gramatica, orden = leerGramatica()
    if not gramatica:
        print("[!] Gramática vacía.")
        return

    noTerminales = obtenerNoTerminales(gramatica)
    inicio = orden[0]

    print(f"\n  Símbolo inicial : {inicio}")
    print("  Producciones:")
    for nt in orden:
        for p in gramatica[nt]:
            print(f"    {nt} → {' '.join(p)}")

    # Paso 1: Calcular Primero/First
    tablaPrimeros = calcularTodosPrimeros(gramatica, orden)
    mostrarPrimeros(tablaPrimeros, orden)

    # Paso 2: Calcular Siguiente/Follow
    tablaSiguientes = calcularTodosSiguientes(gramatica, orden, tablaPrimeros)
    mostrarSiguientes(tablaSiguientes, orden)

    print("\n" + "=" * 60)
    print("  Cálculo de Primero/First y Siguiente/Follow completado")
    print("=" * 60)


if __name__ == "__main__":
    main()
