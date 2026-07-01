%{
/*
 * analizador.y
 * Laboratorio 6 - Analizador sintactico LR con Flex + Bison.
 *
 * Lenguaje soportado:
 *   - Declaraciones: int x, y;
 *   - Asignaciones: x = 10 + 2;
 *   - Entrada/salida: read(x); print(x + 1);
 *   - Bloques: { ... }
 *   - Condicionales: if (x > 0) { ... } else { ... }
 *   - Bucles: while (x < 10) { ... }
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);

extern int errores_lexicos;
extern int yylineno;

int errores_sintacticos = 0;
%}

%define parse.error verbose
%locations

%union {
    int ival;
    char *sval;
}

%token <sval> IDENTIFICADOR
%token <ival> NUMERO BOOL_LITERAL
%token INT FLOAT BOOL IF ELSE WHILE READ PRINT
%token GE LE EQ NE AND OR NOT

%left OR
%left AND
%right NOT
%nonassoc '>' '<' GE LE EQ NE
%left '+' '-'
%left '*' '/'
%right UMINUS
%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%

programa:
      lista_sentencias
        {
            printf("\nAnalisis sintactico finalizado correctamente.\n");
        }
    ;

lista_sentencias:
      /* vacio */
    | lista_sentencias sentencia
    ;

sentencia:
      declaracion ';'
        {
            printf("Linea %d: declaracion valida.\n", @1.first_line);
        }
    | asignacion ';'
        {
            printf("Linea %d: asignacion valida.\n", @1.first_line);
        }
    | lectura ';'
        {
            printf("Linea %d: lectura valida.\n", @1.first_line);
        }
    | escritura ';'
        {
            printf("Linea %d: escritura valida.\n", @1.first_line);
        }
    | bloque
        {
            printf("Linea %d: bloque valido.\n", @1.first_line);
        }
    | seleccion
        {
            printf("Linea %d: condicional valido.\n", @1.first_line);
        }
    | iteracion
        {
            printf("Linea %d: bucle while valido.\n", @1.first_line);
        }
    | error ';'
        {
            fprintf(stderr, "Recuperacion: se descarto la sentencia erronea en la linea %d.\n", @1.first_line);
            yyerrok;
        }
    ;

declaracion:
      tipo lista_identificadores
    ;

tipo:
      INT
    | FLOAT
    | BOOL
    ;

lista_identificadores:
      IDENTIFICADOR
        {
            free($1);
        }
    | lista_identificadores ',' IDENTIFICADOR
        {
            free($3);
        }
    ;

asignacion:
      IDENTIFICADOR '=' expresion
        {
            free($1);
        }
    ;

lectura:
      READ '(' IDENTIFICADOR ')'
        {
            free($3);
        }
    ;

escritura:
      PRINT '(' expresion ')'
    ;

bloque:
      '{' lista_sentencias '}'
    ;

seleccion:
      IF '(' condicion ')' sentencia %prec LOWER_THAN_ELSE
    | IF '(' condicion ')' sentencia ELSE sentencia
    ;

iteracion:
      WHILE '(' condicion ')' sentencia
    ;

condicion:
      expresion operador_relacional expresion
    | BOOL_LITERAL
    | '(' condicion ')'
    | NOT condicion
    | condicion AND condicion
    | condicion OR condicion
    ;

operador_relacional:
      '>'
    | '<'
    | GE
    | LE
    | EQ
    | NE
    ;

expresion:
      expresion '+' expresion
    | expresion '-' expresion
    | expresion '*' expresion
    | expresion '/' expresion
    | '-' expresion %prec UMINUS
    | '(' expresion ')'
    | NUMERO
    | IDENTIFICADOR
        {
            free($1);
        }
    ;

%%

void yyerror(const char *s) {
    errores_sintacticos++;
    fprintf(stderr, "Error sintactico en linea %d: %s\n", yylineno, s);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("LABORATORIO 6 - Analizador Sintactico LR con Flex + Bison\n");
    printf("Ingrese el programa fuente. Presione Ctrl+D para terminar.\n\n");

    int resultado = yyparse();
    if (resultado == 0 && errores_lexicos == 0 && errores_sintacticos == 0) {
        printf("Entrada aceptada por la gramatica.\n");
        return EXIT_SUCCESS;
    }

    printf("Entrada rechazada. Errores lexicos: %d. Errores sintacticos: %d.\n",
           errores_lexicos, errores_sintacticos);
    return EXIT_FAILURE;
}
