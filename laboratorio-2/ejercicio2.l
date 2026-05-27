%{
#include <stdio.h>
%}

%%

"si"        { printf("ESTRUCTURA CONTROL  : si\n"); }
"mientras"  { printf("ESTRUCTURA CONTROL  : mientras\n"); }

"("         { printf("PARENTESIS APERTURA : (\n"); }
")"         { printf("PARENTESIS CIERRE   : )\n"); }
"{"         { printf("LLAVE APERTURA      : {\n"); }
"}"         { printf("LLAVE CIERRE        : }\n"); }

"=="        { printf("OPERADOR RELACIONAL : ==\n"); }
"!="        { printf("OPERADOR RELACIONAL : !=\n"); }
"<"         { printf("OPERADOR RELACIONAL : <\n"); }
">"         { printf("OPERADOR RELACIONAL : >\n"); }

"+"         { printf("OPERADOR ARITMETICO : +\n"); }
"-"         { printf("OPERADOR ARITMETICO : -\n"); }
"*"         { printf("OPERADOR ARITMETICO : *\n"); }
"/"         { printf("OPERADOR ARITMETICO : /\n"); }

[a-zA-Z]   { printf("IDENTIFICADOR       : %s\n", yytext); }

[ \t\n]+   { /* ignorar espacios en blanco */ }
.          { printf("CARACTER DESCONOCIDO: %s\n", yytext); }

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
