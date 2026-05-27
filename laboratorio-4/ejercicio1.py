#!/usr/bin/env python3
"""
ejercicio1.py
Detector de Ambigüedad en Gramáticas Independientes del Contexto (GIC)

Laboratorio 4 - Resolver la Ambigüedad y/o Recursión en Python

Un gramatica es ambigua si existe alguna cadena que puede ser derivada
de dos o más árboles de análisis distintos (derivaciones izquierdas distintas).
"""

from itertools import product as iproduct


# ─── Lectura de la gramática ────────────────────────────────────────────────

def leer_gramatica():
    """Lee la gramática en formato: A -> alfa | beta  (línea vacía para terminar)."""
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
        for alt in der.split('|'):
            simbolos = alt.strip().split()
            if simbolos:
                gramatica[nt].append(simbolos)
    return gramatica, orden


# ─── Contar árboles de análisis ────────────────────────────────────────────

_IN_PROGRESS = object()   # centinela para detectar ciclos

def contar_arboles(gramatica, nts, simbolo, tokens, memo):
    """Cuenta cuántos árboles de análisis puede generar 'simbolo' para 'tokens'.
    Usa un centinela _IN_PROGRESS para cortar ciclos en gramáticas left-recursivas.
    """
    clave = (simbolo, tokens)
    valor = memo.get(clave)
    if valor is _IN_PROGRESS:
        return 0          # ciclo detectado → no cuenta
    if valor is not None:
        return valor

    if simbolo not in nts:                       # es terminal
        res = 1 if tokens == (simbolo,) else 0
        memo[clave] = res
        return res

    memo[clave] = _IN_PROGRESS   # marcar como "en cómputo"
    total = 0
    for prod in gramatica.get(simbolo, []):
        if prod == ['eps'] or prod == ['ε']:
            total += 1 if not tokens else 0
        else:
            total += _contar_prod(gramatica, nts, prod, tokens, memo)
    memo[clave] = total
    return total


def _contar_prod(gramatica, nts, prod, tokens, memo):
    """Cuenta formas de particionar 'tokens' entre los símbolos de 'prod'."""
    if not prod:
        return 1 if not tokens else 0
    if len(prod) == 1:
        return contar_arboles(gramatica, nts, prod[0], tokens, memo)
    total = 0
    for i in range(len(tokens) + 1):
        izq = contar_arboles(gramatica, nts, prod[0], tokens[:i], memo)
        if izq > 0:
            der = _contar_prod(gramatica, nts, prod[1:], tokens[i:], memo)
            total += izq * der
    return total


# ─── Detección de patrones ─────────────────────────────────────────────────

def detectar_patron_directo(gramatica):
    """
    Patrón clásico de ambigüedad: A → α A β A γ
    (el mismo NT aparece dos o más veces en una producción)
    """
    encontrados = []
    for nt, prods in gramatica.items():
        for prod in prods:
            if prod.count(nt) >= 2:
                encontrados.append((nt, prod))
    return encontrados


def detectar_recursion_ambigua(gramatica):
    """
    Detecta si un NT tiene a la vez recursión izquierda Y derecha,
    lo que garantiza ambigüedad para cadenas con 3+ tokens.
    """
    ambiguos = []
    for nt, prods in gramatica.items():
        tiene_izq = any(p and p[0] == nt for p in prods)
        tiene_der = any(p and p[-1] == nt for p in prods)
        if tiene_izq and tiene_der:
            ambiguos.append(nt)
    return ambiguos


# ─── Búsqueda exhaustiva en cadenas cortas ────────────────────────────────

def obtener_terminales(gramatica):
    nts = set(gramatica.keys())
    terms = set()
    for prods in gramatica.values():
        for prod in prods:
            for s in prod:
                if s not in nts and s not in ('eps', 'ε'):
                    terms.add(s)
    return terms


def buscar_cadena_ambigua(gramatica, nts, inicio, max_len=4):
    """Busca la cadena más corta con más de un árbol de análisis."""
    terms = sorted(obtener_terminales(gramatica))
    if not terms:
        return None, 0
    for length in range(1, max_len + 1):
        for cadena in iproduct(terms, repeat=length):
            memo = {}
            count = contar_arboles(gramatica, nts, inicio, cadena, memo)
            if count >= 2:
                return list(cadena), count
    return None, 0


# ─── Análisis principal ───────────────────────────────────────────────────

def analizar(gramatica, orden):
    nts = set(gramatica.keys())
    inicio = orden[0]
    es_ambigua = False

    print("\n── Análisis de Ambigüedad ──────────────────────────────────")

    # Paso 1: patrón estructural directo
    patrones = detectar_patron_directo(gramatica)
    if patrones:
        print("\n[!] Patrón ambiguo directo detectado (A aparece 2+ veces en RHS):")
        for nt, prod in patrones:
            print(f"    {nt} → {' '.join(prod)}")
        es_ambigua = True

    # Paso 2: recursión izquierda + derecha simultánea
    rec_ambiguos = detectar_recursion_ambigua(gramatica)
    for nt in rec_ambiguos:
        if nt not in [p[0] for p in patrones]:
            print(f"\n[!] '{nt}' tiene recursión izquierda Y derecha → ambigüedad potencial.")
            es_ambigua = True

    # Paso 3: búsqueda exhaustiva en cadenas cortas
    print("\n  Buscando cadenas con múltiples árboles (longitud 1 – 4)...")
    cadena, count = buscar_cadena_ambigua(gramatica, nts, inicio)
    if cadena:
        print(f"  [!] Cadena ambigua encontrada: ' {' '.join(cadena)} '")
        print(f"      → {count} árboles de análisis distintos")
        es_ambigua = True
    elif not es_ambigua:
        print("  No se encontró ambigüedad para cadenas de longitud ≤ 4.")

    return es_ambigua


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  EJERCICIO 1: Detector de Ambigüedad en GIC")
    print("=" * 60 + "\n")

    gramatica, orden = leer_gramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    print(f"\n  Símbolo inicial : {orden[0]}")
    print("  Producciones:")
    for nt in orden:
        for p in gramatica[nt]:
            print(f"    {nt} → {' '.join(p)}")

    es_ambigua = analizar(gramatica, orden)

    print("\n" + "=" * 60)
    print(f"  RESULTADO: La gramática {'ES AMBIGUA' if es_ambigua else 'NO ES AMBIGUA (cadenas ≤ 4)'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
