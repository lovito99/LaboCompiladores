%{
/*
 * ejercicio3.l
 * Analizador léxico para sentencias de asignación
 * Laboratorio 3 - Flex + Bison
 */
#include "ejercicio3.tab.h"
#include <stdlib.h>
#include <string.h>

static int prompt_needed = 1;

/* Intercepta la lectura de caracteres para mostrar el prompt >> */
#define YY_INPUT(buf, result, max_size)                      \
    do {                                                      \
        if (prompt_needed) {                                  \
            printf(">> ");                                    \
            fflush(stdout);                                   \
            prompt_needed = 0;                                \
        }                                                     \
        int _c = getchar();                                   \
        if (_c == '\n') prompt_needed = 1;                   \
        (result) = (_c == EOF) ? YY_NULL                      \
                               : (buf[0] = (char)_c, 1);     \
    } while (0)
%}

%%

[a-zA-Z_][a-zA-Z0-9_]*  {
                              yylval.sval = strdup(yytext);
                              return IDENTIFICADOR;
                          }

[0-9]+                   {
                              yylval.ival = atoi(yytext);
                              return NUMERO;
                          }

"="                      { return '='; }
"+"                      { return '+'; }
"-"                      { return '-'; }
";"                      { return ';'; }

[ \t\n]+                 { /* ignorar espacios en blanco y saltos de línea */ }

.                        {
                              fprintf(stderr, "Error léxico: carácter no reconocido '%s'\n", yytext);
                          }

%%

int yywrap() { return 1; }
