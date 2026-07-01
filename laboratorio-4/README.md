# Laboratorio 4 — Ambigüedad y Recursión en Gramáticas Independientes del Contexto

**Nombre:** Efrain Vitorino Marin
**Código:** 160337
**Curso:** Compiladores

Implementaciones en Python de algoritmos de análisis y transformación de GIC.

---

## Ejercicios

### Ejercicio 1 — Detector de Ambigüedad
**Archivo:** `ejercicio1.py`

Determina si una GIC es ambigua. Aplica dos estrategias:
1. Detección de **patrones directos**: un no-terminal aparece dos o más veces en el lado derecho de una producción.
2. Búsqueda por **fuerza bruta**: genera cadenas de longitud 1–4 y verifica si alguna admite múltiples derivaciones izquierdas distintas.

**Entrada esperada:** producciones en formato `A -> alfa | beta`. El símbolo vacío se representa como `eps`.

### Ejercicio 2 — Eliminación de Ambigüedad
**Archivo:** `ejercicio2.py`

Reescribe una GIC ambigua introduciendo **jerarquía de precedencia** y **asociatividad por la izquierda**. El usuario especifica los grupos de precedencia (de menor a mayor), y el algoritmo genera una gramática no ambigua equivalente con no-terminales auxiliares (`E1`, `E_base`, etc.).

**Entrada esperada:** producciones de la gramática + grupos de precedencia (un nivel por línea, operadores separados por espacio).

### Ejercicio 3 — Detector de Recursión por la Izquierda
**Archivo:** `ejercicio3.py`

Detecta si una GIC contiene recursión por la izquierda, distinguiendo entre:
- **Directa:** `A → A α`
- **Indirecta:** ciclo `A → B → … → A` en las derivaciones izquierdas.

Reporta todos los no-terminales afectados y el tipo de recursión de cada uno.

### Ejercicio 4 — Eliminación de Recursión por la Izquierda
**Archivo:** `ejercicio4.py`

Aplica el **algoritmo estándar** de eliminación de recursión por la izquierda:
- Elimina la recursión directa introduciendo un no-terminal primo (`A'`).
- Sustituye primero las producciones indirectas antes de eliminar la recursión directa resultante.

Produce una gramática equivalente sin ningún tipo de recursión izquierda.

---

## Archivos de prueba

| Archivo       | Ejercicio | Descripción |
|---------------|-----------|-------------|
| `prueba1.txt` | 1         | Gramática de expresiones `E → E + E \| E * E \| ( E ) \| id` |
| `prueba2.txt` | 2         | Misma gramática + niveles de precedencia `+` < `*` |
| `prueba3.txt` | 3         | Gramática con recursión directa (`A`) e indirecta (`B`, `C`) |
| `prueba4.txt` | 4         | Gramática clásica de expresiones con recursión izquierda directa |

---

## Ejecución

### Modo interactivo

```bash
make run1   # Ejercicio 1
make run2   # Ejercicio 2
make run3   # Ejercicio 3
make run4   # Ejercicio 4
```

### Con archivos de prueba

```bash
make test1  # Ejercicio 1 con prueba1.txt
make test2  # Ejercicio 2 con prueba2.txt
make test3  # Ejercicio 3 con prueba3.txt
make test4  # Ejercicio 4 con prueba4.txt

make test_all  # Ejecutar todos los tests
```

### Directamente con Python

```bash
python3 ejercicio1.py < prueba1.txt
python3 ejercicio2.py < prueba2.txt
python3 ejercicio3.py < prueba3.txt
python3 ejercicio4.py < prueba4.txt
```

---

## Formato de gramática

```
A -> alfa | beta
B -> gamma
```

- Un no-terminal por línea (puede tener múltiples alternativas separadas por `|`).
- Los símbolos terminales y no-terminales se separan por espacios.
- El símbolo vacío (ε) se escribe como `eps`.
- Una **línea vacía** indica el fin de la gramática.
- El **símbolo inicial** es el no-terminal de la primera producción.

---

## Salidas de ejemplo

### Ejercicio 1 — `python3 ejercicio1.py < prueba1.txt`

```
============================================================
  EJERCICIO 1: Detector de Ambigüedad en GIC
============================================================

Ingrese la gramática (formato: A -> alfa | beta)
Símbolo vacío (ε) se representa como 'eps'.
Deje una línea vacía para terminar.

    
  Símbolo inicial : E
  Producciones:
    E → E + E
    E → E * E
    E → ( E )
    E → id

── Análisis de Ambigüedad ──────────────────────────────────

[!] Patrón ambiguo directo detectado (A aparece 2+ veces en RHS):
    E → E + E
    E → E * E

  Buscando cadenas con múltiples árboles (longitud 1 – 4)...

============================================================
  RESULTADO: La gramática ES AMBIGUA
============================================================
```

### Ejercicio 2 — `python3 ejercicio2.py < prueba2.txt`

```
==============================================================
  EJERCICIO 2: Eliminación de Ambigüedad en GIC
==============================================================

Ingrese la gramática ambigua (formato: A -> alfa | beta)
Deje una línea vacía para terminar.

    
  Símbolo inicial : E
  Gramática ingresada:
  E → E + E
  E → E * E
  E → ( E )
  E → id

[!] NT ambiguo detectado: E
    Operadores encontrados: ['+', '*']
    Producciones base      : ['(  E  )', 'id']

  Operadores a ordenar: ['+', '*']
  Ingrese los grupos de precedencia de MENOR a MAYOR.
  Separe operadores del mismo nivel con coma, grupos distintos con Enter.
  (Ejemplo: para + y -, luego * y /  →  escriba  '+ -'  luego  '* /')
  Línea vacía para terminar.

  Nivel 1:   Nivel 2:   Nivel 3: 
── Gramática NO AMBIGUA resultante ─────────────────────────
  E → E + E1
  E → E1
  E1 → E1 * E_base
  E1 → E_base
  E_base → ( E )
  E_base → id

  Jerarquía de precedencia aplicada (menor → mayor):
    Nivel 1: ['+']
    Nivel 2: ['*']

==============================================================
  La gramática reescrita es asociativa por la izquierda
  y respeta la precedencia indicada.
==============================================================
```

### Ejercicio 3 — `python3 ejercicio3.py < prueba3.txt`

```
==============================================================
  EJERCICIO 3: Detector de Recursión por la Izquierda
==============================================================

Ingrese la gramática (formato: A -> alfa | beta)
Deje una línea vacía para terminar.

        
  Símbolo inicial : A
  Producciones:
    A → A a
    A → b
    B → C d
    C → B e
    C → f

── Análisis de Recursión por la Izquierda ──────────────────

  [!] Recursión DIRECTA detectada:
      A → A a

  [!] Recursión INDIRECTA detectada:
      Ciclo: C → B → C
      Ciclo: B → C → B

── Resumen ─────────────────────────────────────────────────
  NTs con recursión izq.: ['A', 'B', 'C']

  Tipo de recursión:
    A : DIRECTA
    B : INDIRECTA
    C : INDIRECTA

==============================================================
  RESULTADO: TIENE recursión por la izquierda
==============================================================
```

### Ejercicio 4 — `python3 ejercicio4.py < prueba4.txt`

```
==============================================================
  EJERCICIO 4: Eliminación de Recursión por la Izquierda
==============================================================

Ingrese la gramática (formato: A -> alfa | beta)
Deje una línea vacía para terminar.

        
  Símbolo inicial : E
  Gramática ORIGINAL:
  E → E + T
  E → T
  T → T * F
  T → F
  F → ( E )
  F → id

── Aplicando algoritmo de eliminación ──────────────────────

  Pasos realizados:
  Recursión directa eliminada en E  →  se crea E'
  Recursión directa eliminada en T  →  se crea T'

── Gramática RESULTANTE (sin recursión izquierda) ──────────
  E → T E'
  T → F T'
  ...
==============================================================
```

---

## Requisitos

- Python 3.8+
- Sin dependencias externas (sólo biblioteca estándar).
