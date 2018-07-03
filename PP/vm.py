import sys

## data stack
D = []

## syntax parser by RPLY @ http://rply.readthedocs.io/en/latest/
from rply import LexerGenerator

## generator will build lexer in runtime
lexer_generator = LexerGenerator()

## drop comments
lexer_generator.ignore(r'[\\\#].*|\(.*\)')
## drop spaces
lexer_generator.ignore(r'\s+')
## number parsing
lexer_generator.add('HEX','0x[0-9A-Fa-f]+')
lexer_generator.add('BIN','0b[01]+')
lexer_generator.add('NUMBER',r'[\+\-]?[0-9]+(\.[0-9]*)?')
## FORTH word names
lexer_generator.add('WORD',r'[A-Za-z0-9_]+')

## build resulting lexer
lexer = lexer_generator.build()

## parse next token from
## @param[in] source stream
def WORD(source):
    try: token = source.next() ; D.append(token) ; return token
    except StopIteration: return None

## REPL loop
def INTERPRET(SRC=''):
    source = lexer.lex(SRC)         # feed lexer with source code
    while True:
        if not WORD(source): break  # break on end of source
        print D.pop()

def main(argv):
    print argv
    INTERPRET(open(argv[1]).read())
    return 0

def target(*args):
    return main,None

if __name__ == '__main__':
    main(sys.argv)
