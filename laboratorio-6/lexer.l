%{
/*
 * lexer.l
 * Laboratorio 6 - Analizador lexico para el parser LR.
 */
#include "analizador.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int errores_lexicos = 0;

#define YY_USER_ACTION                  \
    yylloc.first_line = yylineno;       \
    yylloc.last_line = yylineno;
%}

%option noyywrap yylineno nounput noinput

%%

"int"           { return INT; }
"float"         { return FLOAT; }
"bool"          { return BOOL; }
"if"            { return IF; }
"else"          { return ELSE; }
"while"         { return WHILE; }
"read"          { return READ; }
"print"         { return PRINT; }
"true"          { yylval.ival = 1; return BOOL_LITERAL; }
"false"         { yylval.ival = 0; return BOOL_LITERAL; }

">="            { return GE; }
"<="            { return LE; }
"=="            { return EQ; }
"!="            { return NE; }
"&&"            { return AND; }
"||"            { return OR; }
"!"             { return NOT; }

[0-9]+          {
                    yylval.ival = atoi(yytext);
                    return NUMERO;
                }

[a-zA-Z_][a-zA-Z0-9_]* {
                    yylval.sval = strdup(yytext);
                    return IDENTIFICADOR;
                }

"//".*          { /* comentario de una linea */ }

[ \t\r\n]+      { /* ignorar espacios */ }

[;(),{}=+\-*/<>] { return yytext[0]; }

.               {
                    fprintf(stderr, "Error lexico en linea %d: simbolo no reconocido '%s'\n", yylineno, yytext);
                    errores_lexicos++;
                }

%%
