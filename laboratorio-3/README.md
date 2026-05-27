# LABORATORIO N° 03 — Analizador Sintáctico con FLEX y BISON

## Objetivo

Desarrollar habilidades en la construcción de analizadores sintácticos utilizando Flex y Bison, comprendiendo la definición de Gramáticas Independientes del Contexto (GIC), la especificación de reglas gramaticales y la integración del analizador léxico con el analizador sintáctico para validar la estructura de un lenguaje.

---

## Compilación

```bash
make all
```

```
bison -d ejercicio1.y -o ejercicio1.tab.c
flex -o ejercicio1.lex.c ejercicio1.l
gcc ejercicio1.tab.c ejercicio1.lex.c -o ejercicio1
bison -d ejercicio2.y -o ejercicio2.tab.c
flex -o ejercicio2.lex.c ejercicio2.l
gcc ejercicio2.tab.c ejercicio2.lex.c -o ejercicio2
bison -d ejercicio3.y -o ejercicio3.tab.c
flex -o ejercicio3.lex.c ejercicio3.l
gcc ejercicio3.tab.c ejercicio3.lex.c -o ejercicio3
```

---

## Ejercicio 1 — Analizador Sintáctico de Fracciones (N/N)

### Descripción

Analizador léxico-sintáctico que reconoce y valida fracciones de la forma `N/N`, donde `N` es un número entero no negativo. Detecta denominador cero.

### GIC

```
FRACCION --> NUMERO '/' NUMERO
NUMERO   --> [0-9]+
```

### Ejecución y resultados

```bash
make run1
# ./ejercicio1 < prueba1.txt
# Ingrese una fraccion (N/N): Fraccion VALIDA: 3/4

./ejercicio1
# Ingrese una fraccion (N/N): 5/0
# Fraccion INVALIDA: denominador cero (5/0)

./ejercicio1
# Ingrese una fraccion (N/N): 7/3
# Fraccion VALIDA: 7/3
```

---

## Ejercicio 2 — Analizador Sintáctico de Expresiones Aritméticas

### Descripción

Analizador sintáctico para expresiones aritméticas con suma, resta, multiplicación y división. Respeta precedencia y asociatividad de operadores, y soporta paréntesis. Evalúa y muestra el resultado.

### GIC

```
E --> E '+' E | E '-' E | E '*' E | E '/' E | '(' E ')' | T
T --> NUMERO
```

Precedencia (de menor a mayor): `+`, `-` → `*`, `/`

### Ejecución y resultados

```bash
./ejercicio2
# Ingrese una expresion aritmetica: 10+5*5
# Resultado: 35

./ejercicio2
# Ingrese una expresion aritmetica: (10+5)*2
# Resultado: 30
```

---

## Ejercicio 3 — Analizador Sintáctico de Sentencias de Asignación

### Descripción

Analizador léxico-sintáctico para validar sentencias de asignación de la forma `variable = expresion;`. Acepta múltiples sentencias en modo interactivo y reporta cada asignación reconocida o los errores encontrados.

### GIC

```
programa   --> sentencia ';'
             | programa sentencia ';'

sentencia  --> IDENTIFICADOR '=' expresion

expresion  --> expresion '+' termino
             | expresion '-' termino
             | termino

termino    --> NUMERO
```

### Ejecución y resultados

```bash
./ejercicio3
# Analizador de sentencias de asignacion
# Formato: variable = expresion;
# Presione Ctrl+D para terminar.
#
# >> x=5+6;
# Asignacion reconocida: x = 11
# >> y=45+4555;
# Asignacion reconocida: y = 4600
# >> x=10+456655;
# Asignacion reconocida: x = 456665
```

Entrada inválida (error esperado):
```bash
# >> 5+3
# Error sintáctico: syntax error, unexpected NUMERO, expecting IDENTIFICADOR

# >> x=5+2       ← sin ';'
# Error sintáctico: syntax error, unexpected IDENTIFICADOR, expecting ';'
```

---

## Comandos útiles

| Comando      | Descripción                              |
|--------------|------------------------------------------|
| `make all`   | Compila los tres ejercicios              |
| `make run1`  | Ejecuta ejercicio1 con `prueba1.txt`     |
| `make run2`  | Ejecuta ejercicio2 con `prueba2.txt`     |
| `make run3`  | Ejecuta ejercicio3 con `prueba3.txt`     |
| `make clean` | Elimina los binarios generados           |
