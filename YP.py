# http://yieldprolog.sourceforge.net/tutorial1.html

class Var:
    def __init__(self): self._value = None
    def __lshift__(self,val): self._value = val
    def __repr__(self):
        if self._value: return '<%s>' % self._value
        else: return str(self._value)

def Persons(P):
    P << 'Alpha' ; yield P
    P << 'Beta'  ; yield P
    P << 'Gamma' ; yield P

P = Var() ; print P
for p in Persons(P):
    print p