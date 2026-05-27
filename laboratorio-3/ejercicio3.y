%{
/*
 * ejercicio3.y
 * Analizador sintáctico para sentencias de asignación
 * GIC:
 *   programa   --> sentencia ';'
 *              |   programa sentencia ';'
 *
 *   sentencia  --> IDENTIFICADOR '=' expresion
 *
 *   expresion  --> expresion '+' termino
 *              |   expresion '-' termino
 *              |   termino
 *
 *   termino    --> NUMERO
 *
 * Laboratorio 3 - Flex + Bison
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int  yylex(void);
%}

/* Tipos semánticos */
%union {
    int   ival;
    char *sval;
}

/* Tokens */
%token <sval> IDENTIFICADOR
%token <ival> NUMERO

/* Tipos de no terminales */
%type <ival> expresion termino
%type <sval> sentencia

/* Opciones de error verboso */
%define parse.error verbose

%%

/* Regla inicial: uno o más sentencias */
programa:
    sentencia ';'
    {
        printf("Asignacion reconocida: %s\n", $1);
        free($1);
    }
    | programa sentencia ';'
    {
        printf("Asignacion reconocida: %s\n", $2);
        free($2);
    }
    ;

/* Sentencia de asignación */
sentencia:
    IDENTIFICADOR '=' expresion
    {
        /* Construir string descriptivo de la asignación */
        char buf[256];
        snprintf(buf, sizeof(buf), "%s = %d", $1, $3);
        free($1);
        $$ = strdup(buf);
    }
    ;

/* Expresión aritmética (suma y resta) */
expresion:
    expresion '+' termino   { $$ = $1 + $3; }
    | expresion '-' termino { $$ = $1 - $3; }
    | termino               { $$ = $1; }
    ;

/* Término base */
termino:
    NUMERO  { $$ = $1; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error sintáctico: %s\n", s);
}

int main(void) {
    printf("Analizador de sentencias de asignacion\n");
    printf("Formato: variable = expresion;\n");
    printf("Presione Ctrl+D para terminar.\n\n");
    yyparse();
    return 0;
}
