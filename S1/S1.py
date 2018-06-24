
## @defgroup prim Primitive
## @brief primitive computer types (evaluates to itself)
## @{

## primitive machine-level types
class Primitive(Qbject): pass

## symbol/atom
class Symbol(Primitive): pass

## string 
class String(Primitive):
    ## linear `string` representation with escapes
    def str(self):
        S = '\''
        for c in self.value:
            if c == '\n': S += '\\n'
            elif c == '\t': S += '\\t'
            else: S += c
        return S + '\''

## number
class Number(Primitive):
    ## construct with `float:value`
    def __init__(self,V,token=None):
        Primitive.__init__(self, V, token)
        ## convert with `float()`
        self.value = float(V)

## integer
class Integer(Number):
    ## construct with `int:value`
    def __init__(self,V,token=None):
        Primitive.__init__(self, V, token)
        ## convert with `int()`
        self.value = int(V)

## machine hex
class Hex(Integer):
    ## override with `int(base=16)`
    def __init__(self,V,token=None):
        Primitive.__init__(self, V, token)
        ## convert with `base=16`
        self.value = int(V[2:],0x10)
    ## hex number print
    ## @returns string value in `0x[0-9A-F]+` form
    def str(self): return '0x%X' % self.value

## machine binary
class Binary(Integer):
    ## override with `int(base=2)`
    def __init__(self,V,token=None):
        Primitive.__init__(self, V, token)
        ## convert with `base=2`
        self.value = int(V[2:],0x02)
    ## binary number print
    ## @returns string value in `0b[01]+` form
    def str(self): return '0b{0:b}'.format(self.value)

## @}


## @defgroup container Container
## @brief Objects targeted for data holding: can contain nested data elements
## @{

## data container
class Container(Qbject):
    ## drop all elements
    def dropall(self): del self.nest[:]

## LIFO stack
class Stack(Container): pass

## ordered vector (list)
class Vector(Container): pass

## associative array (vocabulary)
class Map(Container):
    ## `<<` operator
    def __lshift__(self,o):
        self.attr[o.__name__] = VM(o)
        return self
    ## @return keys
    def keys(self): return self.attr.keys()

## @}


## @defgroup active Active
## @brief Objects has executable semantics
## @{
 
## Objects has executable semantics
class Active(Qbject): pass

## function
class Function(Active):
    ## wraps Python function
    ## @param[in] F function will be wrapped
    ## @param[in] immed immediate function will be executed in COMPILE mode
    ## @param[in] doc docstring
    def __init__(self, F, immed=False, doc=''):
        Active.__init__(self, F.__name__, doc=doc)
        ## wrap function
        self.fn = F
        ## immediate flag
        self.immed = immed
    ## implement callable via wrapped function call
    def __call__(self): return self.fn()

## Virtual Machine command
class VM(Function): pass

## colon definition (executable vector)
class ColonDef(Active):
    ## @warning inherited via `__init__` from `Vector` (mixin alike)
    ## @param[in] V definition FORTH word name 
    ## @param[in] immed immediate flag can be set @see Function
    def __init__(self, V, immed=False):
        Active.__init__(self,V)
        ## override `immed` flag
        self.immed = immed
    ## @todo execute colondef
    def __call__(self): raise BaseException(self)

## @}


## @defgroup meta Meta
## @brief Metaprogramming types and objects
## @{
         
## metaprogramming
class Meta(Qbject): pass

## comment
class Comment(Meta,String):
    ## dump head in linear string format
    def str(self): return String.str(self)

## operator
class Operator(Meta): pass

## definition operator (compiler words)
## shuld have different colorizing in editor
class DefOperator(Operator): pass

## @}


## @defgroup io IO
## @brief Filesystem and Network interfacing 
## @{

## @}


## @}


## @defgroup fvm oFORTH Virtual Machine
## @brief FORTH-inspired stack engine based on OOP /no addressable memory/
## @{

## data stack
D = Stack('DATA')

## @defgroup voc Vocabulary
## @{

## vocabulary
W = Map('FORTH')

## @defgroup persist persistent storage
## @brief store system state in `.image` file
## @{ 
 
import pickle
 
## image file name
IMAGE = sys.argv[0] + '.image'
W['IMAGE'] = String(IMAGE)

## backup vocabulary to `.image`
def BACKUP():
    # filter vocabulary ignoring all functions (VM commands) 
    B = {}
    for i in W.keys():
        if W[i].type not in ['vm','function']: B[i] = W[i]
    F = open(IMAGE,'wb') ; pickle.dump(B,F) ; F.close()
W << BACKUP

## restore from vocabulary  `.image`
def RESTORE():
    global W
    try: F = open(IMAGE,'rb') ; B = pickle.load(F) ; F.close()
    except IOError: B = {}
    # override all elements from loaded image
    for i in B: W[i] = B[i]
W << RESTORE

## @}
## @}

## @defgroup s1lexer Syntax parser
## @brief powered with
## <a href="http://ponyatov.quora.com/Text-data-formats-Parsing-with-Python-and-PLY-library">PLY library</a>
## `(c) David M Beazley` 
## @{

import ply.lex  as lex
import ply.yacc as yacc

## @}

## @}

W['MODULE']  = String(MODULE)
W['TITLE']   = String(TITLE)
W['ABOUT']   = String(ABOUT)
W['AUTHOR']  = String(AUTHOR)
W['LICENCE'] = String(LICENCE)
W['GITHUB']  = String(GITHUB)
W['MANUAL']  = String(MANUAL)
W['README']  = String(README)

W['STAGE']   = Number(re.findall(r'S(\d)\.py$',sys.argv[0])[0])

## @}


print W
