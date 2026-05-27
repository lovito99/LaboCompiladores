# Laboratorio N° 02 — Analizador Lexicógrafo (léxico) con FLEX

## Requisitos

- `flex`
- `gcc`
- `make`

```bash
sudo apt install flex gcc make
```

## Compilación

Compilar los tres ejercicios de una sola vez:

```bash
make all
```

O compilar individualmente:

```bash
make ejercicio1
make ejercicio2
make ejercicio3
```

---

## Ejercicio 1 — Identificador de comentarios y palabras clave

Reconoce las palabras clave `inicio`, `fin`, `si`, `sino` y comentarios de una línea (`//`) y multilínea (`/* ... */`).

**Ejecutar:**
```bash
make run1
```

**Salida esperada con `prueba1.txt`:**
```
PALABRA CLAVE: inicio
COMENTARIO LINEA    : // Este es un comentario de una sola linea
PALABRA CLAVE: si
COMENTARIO MULTILINEA:  Este es un
   comentario
   multilinea 
PALABRA CLAVE: sino
PALABRA CLAVE: fin
```

---

## Ejercicio 2 — Análisis de estructuras de control

Identifica estructuras de control (`si`, `mientras`), paréntesis, llaves, operadores relacionales y aritméticos, e identificadores de un solo carácter.

**Ejecutar:**
```bash
make run2
```

**Salida esperada con `prueba2.txt`:**
```
ESTRUCTURA CONTROL  : si
PARENTESIS APERTURA : (
IDENTIFICADOR       : x
OPERADOR RELACIONAL : >
IDENTIFICADOR       : y
PARENTESIS CIERRE   : )
LLAVE APERTURA      : {
...
```

---

## Ejercicio 3 — Análisis de expresiones matemáticas

Clasifica números enteros y reales, operadores aritméticos (`+`, `-`, `*`, `/`, `^`) y paréntesis. No resuelve las expresiones.

**Ejecutar:**
```bash
make run3
```

**Salida esperada con `prueba3.txt`:**
```
PARENTESIS APERTURA : (
NUMERO ENTERO       : 3
OPERADOR SUMA       : +
NUMERO ENTERO       : 4
PARENTESIS CIERRE   : )
OPERADOR MULT       : *
NUMERO ENTERO       : 2
NUMERO REAL         : 5.5
OPERADOR DIV        : /
...
```

---

## Limpieza

Eliminar los ejecutables generados:

```bash
make clean
```

## Estructura del proyecto

```
laboratorio-2/
├── ejercicio1.l   # Comentarios y palabras clave
├── ejercicio2.l   # Estructuras de control
├── ejercicio3.l   # Expresiones matemáticas
├── prueba1.txt
├── prueba2.txt
├── prueba3.txt
└── Makefile
```
