import sys

## data stack
D = []

# ## syntax parser by PLY (Python Lex-Yacc) @ http://www.dabeaz.com/ply/
# 
# import ply.lex as lex
# 
# ## supported tokens
# tokens = ['WORD','NUMBER']
# 
# ## ignore spaces
# t_ignore = ' \t\r'
# 
# ## line comments can start with # and \
# ## block comments uses ( )
# t_ignore_COMMENT = r'[\#\\].*|\(.*\)'
# 
# ## new line rule increments line counter in lexer
# def t_newline(t):
#     r'\n'
#     t.lexer.lineno += 1
#     
# ## lexer error callback
# def t_error(t):
#     raise SyntaxError(t)
# 
# ## number parser rule
# def t_NUMBER(t):
#     r'[\+\-]?[0-9]+(\.[0-9]*)?'
#     return t
# 
# ## any other non-space groups treated as FORTH word names
# def t_WORD(t):
#     r'[A-Za-z0-9_]+'
#     return t    
# 
# ## single lexer instance
# lexer = lex.lex()

from rply import LexerGenerator

lexer_generator = LexerGenerator()

lexer_generator.add('NUMBER',r'[\+\-]?[0-9]+(\.[0-9]*)?')
lexer_generator.add('WORD',r'[A-Za-z0-9_]+')
lexer_generator.add('SPACE',r'\s+')

lexer = lexer_generator.build()

def WORD(source):
    try: token = stream.next() ; D.append(token) ; return token
    except StopIteration: return None

def INTERPRET(SRC=''):
#     lexer.input(SRC)            # feed lexer with source code
    source = lexer.lex('1 2.3')
    while True:
        if not WORD(source): break    # break on end of source
        print D

def main(argv):
    print argv
    INTERPRET(open(argv[1]).read())
    return 0

def target(*args):
    return main,None

if __name__ == '__main__':
    main(sys.argv)
