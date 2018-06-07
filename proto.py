
import sys
try:                SRC = open(sys.argv[1]).read()
except IndexError:  SRC = open(sys.argv[0]+'.src').read()

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

D = Stack('DATA')

W = Map('FORTH') ; print

def BYE(): sys.exit(0)
W << BYE 

def q(): print D
W['?'] = VM(q)

def qq(): q(); print W ; BYE()
W['??'] = VM(qq)

import ply.lex as lex

lexer = lex.lex()

def INTERPRET(SRC=''):
    lexer.input(SRC)
    while True:
        token = lexer.token()
        
    print 'src',SRC
INTERPRET(SRC)
