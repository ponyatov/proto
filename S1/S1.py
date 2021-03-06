
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

## @}

## @}

