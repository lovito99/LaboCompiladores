all: ejercicio1 ejercicio2 ejercicio3

ejercicio1: ejercicio1.l
	flex ejercicio1.l
	gcc lex.yy.c -o ejercicio1
	rm -f lex.yy.c

ejercicio2: ejercicio2.l
	flex ejercicio2.l
	gcc lex.yy.c -o ejercicio2
	rm -f lex.yy.c

ejercicio3: ejercicio3.l
	flex ejercicio3.l
	gcc lex.yy.c -o ejercicio3
	rm -f lex.yy.c

run1: ejercicio1
	./ejercicio1 prueba1.txt

run2: ejercicio2
	./ejercicio2 prueba2.txt

run3: ejercicio3
	./ejercicio3 prueba3.txt

clean:
	rm -f ejercicio1 ejercicio2 ejercicio3

.PHONY: all run1 run2 run3 clean
