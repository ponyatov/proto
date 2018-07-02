# http://yieldprolog.sourceforge.net/tutorial1.html

class UniVar:
    def __init__(self):
        self._value = None
        self._bound = False
    def __lshift__(self,val):
        return self.unify(val)
    def unify(self,arg):
        if not self._bound:
            self._value = arg ; self._bound = True
            yield self
            # drop binding on continue from here
            self._value = None ; self._bound = False
        elif self._value == arg:
            # elso yield if bound to the same value
            yield self
    def __repr__(self):
        if self._bound: return '<%s>' % self._value
        else: return str(self._value)

def Persons(P):
    for i in P << 'Alpha': yield i
    for i in P << 'Beta' : yield i
    for i in P << 'Gamma': yield i

P = UniVar() ; print P
for p in Persons(P):
    print p