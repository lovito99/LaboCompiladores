#!/usr/bin/env python3
"""
ejercicio2.py
Eliminación de Ambigüedad en GIC mediante jerarquía de precedencia

Laboratorio 4 - Resolver la Ambigüedad y/o Recursión en Python

Algoritmo:
  1. Detectar producciones ambiguas de la forma A → A op A.
  2. Pedir al usuario que ordene los operadores por precedencia
     (de menor a mayor, separados por espacio; mismo nivel con coma).
  3. Reescribir la gramática con una cadena de no-terminales:
       N0 → N0 op1 N1 | N1          (op de menor precedencia, asoc. izq.)
       N1 → N1 op2 N2 | N2
       ...
       Nk → base cases              (paréntesis, identificadores, etc.)
"""

# ─── Lectura de gramática ─────────────────────────────────────────────────

def leerGramatica():
    gramatica = {}
    orden = []
    print("Ingrese la gramática ambigua (formato: A -> alfa | beta)")
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


# ─── Detección ──────────────────────────────────────────────────────────────

def extraerOperadoresBinarios(gramatica, nt):
    nts = set(gramatica.keys())
    ops = []
    bases = []
    for prod in gramatica.get(nt, []):
        if (len(prod) == 3
                and prod[0] == nt
                and prod[1] not in nts
                and prod[2] == nt):
            ops.append(prod[1])
        else:
            bases.append(prod)
    return ops, bases


def detectarNtAmbiguo(gramatica, orden):
    for nt in orden:
        ops, _ = extraerOperadoresBinarios(gramatica, nt)
        if ops:
            return nt
    return None


# ─── Reescritura ─────────────────────────────────────────────────────────────

def reescribirConPrecedencia(ntAmbiguo, ops, bases, gruposPrecedencia, nombreBase):
    nueva = {}
    nombres = []

    for i, grupo in enumerate(gruposPrecedencia):
        nivel = f"{ntAmbiguo}{i}" if i > 0 else ntAmbiguo
        siguiente = (f"{ntAmbiguo}{i+1}" if i + 1 < len(gruposPrecedencia)
                     else nombreBase)
        nombres.append(nivel)
        prods = []
        for op in grupo:
            prods.append([nivel, op, siguiente])
        prods.append([siguiente])
        nueva[nivel] = prods

    baseProds = []
    for prod in bases:
        baseProds.append([ntAmbiguo if s == ntAmbiguo else s for s in prod])
    nueva[nombreBase] = baseProds

    return nueva, nombres


def imprimirGramatica(gramatica, orden):
    for nt in orden:
        for prod in gramatica.get(nt, []):
            print(f"  {nt} → {' '.join(prod)}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  EJERCICIO 2: Eliminación de Ambigüedad en GIC")
    print("=" * 62 + "\n")

    gramatica, orden = leerGramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    inicio = orden[0]
    print(f"\n  Símbolo inicial : {inicio}")
    print("  Gramática ingresada:")
    imprimirGramatica(gramatica, orden)

    ntAmb = detectarNtAmbiguo(gramatica, orden)
    if ntAmb is None:
        print("\n[OK] No se detectaron patrones A → A op A. La gramática podría no ser ambigua.")
        return

    ops, bases = extraerOperadoresBinarios(gramatica, ntAmb)
    print(f"\n[!] NT ambiguo detectado: {ntAmb}")
    print(f"    Operadores encontrados: {ops}")
    print(f"    Producciones base      : {['  '.join(b) for b in bases]}")

    print(f"\n  Operadores a ordenar: {ops}")
    print("  Ingrese los grupos de precedencia de MENOR a MAYOR.")
    print("  Separe operadores del mismo nivel con coma, grupos distintos con Enter.")
    print("  (Ejemplo: para + y -, luego * y /  →  escriba  '+ -'  luego  '* /')")
    print("  Línea vacía para terminar.\n")

    grupos = []
    usados = set()
    while True:
        try:
            linea = input(f"  Nivel {len(grupos)+1}: ").strip()
        except EOFError:
            break
        if not linea:
            break
        grupo = linea.replace(',', ' ').split()
        validos = [op for op in grupo if op in ops and op not in usados]
        if not validos:
            print("  [!] Ningún operador válido en esa línea.")
            continue
        grupos.append(validos)
        usados.update(validos)

    restantes = [op for op in ops if op not in usados]
    if restantes:
        grupos.append(restantes)

    if not grupos:
        print("[!] No se ingresaron grupos de precedencia."); return

    nombreBase = f"{ntAmb}_base"

    nuevaGram, niveles = reescribirConPrecedencia(
        ntAmb, ops, bases, grupos, nombreBase
    )

    ordenFinal = []
    for nt in niveles:
        if nt not in ordenFinal:
            ordenFinal.append(nt)
    if nombreBase not in ordenFinal:
        ordenFinal.append(nombreBase)
    for nt in orden:
        if nt != ntAmb and nt not in ordenFinal:
            ordenFinal.append(nt)
            nuevaGram[nt] = gramatica[nt]

    print("\n── Gramática NO AMBIGUA resultante ─────────────────────────")
    imprimirGramatica(nuevaGram, ordenFinal)

    print("\n  Jerarquía de precedencia aplicada (menor → mayor):")
    for i, g in enumerate(grupos):
        print(f"    Nivel {i+1}: {g}")

    print("\n" + "=" * 62)
    print("  La gramática reescrita es asociativa por la izquierda")
    print("  y respeta la precedencia indicada.")
    print("=" * 62)


if __name__ == "__main__":
    main()
