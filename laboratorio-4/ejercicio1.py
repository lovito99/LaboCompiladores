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

def leerGramatica():
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


# ─── Contar árboles de análisis ────────────────────────────────────────────

ENPROCESO = object()   # centinela para detectar ciclos

def contarArboles(gramatica, nts, simbolo, tokens, memo):
    clave = (simbolo, tokens)
    valor = memo.get(clave)
    if valor is ENPROCESO:
        return 0
    if valor is not None:
        return valor

    if simbolo not in nts:
        res = 1 if tokens == (simbolo,) else 0
        memo[clave] = res
        return res

    memo[clave] = ENPROCESO
    total = 0
    for prod in gramatica.get(simbolo, []):
        if prod == ['eps'] or prod == ['ε']:
            total += 1 if not tokens else 0
        else:
            total += contarProd(gramatica, nts, prod, tokens, memo)
    memo[clave] = total
    return total


def contarProd(gramatica, nts, prod, tokens, memo):
    if not prod:
        return 1 if not tokens else 0
    if len(prod) == 1:
        return contarArboles(gramatica, nts, prod[0], tokens, memo)
    total = 0
    for i in range(len(tokens) + 1):
        izq = contarArboles(gramatica, nts, prod[0], tokens[:i], memo)
        if izq > 0:
            der = contarProd(gramatica, nts, prod[1:], tokens[i:], memo)
            total += izq * der
    return total


# ─── Detección de patrones ─────────────────────────────────────────────────

def detectarPatronDirecto(gramatica):
    encontrados = []
    for nt, prods in gramatica.items():
        for prod in prods:
            if prod.count(nt) >= 2:
                encontrados.append((nt, prod))
    return encontrados


def detectarRecursionAmbigua(gramatica):
    ambiguos = []
    for nt, prods in gramatica.items():
        tieneIzq = any(p and p[0] == nt for p in prods)
        tieneDer = any(p and p[-1] == nt for p in prods)
        if tieneIzq and tieneDer:
            ambiguos.append(nt)
    return ambiguos


# ─── Búsqueda exhaustiva en cadenas cortas ────────────────────────────────

def obtenerTerminales(gramatica):
    nts = set(gramatica.keys())
    terms = set()
    for prods in gramatica.values():
        for prod in prods:
            for s in prod:
                if s not in nts and s not in ('eps', 'ε'):
                    terms.add(s)
    return terms


def buscarCadenaAmbigua(gramatica, nts, inicio, maxLen=4):
    terms = sorted(obtenerTerminales(gramatica))
    if not terms:
        return None, 0
    for longitud in range(1, maxLen + 1):
        for cadena in iproduct(terms, repeat=longitud):
            memo = {}
            conteo = contarArboles(gramatica, nts, inicio, cadena, memo)
            if conteo >= 2:
                return list(cadena), conteo
    return None, 0


# ─── Análisis principal ───────────────────────────────────────────────────

def analizar(gramatica, orden):
    nts = set(gramatica.keys())
    inicio = orden[0]
    esAmbigua = False

    print("\n── Análisis de Ambigüedad ──────────────────────────────────")

    patrones = detectarPatronDirecto(gramatica)
    if patrones:
        print("\n[!] Patrón ambiguo directo detectado (A aparece 2+ veces en RHS):")
        for nt, prod in patrones:
            print(f"    {nt} → {' '.join(prod)}")
        esAmbigua = True

    recAmbiguos = detectarRecursionAmbigua(gramatica)
    for nt in recAmbiguos:
        if nt not in [p[0] for p in patrones]:
            print(f"\n[!] '{nt}' tiene recursión izquierda Y derecha → ambigüedad potencial.")
            esAmbigua = True

    print("\n  Buscando cadenas con múltiples árboles (longitud 1 – 4)...")
    cadena, conteo = buscarCadenaAmbigua(gramatica, nts, inicio)
    if cadena:
        print(f"  [!] Cadena ambigua encontrada: ' {' '.join(cadena)} '")
        print(f"      → {conteo} árboles de análisis distintos")
        esAmbigua = True
    elif not esAmbigua:
        print("  No se encontró ambigüedad para cadenas de longitud ≤ 4.")

    return esAmbigua


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  EJERCICIO 1: Detector de Ambigüedad en GIC")
    print("=" * 60 + "\n")

    gramatica, orden = leerGramatica()
    if not gramatica:
        print("[!] Gramática vacía."); return

    print(f"\n  Símbolo inicial : {orden[0]}")
    print("  Producciones:")
    for nt in orden:
        for p in gramatica[nt]:
            print(f"    {nt} → {' '.join(p)}")

    esAmbigua = analizar(gramatica, orden)

    print("\n" + "=" * 60)
    print(f"  RESULTADO: La gramática {'ES AMBIGUA' if esAmbigua else 'NO ES AMBIGUA (cadenas ≤ 4)'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
