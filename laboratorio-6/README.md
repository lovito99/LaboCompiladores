# LABORATORIO N° 06 — Analizador Sintactico LR con Flex y Bison

**Nombre:** Efrain Vitorino Maric  
**Codigo:** 160337  
**Curso:** IF454AIN - Compiladores  
**Profesor:** Victor Dario Sosa Jauregui  
**Universidad:** Universidad Nacional San Antonio Abad del Cusco  
**Escuela Profesional:** Ingenieria Informatica y de Sistemas

Implementacion de un analizador sintactico LR usando Flex y Bison. El programa reconoce expresiones aritmeticas con numeros enteros y decimales positivos, aplica precedencia de operadores, evalua la expresion y muestra el resultado.

---

## Objetivo

Implementar un analizador sintactico con Flex y Bison que permita:

- Reconocer expresiones aritmeticas.
- Aplicar precedencia y asociatividad de operadores.
- Evaluar expresiones usando acciones semanticas.
- Incluir suma, resta, multiplicacion, division, modulo y potencia.
- Mostrar el resultado de cada expresion ingresada.
- Detectar errores sintacticos, lexicos y matematicos.

---

## Archivos

| Archivo | Descripcion |
|---------|-------------|
| `lexer.l` | Analizador lexico en Flex. Reconoce numeros, operadores, parentesis y saltos de linea. |
| `analizador.y` | Analizador sintactico en Bison. Define la gramatica, precedencia y acciones semanticas. |
| `Makefile` | Automatiza la compilacion, ejecucion y limpieza del proyecto. |
| `analizador` | Ejecutable generado despues de compilar. |

No se utilizan archivos de prueba porque las expresiones se ingresan manualmente por consola.

---

## Gramatica

```text
input  -> vacio
        | input linea

linea  -> expr NL
        | NL
        | expr operador NL
        | operador_inicio expr NL
        | error NL

expr   -> expr '+' expr
        | expr '-' expr
        | expr '*' expr
        | expr '/' expr
        | expr '%' expr
        | expr '**' expr
        | '-' expr
        | '(' expr ')'
        | NUM
```

---

## Precedencia y asociatividad

La precedencia se define en `analizador.y`:

```yacc
%left '+' '-'          /* menor prioridad, izquierda a derecha */
%left '*' '/' '%'      /* prioridad media, izquierda a derecha */
%right UMINUS          /* signo menos unario: -5 */
%right POTENCIA        /* mayor prioridad, derecha a izquierda */
```

En Bison, las declaraciones que aparecen despues tienen mayor prioridad. Por eso `**` se evalua antes que `*`, `/`, `%`, `+` y `-`.

La palabra `%left` indica asociatividad de izquierda a derecha. La potencia usa `%right`, por eso se agrupa de derecha a izquierda.

Ejemplos:

```text
10-5-2     -> (10-5)-2
2+3*4      -> 2+(3*4)
(2+3)*4    -> los parentesis cambian la prioridad
2**3**2      -> 2**(3**2)
-2**2        -> -(2**2)
(-2)**2      -> (-2)**2
```

---

## Acciones semanticas

El parser calcula el resultado usando `$$`, `$1`, `$2`, `$3`.

```yacc
expr '+' expr { $$ = $1 + $3; }
expr '-' expr { $$ = $1 - $3; }
expr '*' expr { $$ = $1 * $3; }
expr '/' expr { $$ = $1 / $3; }
expr '%' expr { $$ = fmod($1, $3); }
expr '**' expr { $$ = pow($1, $3); }
```

Cada numero reconocido por Flex se convierte con `atof` y se guarda en `yylval.valor`:

```lex
[0-9]+(\.[0-9]+)?|\.[0-9]+ {
    yylval.valor = atof(yytext);
    return NUM;
}
```

---

## Compilacion

Desde la carpeta `laboratorio-6`:

```bash
make clean
make all
```

Comandos ejecutados por el `Makefile`:

```bash
bison -d analizador.y -o analizador.tab.c
flex -o lexer.yy.c lexer.l
gcc -Wall -Wextra -g analizador.tab.c lexer.yy.c -o analizador -lm
```

El proyecto enlaza la libreria matematica con `-lm` para usar `pow` y `fmod`.

---

## Ejecucion manual

```bash
make run
```

O directamente:

```bash
./analizador
```

Luego ingresar expresiones y finalizar con `Ctrl + D`.

---

## Ejemplos

Entrada:

```text
1+2*3
(1+2)*3
10-5-2
20/4/5
-5+2
10%3
10.5%4
2**3**2
```

Salida:

```text
Resultado = 7
Resultado = 9
Resultado = 3
Resultado = 1
Resultado = -3
Resultado = 1
Resultado = 2.5
Resultado = 512
```

Entrada con error:

```text
1+1+
```

Salida:

```text
Linea 1: Error sintactico. Expresion incompleta despues del operador.
```

Errores matematicos:

```text
1/0
0**0
10%0
```

Salida:

```text
Linea 1: Error matematico. Division por cero.
Linea 2: Error matematico. Cero elevado a cero no esta definido.
Linea 3: Error matematico. Modulo por cero.
```

---

## Limpieza

```bash
make clean
```

Elimina el ejecutable y archivos temporales generados por Bison/Flex.

---

## Requisitos

- Flex
- Bison
- GCC
