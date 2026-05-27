all:
	@echo "Uso:"
	@echo "  make run1   → Ejercicio 1: Detector de ambigüedad"
	@echo "  make run2   → Ejercicio 2: Eliminación de ambigüedad"
	@echo "  make run3   → Ejercicio 3: Detector de recursión izquierda"
	@echo "  make run4   → Ejercicio 4: Eliminación de recursión izquierda"
	@echo ""
	@echo "  make test1  → Ejecutar ejercicio 1 con prueba1.txt"
	@echo "  make test2  → Ejecutar ejercicio 2 con prueba2.txt"
	@echo "  make test3  → Ejecutar ejercicio 3 con prueba3.txt"
	@echo "  make test4  → Ejecutar ejercicio 4 con prueba4.txt"

run1:
	python3 ejercicio1.py

run2:
	python3 ejercicio2.py

run3:
	python3 ejercicio3.py

run4:
	python3 ejercicio4.py

test1:
	python3 ejercicio1.py < prueba1.txt

test2:
	python3 ejercicio2.py < prueba2.txt

test3:
	python3 ejercicio3.py < prueba3.txt

test4:
	python3 ejercicio4.py < prueba4.txt

test_all: test1 test2 test3 test4

.PHONY: all run1 run2 run3 run4 test1 test2 test3 test4 test_all
