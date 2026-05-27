#!/usr/bin/env python3
"""
ejercicio3.py
Detector de Recursión por la Izquierda en GIC

Laboratorio 4 - Resolver la Ambigüedad y/o Recursión en Python

Tipos de recursión por la izquierda:
  - Directa  : A → A α          (A aparece como primer símbolo de alguna producción)
  - Indirecta: A → B ... y B →* A β  (ciclo en el grafo de "primer símbolo")
"""

from collections import defaultdict, deque


# ─── Lectura de gramática ─────────────────────────────────────────────────────

def leer_gramatica():
    gramatica = {}
    orden = []
    print("Ingrese la gramática (formato: A -> alfa | beta)")
    print("Deje una línea vacía para terminar.\n")
    while True:
        try:
            linea = input("  ").strip()
        except EOFError:
            break
        if not linea:
            break
        if '->' not in linea:
            continue
        izq, der = linea.split('->', 1)
        nt = izq.strip()
        if not nt:
            continue
        if nt not in gramatica:
            gramatica[nt] = []
            orden.append(nt)
        for alt in der.split('|'):
            simbolos = alt.strip().split()
            if simbolos:
                gramatica[nt].append(simbolos)
    return gramatica, orden


# ─── Construcción del grafo de "primer símbolo" ──────────────────────────────

def construir_grafo_primer_simbolo(gramatica, nts):
    """
    Crea un grafo donde existe arista A → B si A tiene alguna producción
    cuyo primer símbolo es B (un no-terminal).

    Esto permite detectar recursión izquierda indirecta buscando ciclos.
    """
    grafo = defaultdict(set)
    for nt in nts:
        for prod in gramatica.get(nt, []):
            if prod and prod[0] in nts:
                grafo[nt].add(prod[0])
    return grafo


def alcanzables_desde(grafo, origen):
    """BFS: devuelve todos los nodos alcanzables desde 'origen' (sin incluirlo)."""
    visitados = set()
    cola = deque(grafo[origen])
    while cola:
        nodo = cola.popleft()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        cola.extend(grafo[nodo] - visitados)
    return visitados


# ─── Detección ────────────────────────────────────────────────────────────────

def detectar_recursion_directa(gramatica, nts):
    """Devuelve lista de (NT, produccion) con recursión directa."""
    directa = []
    for nt in nts:
        for prod in gramatica.get(nt, []):
            if prod and prod[0] == nt:
                directa.append((nt, prod))
    return directa


def detectar_recursion_indirecta(gramatica, nts, grafo, directos_set):
    """
    Devuelve lista de (NT, camino) con recursión izquierda indirecta.
    Solo informa NTs que NO tienen recursión directa (para no duplicar).
    """
    indirecta = []
    for nt in nts:
        if nt in directos_set:
            continue
        alcanzables = alcanzables_desde(grafo, nt)
        if nt in alcanzables:
            # Reconstruir el camino del ciclo
            camino = reconstruir_camino(grafo, nt, nt)
            indirecta.append((nt, camino))
    return indirecta


def reconstruir_camino(grafo, origen, destino):
    """BFS para encontrar el camino más corto de origen de vuelta a destino."""
    cola = deque([[origen]])
    visitados = {origen}
    while cola:
        camino = cola.popleft()
        ultimo = camino[-1]
        for vecino in grafo[ultimo]:
            nuevo_camino = camino + [vecino]
            if vecino == destino:
                return nuevo_camino
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(nuevo_camino)
    return [origen, destino]


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  EJERCICIO 3: Detector de Recursión por la Izquierda")
    print("=" * 62 + "\n")

    gramatica, orden = leer_gramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    nts = set(gramatica.keys())
    inicio = orden[0]

    print(f"\n  Símbolo inicial : {inicio}")
    print("  Producciones:")
    for nt in orden:
        for prod in gramatica[nt]:
            print(f"    {nt} → {' '.join(prod)}")

    grafo = construir_grafo_primer_simbolo(gramatica, nts)

    print("\n── Análisis de Recursión por la Izquierda ──────────────────")

    # ── Recursión directa ──
    directa = detectar_recursion_directa(gramatica, nts)
    directos_set = {nt for nt, _ in directa}

    if directa:
        print("\n  [!] Recursión DIRECTA detectada:")
        for nt, prod in directa:
            print(f"      {nt} → {' '.join(prod)}")
    else:
        print("\n  [OK] Sin recursión directa.")

    # ── Recursión indirecta ──
    indirecta = detectar_recursion_indirecta(gramatica, nts, grafo, directos_set)

    if indirecta:
        print("\n  [!] Recursión INDIRECTA detectada:")
        for nt, camino in indirecta:
            print(f"      Ciclo: {' → '.join(camino)}")
    else:
        print("  [OK] Sin recursión indirecta.")

    # ── Resumen ──
    tiene_recursion = bool(directa or indirecta)
    todos_recursivos = sorted(directos_set | {nt for nt, _ in indirecta})

    print("\n── Resumen ─────────────────────────────────────────────────")
    if tiene_recursion:
        print(f"  NTs con recursión izq.: {todos_recursivos}")
        print("\n  Tipo de recursión:")
        for nt in todos_recursivos:
            tipos = []
            if nt in directos_set:
                tipos.append("DIRECTA")
            if nt in {n for n, _ in indirecta}:
                tipos.append("INDIRECTA")
            print(f"    {nt} : {', '.join(tipos)}")
    else:
        print("  La gramática NO tiene recursión por la izquierda.")

    print("\n" + "=" * 62)
    print(f"  RESULTADO: {'TIENE recursión por la izquierda' if tiene_recursion else 'SIN recursión por la izquierda'}")
    print("=" * 62)


if __name__ == "__main__":
    main()
