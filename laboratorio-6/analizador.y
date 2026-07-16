%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int yylex(void);
void yyerror(const char *s);

extern int errores_lexicos;
extern int yylineno;

int errores_sintacticos = 0;
int error_matematico = 0;
%}

%define parse.error verbose
%locations

%union {
    double valor;
}

%token <valor> NUM
%token NL POTENCIA
%type <valor> expr

/*
   Precedencia y asociatividad:

   %left indica asociatividad de izquierda a derecha.
   Ejemplo: 10 - 5 - 2 se interpreta como (10 - 5) - 2.

   En Bison, las declaraciones que aparecen despues tienen mayor prioridad.
   Por eso '**' tiene mayor prioridad que '*', '/', '%' y que '+' y '-'.
*/
%left '+' '-'          /* menor prioridad, izquierda a derecha */
%left '*' '/' '%'      /* prioridad media, izquierda a derecha */
%right UMINUS          /* signo menos unario: -5 */
%right POTENCIA        /* mayor prioridad, derecha a izquierda: 2**3**2 = 2**(3**2) */

%%

input:
      /* vacio */
    | input linea
    ;

linea:
      expr NL
        {
            /* printf("Linea %d: Sintaxis correcta. Expresion valida encontrada.\n", @1.first_line); */
            if (!error_matematico) {
                printf("Resultado = %.10g\n", $1);
            }
            error_matematico = 0;
        }
    | NL
        {
            /* Ignorar lineas vacias */
        }
    | expr operador NL
        {
            errores_sintacticos++;
            error_matematico = 0;
            fprintf(stderr, "Linea %d: Error sintactico. Expresion incompleta despues del operador.\n", @2.first_line);
        }
    | operador_inicio expr NL
        {
            errores_sintacticos++;
            error_matematico = 0;
            fprintf(stderr, "Linea %d: Error sintactico. La expresion no puede iniciar con ese operador.\n", @1.first_line);
        }
    | error NL
        {
            error_matematico = 0;
            fprintf(stderr, "Linea %d: Recuperacion de error. Se descarto la expresion incorrecta.\n", @1.first_line);
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
                error_matematico = 1;
                fprintf(stderr, "Linea %d: Error matematico. Division por cero.\n", @3.first_line);
                $$ = 0;
            } else {
                $$ = $1 / $3;
            }
        }
    | expr '%' expr
        {
            if ($3 == 0) {
                errores_sintacticos++;
                error_matematico = 1;
                fprintf(stderr, "Linea %d: Error matematico. Modulo por cero.\n", @3.first_line);
                $$ = 0;
            } else {
                $$ = fmod($1, $3);
            }
        }
    | expr POTENCIA expr
        {
            if ($1 == 0 && $3 == 0) {
                errores_sintacticos++;
                error_matematico = 1;
                fprintf(stderr, "Linea %d: Error matematico. Cero elevado a cero no esta definido.\n", @2.first_line);
                $$ = 0;
            } else {
                $$ = pow($1, $3);
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
    | '%'
    | POTENCIA
    ;

operador_inicio:
      '+'
    | '*'
    | '/'
    | '%'
    | POTENCIA
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
    setvbuf(stderr, NULL, _IONBF, 0);

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
