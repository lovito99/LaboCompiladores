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

def leer_gramatica():
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

def extraer_operadores_binarios(gramatica, nt):
    """
    Devuelve (ops, bases):
      ops  = lista de operadores encontrados en  A → A op A
      bases = lista de producciones no-operador  (A → ( A ), A → id, ...)
    """
    nts = set(gramatica.keys())
    ops = []
    bases = []
    for prod in gramatica.get(nt, []):
        # Patrón: A → A op A   (longitud 3, primero y último son el mismo NT)
        if (len(prod) == 3
                and prod[0] == nt
                and prod[1] not in nts
                and prod[2] == nt):
            ops.append(prod[1])
        else:
            bases.append(prod)
    return ops, bases


def detectar_nt_ambiguo(gramatica, orden):
    """Devuelve el primer NT que tiene producciones A → A op A."""
    for nt in orden:
        ops, _ = extraer_operadores_binarios(gramatica, nt)
        if ops:
            return nt
    return None


# ─── Reescritura ─────────────────────────────────────────────────────────────

def reescribir_con_precedencia(nt_ambiguo, ops, bases, grupos_precedencia, nombre_base):
    """
    Genera la gramática no ambigua con la cadena de no-terminales.

    grupos_precedencia: lista de listas, de MENOR a MAYOR precedencia.
    nombre_base: nombre del NT de mayor precedencia (para los casos base).
    """
    nueva = {}
    nombres = []

    # Un nivel por cada grupo de operadores
    for i, grupo in enumerate(grupos_precedencia):
        nivel = f"{nt_ambiguo}{i}" if i > 0 else nt_ambiguo
        siguiente = (f"{nt_ambiguo}{i+1}" if i + 1 < len(grupos_precedencia)
                     else nombre_base)
        nombres.append(nivel)
        prods = []
        for op in grupo:
            prods.append([nivel, op, siguiente])   # asociatividad izquierda
        prods.append([siguiente])                   # alternativa base
        nueva[nivel] = prods

    # Nivel base (paréntesis, identificadores, etc.)
    base_prods = []
    for prod in bases:
        # Reemplaza referencias al NT ambiguo original por el nivel 0
        base_prods.append([nt_ambiguo if s == nt_ambiguo else s for s in prod])
    nueva[nombre_base] = base_prods

    return nueva, nombres


def imprimir_gramatica(gramatica, orden):
    for nt in orden:
        for prod in gramatica.get(nt, []):
            print(f"  {nt} → {' '.join(prod)}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 62)
    print("  EJERCICIO 2: Eliminación de Ambigüedad en GIC")
    print("=" * 62 + "\n")

    gramatica, orden = leer_gramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    inicio = orden[0]
    print(f"\n  Símbolo inicial : {inicio}")
    print("  Gramática ingresada:")
    imprimir_gramatica(gramatica, orden)

    # ── Detectar NT ambiguo ──
    nt_amb = detectar_nt_ambiguo(gramatica, orden)
    if nt_amb is None:
        print("\n[OK] No se detectaron patrones A → A op A. La gramática podría no ser ambigua.")
        return

    ops, bases = extraer_operadores_binarios(gramatica, nt_amb)
    print(f"\n[!] NT ambiguo detectado: {nt_amb}")
    print(f"    Operadores encontrados: {ops}")
    print(f"    Producciones base      : {['  '.join(b) for b in bases]}")

    # ── Pedir precedencia al usuario ──
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

    # Si quedaron operadores sin asignar, van al último nivel
    restantes = [op for op in ops if op not in usados]
    if restantes:
        grupos.append(restantes)

    if not grupos:
        print("[!] No se ingresaron grupos de precedencia."); return

    # ── Generar NT base ──
    nombre_base = f"{nt_amb}_base"

    # ── Reescribir ──
    nueva_gram, niveles = reescribir_con_precedencia(
        nt_amb, ops, bases, grupos, nombre_base
    )

    # Conservar el resto de la gramática (NTs distintos al ambiguo)
    orden_final = []
    for nt in niveles:
        if nt not in orden_final:
            orden_final.append(nt)
    if nombre_base not in orden_final:
        orden_final.append(nombre_base)
    for nt in orden:
        if nt != nt_amb and nt not in orden_final:
            orden_final.append(nt)
            nueva_gram[nt] = gramatica[nt]

    # ── Mostrar resultado ──
    print("\n── Gramática NO AMBIGUA resultante ─────────────────────────")
    imprimir_gramatica(nueva_gram, orden_final)

    print("\n  Jerarquía de precedencia aplicada (menor → mayor):")
    for i, g in enumerate(grupos):
        print(f"    Nivel {i+1}: {g}")

    print("\n" + "=" * 62)
    print("  La gramática reescrita es asociativa por la izquierda")
    print("  y respeta la precedencia indicada.")
    print("=" * 62)


if __name__ == "__main__":
    main()
