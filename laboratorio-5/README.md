# Laboratorio 5 — Conjuntos Primeros/First y Siguientes/Follow

**Nombre:** Efrain Vitorino Maric
**Código:** 160337
**Curso:** IF454AIN - Compiladores
**Profesor:** Victor Dario Sosa Jauregui
**Universidad:** Universidad Nacional San Antonio Abad del Cusco
**Escuela Profesional:** Ingeniería Informática y de Sistemas

Implementaciones en Python de los algoritmos para calcular los conjuntos Primero/First y Siguiente/Follow en gramáticas libres de contexto.

---

## Objetivo

Desarrollar funciones en Python que calculen los conjuntos Primeros/First y Siguientes/Follow para una gramática libre de contexto, aplicando los algoritmos (definiciones) correspondientes.

---

## Ejercicios

### Ejercicio 1 — Cálculo del Conjunto Primero/First
**Archivo:** `ejercicio1.py`

Implementa una función que calcula el conjunto Primero/First para todos los no terminales de una gramática libre de contexto.

**Algoritmo aplicado:**
1. Si `X` es terminal → `Primero(X) = {X}`
2. Si `X → ε` → agregar `ε` a `Primero(X)`
3. Si `X → Y1 Y2 ... Yk`:
   - Agregar `Primero(Y1) - {ε}` a `Primero(X)`
   - Si `ε ∈ Primero(Y1)`, agregar `Primero(Y2) - {ε}`
   - Si `ε ∈ Primero(Y1) ... Primero(Yk)`, agregar `ε` a `Primero(X)`

Además muestra el conjunto Primero de cada producción individual.

### Ejercicio 2 — Cálculo del Conjunto Siguiente/Follow
**Archivo:** `ejercicio2.py`

Implementa funciones que calculan tanto el conjunto Primero/First como el conjunto Siguiente/Follow para todos los no terminales de una gramática libre de contexto.

**Algoritmo aplicado para Siguiente/Follow:**
1. Agregar `$` a `Siguiente(S)`, donde `S` es el símbolo inicial.
2. Si hay una producción `A → αBβ`:
   - Agregar `Primero(β) - {ε}` a `Siguiente(B)`
3. Si hay una producción `A → αB`, o `A → αBβ` donde `ε ∈ Primero(β)`:
   - Agregar `Siguiente(A)` a `Siguiente(B)`

Ambos conjuntos se calculan usando un enfoque iterativo de punto fijo.

---

## Archivos de prueba

| Archivo       | Descripción |
|---------------|-------------|
| `prueba1.txt` | Gramática clásica de expresiones aritméticas (sin recursión izquierda): `E → T Ep`, `Ep → + T Ep \| eps`, `T → F Tp`, `Tp → * F Tp \| eps`, `F → ( E ) \| id` |
| `prueba2.txt` | Gramática con múltiples producciones epsilon: `S → A B C`, `A → a \| eps`, `B → b \| eps`, `C → c \| eps` |
| `prueba3.txt` | Gramática con recursión y epsilon: `S → A a \| b`, `A → A c \| S d \| eps` |

---

## Ejecución

### Modo interactivo

```bash
make run1   # Ejercicio 1 (Primero/First)
make run2   # Ejercicio 2 (Primero/First + Siguiente/Follow)
```

### Con archivos de prueba

```bash
make test1  # Ejercicio 1 con prueba1.txt
make test2  # Ejercicio 1 con prueba2.txt
make test3  # Ejercicio 1 con prueba3.txt
make test4  # Ejercicio 2 con prueba1.txt
make test5  # Ejercicio 2 con prueba2.txt
make test6  # Ejercicio 2 con prueba3.txt

make test_all  # Ejecutar todos los tests
```

### Directamente con Python

```bash
python3 ejercicio1.py < prueba1.txt
python3 ejercicio2.py < prueba1.txt
```

---

## Formato de gramática

```
A -> alfa | beta
B -> gamma
```

- Un no terminal por línea (puede tener múltiples alternativas separadas por `|`).
- Los símbolos terminales y no terminales se separan por espacios.
- El símbolo vacío (ε) se escribe como `eps`.
- Una **línea vacía** indica el fin de la gramática.
- El **símbolo inicial** es el no terminal de la primera producción.

---

## Salidas de ejemplo

### Ejercicio 1 — `python3 ejercicio1.py < prueba1.txt`

```
============================================================
  EJERCICIO 1: Cálculo del Conjunto Primero/First
============================================================

Ingrese la gramática (formato: A -> alfa | beta)
Símbolo vacío (ε) se representa como 'eps'.
Deje una línea vacía para terminar.

    
  Símbolo inicial : E
  Producciones:
    E → T Ep
    Ep → + T Ep
    Ep → eps
    T → F Tp
    Tp → * F Tp
    Tp → eps
    F → ( E )
    F → id

── Conjuntos Primero/First ──────────────────────────────────

  Primero(E) = { (, id }
  Primero(Ep) = { +, eps }
  Primero(T) = { (, id }
  Primero(Tp) = { *, eps }
  Primero(F) = { (, id }

── Primero de cada producción ───────────────────────────────

  Primero(E → T Ep) = { (, id }
  Primero(Ep → + T Ep) = { + }
  Primero(Ep → eps) = { eps }
  Primero(T → F Tp) = { (, id }
  Primero(Tp → * F Tp) = { * }
  Primero(Tp → eps) = { eps }
  Primero(F → ( E )) = { ( }
  Primero(F → id) = { id }

============================================================
  Cálculo de Primero/First completado exitosamente
============================================================
```

### Ejercicio 2 — `python3 ejercicio2.py < prueba1.txt`

```
============================================================
  EJERCICIO 2: Cálculo de Primero/First y Siguiente/Follow
============================================================

Ingrese la gramática (formato: A -> alfa | beta)
Símbolo vacío (ε) se representa como 'eps'.
Deje una línea vacía para terminar.

    
  Símbolo inicial : E
  Producciones:
    E → T Ep
    Ep → + T Ep
    Ep → eps
    T → F Tp
    Tp → * F Tp
    Tp → eps
    F → ( E )
    F → id

── Conjuntos Primero/First ──────────────────────────────────

  Primero(E) = { (, id }
  Primero(Ep) = { +, eps }
  Primero(T) = { (, id }
  Primero(Tp) = { *, eps }
  Primero(F) = { (, id }

── Conjuntos Siguiente/Follow ───────────────────────────────

  Siguiente(E) = { ), $ }
  Siguiente(Ep) = { ), $ }
  Siguiente(T) = { ), +, $ }
  Siguiente(Tp) = { ), +, $ }
  Siguiente(F) = { ), *, +, $ }

============================================================
  Cálculo de Primero/First y Siguiente/Follow completado
============================================================
```

---

## Requisitos

- Python 3.8+
- Sin dependencias externas (sólo biblioteca estándar).
