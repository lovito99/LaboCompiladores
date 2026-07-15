%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);

extern int errores_lexicos;
extern int yylineno;

int errores_sintacticos = 0;
%}

%define parse.error verbose
%locations

%token NUM
%token NL

/*
   Definicion de precedencia y asociatividad:
   Los operadores en lineas inferiores tienen MAYOR prioridad.
   Por eso, '*' y '/' se evaluan antes que '+' y '-'.
*/
%left '+' '-'
%left '*' '/'
%right UMINUS

%%

input:
      /* vacio */
    | input linea
    ;

linea:
      expr NL
        {
            printf("Linea %d: Sintaxis correcta. Expresion valida encontrada.\n", @1.first_line);
        }
    | NL
        {
            /* Ignorar lineas vacias */
        }
    | expr operador NL
        {
            errores_sintacticos++;
            fprintf(stderr, "Linea %d: Error sintactico. Expresion incompleta despues del operador.\n", @2.first_line);
        }
    | operador_inicio expr NL
        {
            errores_sintacticos++;
            fprintf(stderr, "Linea %d: Error sintactico. La expresion no puede iniciar con ese operador.\n", @1.first_line);
        }
    | error NL
        {
            fprintf(stderr, "Linea %d: Recuperacion. Se descarto la expresion incorrecta.\n", @1.first_line);
            yyerrok;
        }
    ;

expr:
      expr '+' expr
    | expr '-' expr
    | expr '*' expr
    | expr '/' expr
    | '-' expr %prec UMINUS
    | '(' expr ')'
    | NUM
    ;

operador:
      '+'
    | '-'
    | '*'
    | '/'
    ;

operador_inicio:
      '+'
    | '*'
    | '/'
    ;

%%

void yyerror(const char *s)
{
    errores_sintacticos++;
    fprintf(stderr, "Linea %d: Error sintactico: %s\n", yylineno, s);
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("LABORATORIO 6 - Analizador Sintactico LR con Flex + Bison\n");
    printf("Introduce expresiones. Presiona Ctrl+D para terminar.\n\n");

    yyparse();

    if (errores_lexicos == 0 && errores_sintacticos == 0) {
        printf("\nEntrada aceptada por la gramatica.\n");
        return EXIT_SUCCESS;
    }

    printf("\nEntrada rechazada. Errores lexicos: %d. Errores sintacticos: %d.\n",
           errores_lexicos, errores_sintacticos);
    return EXIT_FAILURE;
}
