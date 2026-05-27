%{
/*
 * ejercicio2.y
 * Analizador sintáctico para expresiones aritméticas
 * GIC (extendida con precedencia):
 *   E --> E '+' E | E '-' E | E '*' E | E '/' E | '(' E ')' | T
 *   T --> NUMERO
 *
 * La ambigüedad se resuelve con declaraciones de precedencia:
 *   - '+' y '-': asociativos por la izquierda, menor precedencia
 *   - '*' y '/': asociativos por la izquierda, mayor precedencia
 *
 * Laboratorio 3 - Flex + Bison
 */
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int  yylex(void);
%}

/* Tipos semánticos */
%union {
    int ival;
}

/* Tokens */
%token <ival> NUMERO

/* Precedencia y asociatividad (de menor a mayor) */
%left  '+' '-'
%left  '*' '/'

/* Resultado no terminal */
%type <ival> expr

/* Opciones de error verboso */
%define parse.error verbose

%%

/* Regla inicial */
input:
    expr    { printf("Resultado: %d\n", $1); }
    ;

/* Expresión aritmética */
expr:
    expr '+' expr   { $$ = $1 + $3; }
    | expr '-' expr { $$ = $1 - $3; }
    | expr '*' expr { $$ = $1 * $3; }
    | expr '/' expr {
                        if ($3 == 0) {
                            fprintf(stderr, "Error: division por cero\n");
                            $$ = 0;
                        } else {
                            $$ = $1 / $3;
                        }
                    }
    | '(' expr ')'  { $$ = $2; }
    | NUMERO        { $$ = $1; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error sintáctico: %s\n", s);
}

int main(void) {
    printf("Ingrese una expresion aritmetica: ");
    yyparse();
    return 0;
}
