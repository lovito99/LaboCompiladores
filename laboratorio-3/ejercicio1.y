%{
/*
 * ejercicio1.y
 * Analizador sintáctico para fracciones N/N
 * GIC:
 *   fraccion --> NUMERO '/' NUMERO
 *   NUMERO   --> [0-9]+
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

/* Opciones de error verboso */
%define parse.error verbose

%%

/* Regla inicial: leer una fracción */
input:
    fraccion
    ;

fraccion:
    NUMERO '/' NUMERO
    {
        if ($3 == 0)
            printf("Fraccion INVALIDA: denominador cero (%d/0)\n", $1);
        else
            printf("Fraccion VALIDA: %d/%d\n", $1, $3);
    }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error sintáctico: %s\n", s);
}

int main(void) {
    printf("Ingrese una fraccion (N/N): ");
    yyparse();
    return 0;
}
