all: ejercicio1 ejercicio2 ejercicio3

# ─── Ejercicio 1: Fracciones N/N ─────────────────────────────────────────────
ejercicio1: ejercicio1.l ejercicio1.y
	bison -d ejercicio1.y -o ejercicio1.tab.c
	flex -o ejercicio1.lex.c ejercicio1.l
	gcc ejercicio1.tab.c ejercicio1.lex.c -o ejercicio1
	rm -f ejercicio1.tab.c ejercicio1.tab.h ejercicio1.lex.c

# ─── Ejercicio 2: Expresiones Aritméticas ─────────────────────────────────────
ejercicio2: ejercicio2.l ejercicio2.y
	bison -d ejercicio2.y -o ejercicio2.tab.c
	flex -o ejercicio2.lex.c ejercicio2.l
	gcc ejercicio2.tab.c ejercicio2.lex.c -o ejercicio2
	rm -f ejercicio2.tab.c ejercicio2.tab.h ejercicio2.lex.c

# ─── Ejercicio 3: Sentencias de Asignación ────────────────────────────────────
ejercicio3: ejercicio3.l ejercicio3.y
	bison -d ejercicio3.y -o ejercicio3.tab.c
	flex -o ejercicio3.lex.c ejercicio3.l
	gcc ejercicio3.tab.c ejercicio3.lex.c -o ejercicio3
	rm -f ejercicio3.tab.c ejercicio3.tab.h ejercicio3.lex.c

# ─── Ejecutar con archivos de prueba ─────────────────────────────────────────
run1: ejercicio1
	./ejercicio1 < prueba1.txt

run2: ejercicio2
	./ejercicio2 < prueba2.txt

run3: ejercicio3
	./ejercicio3 < prueba3.txt

# ─── Limpieza ─────────────────────────────────────────────────────────────────
clean:
	rm -f ejercicio1 ejercicio2 ejercicio3
	rm -f *.tab.c *.tab.h *.lex.c lex.yy.c

.PHONY: all run1 run2 run3 clean
