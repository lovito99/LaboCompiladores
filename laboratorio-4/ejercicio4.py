#!/usr/bin/env python3
"""
ejercicio4.py
Eliminación de Recursión por la Izquierda en GIC

Laboratorio 4 - Resolver la Ambigüedad y/o Recursión en Python

Algoritmo estándar (Dragon Book):
  Dado los no-terminales A1, A2, ..., An (en orden):
  Para i = 1 hasta n:
    Para j = 1 hasta i-1:
      Reemplazar cada producción  Ai → Aj γ
      con                         Ai → δ1 γ | δ2 γ | ...
      donde Aj → δ1 | δ2 | ...
    Eliminar la recursión directa de Ai:
      Si Ai → Ai α1 | ... | Ai αk | β1 | ... | βm
      Reemplazar con:
        Ai  → β1 Ai' | β2 Ai' | ... | βm Ai'
        Ai' → α1 Ai' | α2 Ai' | ... | αk Ai' | ε
"""

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


# ─── Paso 1: sustitución de producciones Ai → Aj γ ──────────────────────────

def sustituir(gramatica, ai, aj):
    nuevas = []
    for prod in gramatica[ai]:
        if prod and prod[0] == aj:
            cola = prod[1:]
            for delta in gramatica[aj]:
                nuevas.append(delta + cola)
        else:
            nuevas.append(prod)
    gramatica[ai] = nuevas


# ─── Paso 2: eliminación de recursión directa ────────────────────────────────

def eliminarRecursionDirecta(gramatica, orden, ai):
    prods = gramatica[ai]
    recursivas = [p[1:] for p in prods if p and p[0] == ai]
    noRecursivas = [p for p in prods if not p or p[0] != ai]

    if not recursivas:
        return None

    aiPrima = f"{ai}'"
    while aiPrima in gramatica:
        aiPrima += "'"

    gramatica[ai] = [b + [aiPrima] for b in noRecursivas]
    gramatica[aiPrima] = [a + [aiPrima] for a in recursivas] + [['eps']]

    orden.append(aiPrima)
    return aiPrima


# ─── Algoritmo principal ─────────────────────────────────────────────────────

def eliminarTodaRecursion(gramatica, orden):
    n = len(orden)
    log = []

    for i in range(n):
        ai = orden[i]
        for j in range(i):
            aj = orden[j]
            antes = [list(p) for p in gramatica[ai]]
            sustituir(gramatica, ai, aj)
            despues = [list(p) for p in gramatica[ai]]
            if antes != despues:
                log.append(f"  Sustituyendo {aj} en {ai}:")
                for p in despues:
                    log.append(f"    {ai} → {' '.join(p)}")

        ntNuevo = eliminarRecursionDirecta(gramatica, orden, ai)
        if ntNuevo:
            log.append(f"  Recursión directa eliminada en {ai}  →  se crea {ntNuevo}")

    return log


# ─── Utilidades de impresión ─────────────────────────────────────────────────

def imprimirGramatica(gramatica, orden):
    for nt in orden:
        if nt in gramatica:
            for prod in gramatica[nt]:
                print(f"  {nt} → {' '.join(prod)}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  EJERCICIO 4: Eliminación de Recursión por la Izquierda")
    print("=" * 62 + "\n")

    gramatica, orden = leerGramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    print(f"\n  Símbolo inicial : {orden[0]}")
    print("  Gramática ORIGINAL:")
    imprimirGramatica(gramatica, orden)

    nts = set(gramatica.keys())
    tieneRecursion = any(
        any(p and p[0] == nt for p in prods)
        for nt, prods in gramatica.items()
    )

    if not tieneRecursion:
        from collections import defaultdict, deque
        grafo = defaultdict(set)
        for nt in nts:
            for prod in gramatica.get(nt, []):
                if prod and prod[0] in nts:
                    grafo[nt].add(prod[0])
        for nt in nts:
            visitados = set()
            cola = deque(grafo[nt])
            while cola:
                nodo = cola.popleft()
                if nodo == nt:
                    tieneRecursion = True
                    break
                if nodo not in visitados:
                    visitados.add(nodo)
                    cola.extend(grafo[nodo] - visitados)
            if tieneRecursion:
                break

    if not tieneRecursion:
        print("\n[OK] La gramática NO tiene recursión por la izquierda.")
        print("     No se requiere transformación.")
        return

    print("\n── Aplicando algoritmo de eliminación ──────────────────────")
    import copy
    gramaticaNueva = copy.deepcopy(gramatica)
    ordenNuevo = list(orden)

    log = eliminarTodaRecursion(gramaticaNueva, ordenNuevo)

    if log:
        print("\n  Pasos realizados:")
        for linea in log:
            print(linea)

    print("\n── Gramática RESULTANTE (sin recursión izquierda) ──────────")
    imprimirGramatica(gramaticaNueva, ordenNuevo)

    print("\n  Leyenda: 'eps' representa ε (cadena vacía)")
    print("\n" + "=" * 62)
    print("  Recursión por la izquierda eliminada exitosamente.")
    print("=" * 62)


if __name__ == "__main__":
    main()
