# http://yieldprolog.sourceforge.net/tutorial1.html

def Persons():
    yield 'Alpha'
    yield 'Beta'
    yield 'Gamma'

for p in Persons():
    print p