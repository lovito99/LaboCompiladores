#!/usr/bin/env python3
"""
ejercicio1.py
Cálculo del conjunto Primero/First para Gramáticas Libres de Contexto (GLC)

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
       - Si eps ∈ Primero(Y1) ... Primero(Yk), agregar eps a Primero(X)
    """
    # Si ya fue calculado, retornar
    if simbolo in tablaPrimeros:
        return tablaPrimeros[simbolo]

    # Si es terminal, Primero(terminal) = {terminal}
    if esTerminal(simbolo, noTerminales):
        tablaPrimeros[simbolo] = {simbolo}
        return {simbolo}

    # Evitar ciclos en recursión
    if simbolo in enProceso:
        return set()
    enProceso.add(simbolo)

    resultado = set()

    for produccion in gramatica.get(simbolo, []):
        # Si la producción es eps
        if produccion == ['eps'] or produccion == ['ε']:
            resultado.add('eps')
            continue

        # Recorrer símbolos de la producción
        todosConEps = True
        for sim in produccion:
            primeroDeSim = calcularPrimero(gramatica, sim, noTerminales,
                                          tablaPrimeros, enProceso)
            # Agregar todo excepto eps
            resultado.update(primeroDeSim - {'eps'})

            # Si eps no está en Primero(sim), detenerse
            if 'eps' not in primeroDeSim:
                todosConEps = False
                break

        # Si todos los símbolos tienen eps, agregar eps
        if todosConEps:
            resultado.add('eps')

    tablaPrimeros[simbolo] = resultado
    enProceso.discard(simbolo)
    return resultado


def calcularPrimeroDeCadena(cadena, noTerminales, tablaPrimeros):
    """
    Calcula Primero de una cadena de símbolos (α = X1 X2 ... Xn).
    Se usa para producciones completas.
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
    de la gramática usando un enfoque iterativo de punto fijo.
    """
    noTerminales = obtenerNoTerminales(gramatica)
    tablaPrimeros = {}

    # Inicializar terminales
    terminales = obtenerTerminales(gramatica)
    for t in terminales:
        tablaPrimeros[t] = {t}

    # Inicializar no terminales con conjunto vacío
    for nt in orden:
        tablaPrimeros[nt] = set()

    # Iterar hasta punto fijo
    cambio = True
    while cambio:
        cambio = False
        for nt in orden:
            anterior = set(tablaPrimeros.get(nt, set()))
            # Borrar para recalcular con datos actualizados
            del tablaPrimeros[nt]
            enProceso = set()
            calcularPrimero(gramatica, nt, noTerminales,
                           tablaPrimeros, enProceso)
            if tablaPrimeros.get(nt, set()) != anterior:
                cambio = True

    return tablaPrimeros


# ─── Mostrar resultados ───────────────────────────────────────────────────

def mostrarPrimeros(tablaPrimeros, orden):
    """Muestra los conjuntos Primero/First de forma formateada."""
    print("\n── Conjuntos Primero/First ──────────────────────────────────\n")
    for nt in orden:
        elementos = tablaPrimeros.get(nt, set())
        elementosOrdenados = sorted(elementos, key=lambda x: (x == 'eps', x))
        cadena = ", ".join(elementosOrdenados)
        print(f"  Primero({nt}) = {{ {cadena} }}")


def mostrarPrimerosProducciones(gramatica, orden, noTerminales, tablaPrimeros):
    """Muestra Primero de cada producción individual."""
    print("\n── Primero de cada producción ───────────────────────────────\n")
    for nt in orden:
        for produccion in gramatica[nt]:
            cadenaProduccion = ' '.join(produccion)
            primeroProd = calcularPrimeroDeCadena(produccion, noTerminales,
                                                 tablaPrimeros)
            elementosOrd = sorted(primeroProd, key=lambda x: (x == 'eps', x))
            cadenaElementos = ", ".join(elementosOrd)
            print(f"  Primero({nt} → {cadenaProduccion}) = {{ {cadenaElementos} }}")


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  EJERCICIO 1: Cálculo del Conjunto Primero/First")
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

    # Calcular Primero/First
    tablaPrimeros = calcularTodosPrimeros(gramatica, orden)

    # Mostrar resultados
    mostrarPrimeros(tablaPrimeros, orden)
    mostrarPrimerosProducciones(gramatica, orden, noTerminales, tablaPrimeros)

    print("\n" + "=" * 60)
    print("  Cálculo de Primero/First completado exitosamente")
    print("=" * 60)


if __name__ == "__main__":
    main()
