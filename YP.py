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
    
def generalGetValue(value):
    if not isinstance(value, UniVar): return value  ## non-var
    if not value._bound: return value               ## unbound var
    return value._value                             ## bounded value

def generalUnify(arg1, arg2):
    arg1val = generalGetValue(arg1)
    arg2val = generalGetValue(arg2)
    if isinstance(arg1val,UniVar):                  ## unbound arg1val
        for i in arg1val << arg2val: yield i        ##   unify with arg2val
    elif isinstance(arg2val, UniVar):               ## unbound arg2val
        for j in arg2val << arg1val: yield j        ##   unify with arg1val
    else:                                           ## both non-univars
        if arg1val == arg2val: yield arg1val        ##   

P = UniVar() ; print generalGetValue(P)
for i in P << 'Beta':
    print generalGetValue(i)
print generalGetValue(123)
