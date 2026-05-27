%{
#include <stdio.h>

#define TAMANO 4096

char contenido[TAMANO];
int posicion;
%}

%x ESTADOMULTILINEA

%%

"//"[^\n]*              {
                            printf("COMENTARIO LINEA    : %s\n", yytext);
                        }

"/*"                    {
                            posicion = 0;
                            contenido[0] = '\0';
                            BEGIN(ESTADOMULTILINEA);
                        }

<ESTADOMULTILINEA>"*/" {
                            contenido[posicion] = '\0';
                            printf("COMENTARIO MULTILINEA: %s\n", contenido);
                            BEGIN(INITIAL);
                        }

<ESTADOMULTILINEA>.    {
                            if (posicion < TAMANO - 1)
                                contenido[posicion++] = yytext[0];
                        }

<ESTADOMULTILINEA>\n   {
                            if (posicion < TAMANO - 1)
                                contenido[posicion++] = '\n';
                        }

"inicio"                { printf("PALABRA CLAVE: inicio\n"); }
"fin"                   { printf("PALABRA CLAVE: fin\n"); }
"sino"                  { printf("PALABRA CLAVE: sino\n"); }
"si"                    { printf("PALABRA CLAVE: si\n"); }

[ \t\n]+                { /* ignorar espacios en blanco */ }
.                       { /* ignorar otros caracteres */ }

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
