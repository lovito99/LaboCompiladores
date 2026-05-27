%{
/*
 * ejercicio1.l
 * Analizador léxico para fracciones N/N
 * Laboratorio 3 - Flex + Bison
 */
#include "ejercicio1.tab.h"
#include <stdlib.h>
%}

%%

[0-9]+      {
                yylval.ival = atoi(yytext);
                return NUMERO;
            }

"/"         { return '/'; }

[ \t\n]+    { /* ignorar espacios en blanco y saltos de línea */ }

.           {
                fprintf(stderr, "Error léxico: carácter no reconocido '%s'\n", yytext);
                return 0;
            }

%%

int yywrap() { return 1; }
