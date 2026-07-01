# LABORATORIO N° 06 — Tabla de Analisis Sintactico LR con Flex y Bison

**Nombre:** Efrain Vitorino Maric
**Codigo:** 160337
**Curso:** IF454AIN - Compiladores
**Profesor:** Victor Dario Sosa Jauregui
**Universidad:** Universidad Nacional San Antonio Abad del Cusco
**Escuela Profesional:** Ingenieria Informatica y de Sistemas

Implementacion de un analizador sintactico LR usando Flex y Bison. El laboratorio define la gramatica de un mini lenguaje imperativo, acepta expresiones aritmeticas sueltas como `1+2`, integra el analizador lexico con el sintactico, genera la tabla LR de Bison y prueba entradas validas e invalidas.

---

## Objetivo

Implementar un analizador sintactico LR utilizando generadores de analizadores sintacticos como Flex y Bison, con el objetivo de entender y aplicar los conceptos de analisis sintactico y desarrollo de compiladores.

---

## Archivos

| Archivo | Descripcion |
|---------|-------------|
| `lexer.l` | Analizador lexico en Flex. Reconoce palabras reservadas, identificadores, numeros, operadores y delimitadores. |
| `analizador.y` | Analizador sintactico en Bison. Contiene la gramatica, precedencia, acciones semanticas y manejo de errores. |
| `Makefile` | Automatiza la compilacion, pruebas y generacion de la tabla LR. |
| `prueba1.txt` | Programa valido con declaraciones, asignaciones, lectura y escritura. |
| `prueba2.txt` | Programa valido con bloque, `while`, `if`, `else` y condiciones booleanas. |
| `prueba3.txt` | Expresiones con sumas validas e invalidas para probar reconocimiento y recuperacion. |

---

## Gramatica del lenguaje

```text
programa              -> lista_elementos
lista_elementos       -> ε | lista_elementos sentencia
                       | lista_elementos expresion fin_linea
                       | lista_elementos fin_linea

sentencia             -> declaracion ';'
                       | asignacion ';'
                       | lectura ';'
                       | escritura ';'
                       | bloque
                       | seleccion
                       | iteracion
                       | error ';'

declaracion           -> tipo lista_identificadores
tipo                  -> int | float | bool
lista_identificadores -> id | lista_identificadores ',' id

asignacion            -> id '=' expresion
lectura               -> read '(' id ')'
escritura             -> print '(' expresion ')'
bloque                -> '{' lista_sentencias '}'

seleccion             -> if '(' condicion ')' sentencia
                       | if '(' condicion ')' sentencia else sentencia
iteracion             -> while '(' condicion ')' sentencia

condicion             -> expresion operador_relacional expresion
                       | true | false
                       | '(' condicion ')'
                       | '!' condicion
                       | condicion '&&' condicion
                       | condicion '||' condicion

operador_relacional   -> '>' | '<' | '>=' | '<=' | '==' | '!='

expresion             -> expresion '+' expresion
                       | expresion '-' expresion
                       | expresion '*' expresion
                       | expresion '/' expresion
                       | '-' expresion
                       | '(' expresion ')'
                       | numero
                       | id

fin_linea             -> salto_de_linea | ';'
```

---

## Construccion del analizador LR

Bison construye automaticamente un analizador LALR(1), una variante practica de LR, a partir del archivo `analizador.y`.

Para compilar:

```bash
make all
```

Comandos ejecutados por el `Makefile`:

```bash
bison -d -v analizador.y -o analizador.tab.c
flex -o lexer.yy.c lexer.l
gcc -Wall -Wextra -g analizador.tab.c lexer.yy.c -o analizador
```

La opcion `-v` de Bison genera el archivo `analizador.output`, donde se observa la tabla/automata LR: estados, transiciones, reducciones y desplazamientos.

Para generar solo la tabla LR:

```bash
make tabla
```

---

## Ejecucion

```bash
make run       # Ejecuta prueba1.txt
make test1     # Entrada valida basica
make test2     # Entrada valida con if/else y while
make test3     # Entrada con errores
make test_all  # Ejecuta todas las pruebas y genera la tabla LR
```

Tambien se puede ejecutar directamente:

```bash
./analizador < prueba1.txt
```

---

## Salidas esperadas

### `make test1`

```text
LABORATORIO 6 - Analizador Sintactico LR con Flex + Bison
Ingrese el programa fuente. Presione Ctrl+D para terminar.

Linea 1: declaracion valida.
Linea 2: declaracion valida.
Linea 3: declaracion valida.
Linea 5: asignacion valida.
Linea 6: asignacion valida.
Linea 7: lectura valida.
Linea 8: escritura valida.

Analisis sintactico finalizado correctamente.
Entrada aceptada por la gramatica.
```

### `make test3`

La tercera prueba incluye sumas correctas (`1+2`, `1+2+3`, etc.) y errores intencionales (`3+`, `+4`). El parser debe reportar los errores y continuar analizando las expresiones restantes.

---

## Manejo de errores

El analizador incluye dos niveles de error:

- **Errores lexicos:** el lexer reporta simbolos no reconocidos e incrementa `errores_lexicos`.
- **Errores sintacticos:** Bison usa `%define parse.error verbose` para mostrar mensajes detallados. La produccion `error ';'` permite descartar una sentencia erronea y continuar con el resto del programa.

---

## Requisitos

- Flex 2.6+
- Bison 3.8+
- GCC
