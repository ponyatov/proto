# bare Symbolic type system (Python only, no FORTH bindings)

import re

class Qbject:

    def __init__(self, V):
        self.type = self.__class__.__name__.lower() ; self.value = V

    def __repr__(self):
        return self.dump()

    def dump(self, depth=0, prefix=''):
        S = self.pad(depth) + self.head(prefix)
        return S

    def pad(self, N):
        return '\n' + '\t' * N

    def head(self, prefix=''):
        return '<%s:%s> @%X' % (self.type, self.str(), id(self))
    
    def str(self): return str(self.value)


def test_qbject():
    Q = Qbject('value')
    assert re.match(r'\n<qbject:value> @[0-9A-F]+',Q.dump())

class Primitive(Qbject): pass

class Symbol(Primitive): pass

def test_symbol():
    S = Symbol('symbol')
    assert re.match(r'\n<symbol:symbol> @[0-9A-F]+',S.dump())

class Number(Primitive):
    def __init__(self,N):
        Primitive.__init__(self, float(N))

def test_num_123():
    N = Number(123)
    assert re.match(r'\n<number:123.0> @[0-9A-F]+',N.dump())

class String(Primitive):
    def str(self):
        return '\'%s\'' % self.value

def test_string():
    S = String('string')
    print S
    assert re.match(r'\n<string:\'string\'> @[0-9A-F]+',S.dump())

