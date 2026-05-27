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

def leerGramatica():
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

def construirGrafoPrimerSimbolo(gramatica, nts):
    grafo = defaultdict(set)
    for nt in nts:
        for prod in gramatica.get(nt, []):
            if prod and prod[0] in nts:
                grafo[nt].add(prod[0])
    return grafo


def alcanzablesDesde(grafo, origen):
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

def detectarRecursionDirecta(gramatica, nts):
    directa = []
    for nt in nts:
        for prod in gramatica.get(nt, []):
            if prod and prod[0] == nt:
                directa.append((nt, prod))
    return directa


def detectarRecursionIndirecta(gramatica, nts, grafo, directosSet):
    indirecta = []
    for nt in nts:
        if nt in directosSet:
            continue
        alcanzables = alcanzablesDesde(grafo, nt)
        if nt in alcanzables:
            camino = reconstruirCamino(grafo, nt, nt)
            indirecta.append((nt, camino))
    return indirecta


def reconstruirCamino(grafo, origen, destino):
    cola = deque([[origen]])
    visitados = {origen}
    while cola:
        camino = cola.popleft()
        ultimo = camino[-1]
        for vecino in grafo[ultimo]:
            nuevoCamino = camino + [vecino]
            if vecino == destino:
                return nuevoCamino
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(nuevoCamino)
    return [origen, destino]


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  EJERCICIO 3: Detector de Recursión por la Izquierda")
    print("=" * 62 + "\n")

    gramatica, orden = leerGramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    nts = set(gramatica.keys())
    inicio = orden[0]

    print(f"\n  Símbolo inicial : {inicio}")
    print("  Producciones:")
    for nt in orden:
        for prod in gramatica[nt]:
            print(f"    {nt} → {' '.join(prod)}")

    grafo = construirGrafoPrimerSimbolo(gramatica, nts)

    print("\n── Análisis de Recursión por la Izquierda ──────────────────")

    directa = detectarRecursionDirecta(gramatica, nts)
    directosSet = {nt for nt, _ in directa}

    if directa:
        print("\n  [!] Recursión DIRECTA detectada:")
        for nt, prod in directa:
            print(f"      {nt} → {' '.join(prod)}")
    else:
        print("\n  [OK] Sin recursión directa.")

    indirecta = detectarRecursionIndirecta(gramatica, nts, grafo, directosSet)

    if indirecta:
        print("\n  [!] Recursión INDIRECTA detectada:")
        for nt, camino in indirecta:
            print(f"      Ciclo: {' → '.join(camino)}")
    else:
        print("  [OK] Sin recursión indirecta.")

    tieneRecursion = bool(directa or indirecta)
    todosRecursivos = sorted(directosSet | {nt for nt, _ in indirecta})

    print("\n── Resumen ─────────────────────────────────────────────────")
    if tieneRecursion:
        print(f"  NTs con recursión izq.: {todosRecursivos}")
        print("\n  Tipo de recursión:")
        for nt in todosRecursivos:
            tipos = []
            if nt in directosSet:
                tipos.append("DIRECTA")
            if nt in {n for n, _ in indirecta}:
                tipos.append("INDIRECTA")
            print(f"    {nt} : {', '.join(tipos)}")
    else:
        print("  La gramática NO tiene recursión por la izquierda.")

    print("\n" + "=" * 62)
    print(f"  RESULTADO: {'TIENE recursión por la izquierda' if tieneRecursion else 'SIN recursión por la izquierda'}")
    print("=" * 62)


if __name__ == "__main__":
    main()
