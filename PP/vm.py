import sys

## data stack
D = []

## syntax parser by RPLY @ http://rply.readthedocs.io/en/latest/

from rply import LexerGenerator

lexer_generator = LexerGenerator()

lexer_generator.add('NUMBER',r'[\+\-]?[0-9]+(\.[0-9]*)?')
lexer_generator.add('WORD',r'[A-Za-z0-9_]+')
lexer_generator.add('SPACE',r'\s+')

lexer = lexer_generator.build()

def WORD(source):
    try: token = source.next() ; D.append(token) ; return token
    except StopIteration: return None

def INTERPRET(SRC=''):
    source = lexer.lex('1 2.3')         # feed lexer with source code
    while True:
        if not WORD(source): break      # break on end of source
        print D.pop()

def main(argv):
    print argv
    INTERPRET(open(argv[1]).read())
    return 0

def target(*args):
    return main,None

if __name__ == '__main__':
    main(sys.argv)
