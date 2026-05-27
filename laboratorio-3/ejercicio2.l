%{
/*
 * ejercicio2.l
 * Analizador léxico para expresiones aritméticas
 * Laboratorio 3 - Flex + Bison
 */
#include "ejercicio2.tab.h"
#include <stdlib.h>
%}

%%

[0-9]+      {
                yylval.ival = atoi(yytext);
                return NUMERO;
            }

"+"         { return '+'; }
"-"         { return '-'; }
"*"         { return '*'; }
"/"         { return '/'; }
"("         { return '('; }
")"         { return ')'; }

\n          { return 0; }   /* fin de expresión → señal de EOF al parser */
[ \t]+      { /* ignorar espacios y tabulaciones */ }

.           {
                fprintf(stderr, "Error léxico: carácter no reconocido '%s'\n", yytext);
                return 0;
            }

%%

int yywrap() { return 1; }
