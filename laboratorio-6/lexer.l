%{
#include "analizador.tab.h"
#include <stdio.h>
#include <stdlib.h>

int errores_lexicos = 0;

#define YY_USER_ACTION                  \
    yylloc.first_line = yylineno;       \
    yylloc.last_line = yylineno;
%}

%option noyywrap yylineno nounput noinput

%%

[0-9]+      {
                yylval.valor = atoi(yytext);
                return NUM;
            }
"+"         { return '+'; }
"-"         { return '-'; }
"*"         { return '*'; }
"/"         { return '/'; }
"("         { return '('; }
")"         { return ')'; }
\n          { return NL; }
[ \t\r]+    { /* Ignorar espacios y tabulaciones */ }
.           {
                fprintf(stderr, "Linea %d: Error lexico. Caracter no reconocido '%s'.\n", yylineno, yytext);
                errores_lexicos++;
            }

%%
