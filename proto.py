## @file
## @brief zero stage implementation

import sys
try:                SRC = open(sys.argv[1]).read()
except IndexError:  SRC = open(sys.argv[0]+'.src').read()

## @defgroup sym Symbolic class system
## @brief <a href="http://ponyatov.quora.com/On-computer-language-design-Symbolic-data-type-system">symbolic in the sense of computer algebra</a>
## @{

class Qbject:
    def __init__(self, V):
        self.type = self.__class__.__name__.lower()
        self.value = V
        self.attr = {}
    def __setitem__(self,key,o):
        self.attr[key] = o ; return self
    def __lshift__(self,o):
        self.attr[o.__name__] = VM(o) ; return self
    def __repr__(self):
        return self.dump()
    def head(self,prefix=''):
        return '%s<%s:%s>' % (prefix, self.type, self.value)
    def pad(self, N):
        return '\n' + '\t' * N
    def dump(self, depth=0, prefix=''):
        S = self.pad(depth) + self.head(prefix)
        for i in self.attr:
            S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        return S

class Primitive(Qbject): pass

class Symbol(Primitive): pass

class Number(Primitive): pass

class String(Primitive): pass

class Container(Qbject): pass

class Stack(Container): pass

class Map(Container): pass

class Active(Qbject): pass

class VM(Active): pass

class Meta(Qbject): pass

class Module(Meta): pass

class Clazz(Meta): pass

## @}

## @defgroup lexer Syntax parser /lexer only/
## @brief powered by PLY library (c) David Beazley <<dave@dabeaz.com>>
## @{

import ply.lex as lex

## token types list:
## all names must correspond to lowercased literal names in the @ref sym 
tokens = ['symbol']

## drop spaces
t_ignore = ' \t\r'
## drop comments
t_ignore_COMMENT = r'[\#\\].*\n|\(.*\)'

## increment line number
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## lexer error callback
def t_error(t): raise SyntaxError(t)

## symbol /word name/
def t_symbol(t):
    r'[a-zA-Z0-9_\?]+'
    t.value = Symbol(t.value) ; return t

## lexer
lexer = lex.lex()

## @}

## @defgroup fvm oFORTH Virtual Machine
## @brief FORTH-inspired stack engine based on OOP /no addressable memory/
## @{

D = Stack('DATA')

W = Map('FORTH') ; print

def BYE(): sys.exit(0)
W << BYE 

def q(): print D
W['?'] = VM(q)

def qq(): q(); print W ; BYE()
W['??'] = VM(qq)

## @defgroup compiler Compiler
## @brief @ref Active objects constructor, not machine code
## @{

## current definition or None in interpreter mode
COMPILE = None

## @}

## @defgroup interpret Interpreter
## @brief <b>`o`</b>bject FORTH script
## @{

def INTERPRET(SRC=''):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        if not token: break
        print token
INTERPRET(SRC)

## @}

## @}