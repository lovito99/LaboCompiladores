# Makefile — Laboratorio 5: Conjuntos Primeros y Siguientes
# Curso: IF454AIN - Compiladores
# UNSAAC

PYTHON = python3

.PHONY: run1 run2 test1 test2 test3 test4 test5 test6 test_all clean

# ─── Modo interactivo ────────────────────────────────────────
run1:
	@$(PYTHON) ejercicio1.py

run2:
	@$(PYTHON) ejercicio2.py

# ─── Ejecución con archivos de prueba ────────────────────────
test1:
	@echo "═══ Ejercicio 1 con prueba1.txt ═══"
	@$(PYTHON) ejercicio1.py < prueba1.txt

test2:
	@echo "═══ Ejercicio 1 con prueba2.txt ═══"
	@$(PYTHON) ejercicio1.py < prueba2.txt

test3:
	@echo "═══ Ejercicio 1 con prueba3.txt ═══"
	@$(PYTHON) ejercicio1.py < prueba3.txt

test4:
	@echo "═══ Ejercicio 2 con prueba1.txt ═══"
	@$(PYTHON) ejercicio2.py < prueba1.txt

test5:
	@echo "═══ Ejercicio 2 con prueba2.txt ═══"
	@$(PYTHON) ejercicio2.py < prueba2.txt

test6:
	@echo "═══ Ejercicio 2 con prueba3.txt ═══"
	@$(PYTHON) ejercicio2.py < prueba3.txt

test_all: test1 test2 test3 test4 test5 test6
