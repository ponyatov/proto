
class Qbject: pass

class Primitive(Qbject): pass

class Symbol(Primitive): pass

class Number(Primitive): pass

class String(Primitive): pass

class Container(Qbject): pass

class Stack(Container): pass

class Map(Container): pass

class Active(Qbject): pass

class Function(Active): pass

D = Stack('DATA')

W = Map('FORTH')
