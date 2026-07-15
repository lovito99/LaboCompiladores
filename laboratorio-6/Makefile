CC=gcc
BISON=bison
FLEX=flex
CFLAGS=-Wall -Wextra -g

TARGET=analizador
PARSER=analizador.tab.c
HEADER=analizador.tab.h
LEXER=lexer.yy.c

all: $(TARGET)

$(TARGET): analizador.y lexer.l
	$(BISON) -d analizador.y -o $(PARSER)
	$(FLEX) -o $(LEXER) lexer.l
	$(CC) $(CFLAGS) $(PARSER) $(LEXER) -o $(TARGET)
	rm -f $(PARSER) $(HEADER) $(LEXER)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) $(PARSER) $(HEADER) $(LEXER) analizador.output

.PHONY: all run clean
