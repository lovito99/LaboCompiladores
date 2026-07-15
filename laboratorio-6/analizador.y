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

%union {
    int valor;
}

%token <valor> NUM
%token NL
%type <valor> expr

/*
   Precedencia y asociatividad:

   %left indica asociatividad de izquierda a derecha.
   Ejemplo: 10 - 5 - 2 se interpreta como (10 - 5) - 2.

   En Bison, las declaraciones que aparecen despues tienen mayor prioridad.
   Por eso '*' y '/' tienen mayor prioridad que '+' y '-'.
*/
%left '+' '-'      /* menor prioridad, izquierda a derecha */
%left '*' '/'      /* mayor prioridad, izquierda a derecha */
%right UMINUS      /* signo menos unario: -5 */

%%

input:
      /* vacio */
    | input linea
    ;

linea:
      expr NL
        {
            /* printf("Linea %d: Sintaxis correcta. Expresion valida encontrada.\n", @1.first_line); */
            printf("Resultado = %d\n", $1);
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
        {
            $$ = $1 + $3;
        }
    | expr '-' expr
        {
            $$ = $1 - $3;
        }
    | expr '*' expr
        {
            $$ = $1 * $3;
        }
    | expr '/' expr
        {
            if ($3 == 0) {
                errores_sintacticos++;
                fprintf(stderr, "Linea %d: Error sintactico. Division entre cero.\n", @3.first_line);
                $$ = 0;
            } else {
                $$ = $1 / $3;
            }
        }
    | '-' expr %prec UMINUS
        {
            $$ = -$2;
        }
    | '(' expr ')'
        {
            $$ = $2;
        }
    | NUM
        {
            $$ = $1;
        }
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

    /* printf("LABORATORIO 6 - Analizador Sintactico LR con Flex + Bison\n"); */
    /* printf("Introduce expresiones. Presiona Ctrl+D para terminar.\n\n"); */

    yyparse();

    if (errores_lexicos == 0 && errores_sintacticos == 0) {
        /* printf("\nEntrada aceptada por la gramatica.\n"); */
        return EXIT_SUCCESS;
    }

    /* printf("\nEntrada rechazada. Errores lexicos: %d. Errores sintacticos: %d.\n",
           errores_lexicos, errores_sintacticos); */
    return EXIT_FAILURE;
}
