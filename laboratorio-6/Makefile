CC=gcc
BISON=bison
FLEX=flex
CFLAGS=-Wall -Wextra -g

TARGET=analizador
PARSER=analizador.tab.c
HEADER=analizador.tab.h
LEXER=lexer.yy.c
TABLE=analizador.output

all: $(TARGET)

$(TARGET): analizador.y lexer.l
	$(BISON) -d -v analizador.y -o $(PARSER)
	$(FLEX) -o $(LEXER) lexer.l
	$(CC) $(CFLAGS) $(PARSER) $(LEXER) -o $(TARGET)
	rm -f $(PARSER) $(HEADER) $(LEXER)

tabla: analizador.y
	$(BISON) -d -v analizador.y -o $(PARSER)
	rm -f $(PARSER) $(HEADER)
	@echo "Tabla LR generada en $(TABLE)"

run: $(TARGET)
	./$(TARGET) < prueba1.txt

test1: $(TARGET)
	./$(TARGET) < prueba1.txt

test2: $(TARGET)
	./$(TARGET) < prueba2.txt

test3: $(TARGET)
	@./$(TARGET) < prueba3.txt || true

test_all: test1 test2 test3 tabla

clean:
	rm -f $(TARGET) $(PARSER) $(HEADER) $(LEXER) $(TABLE)

.PHONY: all tabla run test1 test2 test3 test_all clean
