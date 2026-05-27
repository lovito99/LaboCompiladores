%{
#include <stdio.h>
%}

ENTERO  [0-9]+
REAL    [0-9]+"."[0-9]+

%%

{REAL}      { printf("NUMERO REAL         : %s\n", yytext); }
{ENTERO}    { printf("NUMERO ENTERO       : %s\n", yytext); }

"+"         { printf("OPERADOR SUMA       : +\n"); }
"-"         { printf("OPERADOR RESTA      : -\n"); }
"*"         { printf("OPERADOR MULT       : *\n"); }
"/"         { printf("OPERADOR DIV        : /\n"); }
"^"         { printf("OPERADOR POTENCIA   : ^\n"); }

"("         { printf("PARENTESIS APERTURA : (\n"); }
")"         { printf("PARENTESIS CIERRE   : )\n"); }

[ \t\n]+    { /* ignorar espacios en blanco */ }
.           { printf("CARACTER DESCONOCIDO: %s\n", yytext); }

%%

int main(int argc, char *argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            fprintf(stderr, "No se pudo abrir el archivo: %s\n", argv[1]);
            return 1;
        }
    }
    yylex();
    return 0;
}

int yywrap() { return 1; }
