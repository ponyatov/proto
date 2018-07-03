import sys

## data stack
D = []

## syntax parser by PLY (Python Lex-Yacc) @ http://www.dabeaz.com/ply/

import ply.lex as lex

## supported tokens
tokens = ['WORD','NUMBER']

## ignore spaces
t_ignore = ' \t\r'

## line comments can start with # and \
## block comments uses ( )
t_ignore_COMMENT = r'[\#\\].*|\(.*\)'

## new line rule increments line counter in lexer
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    
## lexer error callback
def t_error(t):
    raise SyntaxError(t)

## number parser rule
def t_NUMBER(t):
    r'[\+\-]?[0-9]+(\.[0-9]*)?'
    return t

## any other non-space groups treated as FORTH word names
def t_WORD(t):
    r'[A-Za-z0-9_]+'
    return t    

## single lexer instance
lexer = lex.lex()

def WORD():
    token = lexer.token()
    D.append(token)
    return token

def INTERPRET(SRC=''):
    lexer.input(SRC)            # feed lexer with source code
    while True:
        if not WORD(): break    # break on end of source
        print D

def main(argv):
    print argv
    INTERPRET(open(argv[1]).read())
    return 0

def target(*args):
    return main,None

if __name__ == '__main__':
    main(sys.argv)
