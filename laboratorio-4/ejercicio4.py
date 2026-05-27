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


# ─── Paso 1: sustitución de producciones Ai → Aj γ ──────────────────────────

def sustituir(gramatica, ai, aj):
    """
    Reemplaza todas las producciones de Ai que comienzan con Aj
    por las expansiones de Aj.
    Ejemplo: Ai → Aj γ  y  Aj → δ1 | δ2
             →  Ai → δ1 γ | δ2 γ
    """
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

def eliminar_recursion_directa(gramatica, orden, ai):
    """
    Elimina la recursión directa de Ai.
    Si Ai → Ai α | β  entonces se genera  Ai', y:
      Ai  → β Ai'
      Ai' → α Ai' | ε
    Devuelve el nombre del nuevo NT creado (o None si no había recursión).
    """
    prods = gramatica[ai]
    recursivas = [p[1:] for p in prods if p and p[0] == ai]   # los α
    no_recursivas = [p for p in prods if not p or p[0] != ai]  # los β

    if not recursivas:
        return None  # sin recursión directa, nada que hacer

    ai_prima = f"{ai}'"
    # Garantizar nombre único
    while ai_prima in gramatica:
        ai_prima += "'"

    # Ai  → β Ai'
    gramatica[ai] = [b + [ai_prima] for b in no_recursivas]

    # Ai' → α Ai' | ε
    gramatica[ai_prima] = [a + [ai_prima] for a in recursivas] + [['eps']]

    orden.append(ai_prima)
    return ai_prima


# ─── Algoritmo principal ─────────────────────────────────────────────────────

def eliminar_toda_recursion(gramatica, orden):
    """
    Aplica el algoritmo completo sobre todos los no-terminales originales.
    Modifica 'gramatica' y 'orden' en su lugar.
    """
    n = len(orden)  # solo iteramos sobre los NTs originales
    log = []        # registro de transformaciones

    for i in range(n):
        ai = orden[i]
        # Sustituir referencias a Aj (j < i)
        for j in range(i):
            aj = orden[j]
            antes = [list(p) for p in gramatica[ai]]
            sustituir(gramatica, ai, aj)
            despues = [list(p) for p in gramatica[ai]]
            if antes != despues:
                log.append(f"  Sustituyendo {aj} en {ai}:")
                for p in despues:
                    log.append(f"    {ai} → {' '.join(p)}")

        # Eliminar recursión directa
        nt_nuevo = eliminar_recursion_directa(gramatica, orden, ai)
        if nt_nuevo:
            log.append(f"  Recursión directa eliminada en {ai}  →  se crea {nt_nuevo}")

    return log


# ─── Utilidades de impresión ─────────────────────────────────────────────────

def imprimir_gramatica(gramatica, orden):
    for nt in orden:
        if nt in gramatica:
            for prod in gramatica[nt]:
                print(f"  {nt} → {' '.join(prod)}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  EJERCICIO 4: Eliminación de Recursión por la Izquierda")
    print("=" * 62 + "\n")

    gramatica, orden = leer_gramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    print(f"\n  Símbolo inicial : {orden[0]}")
    print("  Gramática ORIGINAL:")
    imprimir_gramatica(gramatica, orden)

    # Verificar si hay recursión
    nts = set(gramatica.keys())
    tiene_recursion = any(
        any(p and p[0] == nt for p in prods)
        for nt, prods in gramatica.items()
    )

    if not tiene_recursion:
        # Comprobar también indirecta (ciclos)
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
                    tiene_recursion = True
                    break
                if nodo not in visitados:
                    visitados.add(nodo)
                    cola.extend(grafo[nodo] - visitados)
            if tiene_recursion:
                break

    if not tiene_recursion:
        print("\n[OK] La gramática NO tiene recursión por la izquierda.")
        print("     No se requiere transformación.")
        return

    print("\n── Aplicando algoritmo de eliminación ──────────────────────")
    import copy
    gramatica_nueva = copy.deepcopy(gramatica)
    orden_nuevo = list(orden)

    log = eliminar_toda_recursion(gramatica_nueva, orden_nuevo)

    if log:
        print("\n  Pasos realizados:")
        for linea in log:
            print(linea)

    print("\n── Gramática RESULTANTE (sin recursión izquierda) ──────────")
    imprimir_gramatica(gramatica_nueva, orden_nuevo)

    print("\n  Leyenda: 'eps' representa ε (cadena vacía)")
    print("\n" + "=" * 62)
    print("  Recursión por la izquierda eliminada exitosamente.")
    print("=" * 62)


if __name__ == "__main__":
    main()
