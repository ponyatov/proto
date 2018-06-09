## @file
## @brief zero stage implementation

## @defgroup stage0 Stage 0 
## @brief minimal codegenerator S0 -> S1.py
## @{

import os,sys
## source code
SRC = open(sys.argv[0]+'.src','r').read()

## @defgroup sym Symbolic class system
## @brief <a href="http://ponyatov.quora.com/On-computer-language-design-Symbolic-data-type-system">symbolic in the sense of computer algebra</a>
## @{

## base object class, such named for avoiding Python3 interference with `Object`
class Qbject:
    ## construct as `<type:value>` pair 
    ## **universal object can hold nested elements**
    def __init__(self, V, immed=False):
        ## object type
        self.type = self.__class__.__name__.lower()
        ## single value
        self.value = V
        ## immediate flag
        self.immed = immed
        ## `attr{}`ibutes /associative array/
        self.attr = {}
        ## init `nest[]`
        self.clean()
        
    ## `object[key]` operator: **lookup** in `attr{}`ibutes
    def __getitem__(self,key):
        return self.attr[key]
    ## `container[key]=object` opertor: **store to object** by attribute key 
    def __setitem__(self,key,o):
        self.attr[key] = o ; return self
        
    ## `<<` operator: pushes objects 
    def __lshift__(self,o):
        return self.push(o)
    ## push into `nest[]` treated as stack
    def push(self,o):
        self.nest.append(o) ; return self
    ## pop from `nest[]` as stack
    def pop(self):
        return self.nest.pop()
    ## top element without pop
    def top(self):
        return self.nest[-1]
    ## clean `nest[]`
    def clean(self):
        ## storage for `nest[]`ed elements /ordered/
        self.nest = []
    
    ## `print object` operator
    def __repr__(self):
        return self.dump()
    ## short header-only dump
    ## @returns string `<type:value>` 
    def head(self,prefix=''):
        return '%s<%s:%s> %X' % (prefix, self.type, self.str(), id(self))
    ## get str(self)
    def str(self): return str(self.value)
    ## left pad for treee output
    ## @returns string `'\\n\\t...'`
    def pad(self, N):
        return '\n' + ' ' * 4 * N
    ## infty dump blocker
    dumped = []
    ## full dump in tree form
    ## @returns string 
    def dump(self, depth=0, prefix=''):
        S = self.pad(depth) + self.head(prefix)
        if self in self.dumped: return S + ' ...'
        else:                   self.dumped.append(self)
        for i in self.attr:
            S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    
    ## python code generator
    def py(self): return str(self.value)
    
## @defgroup prim Primitive
## @brief primitive machine-level types
## @{

## primitive machine-level types
class Primitive(Qbject):
    ## all primitive has clue propertiy: it evaluates into itself
    def __call__(self): D << self 

## symbol/atom
class Symbol(Primitive): pass

## number
class Number(Primitive): pass

## integer
class Integer(Number):
    ## construct integer 
    def __init__(self,V): Primitive.__init__(self,int(V))
    ## `+` operator
    def __add__(self,o): return Integer(self.value + o.value)
    
## machine hex
class Hex(Integer): pass
## machine binary
class Bin(Integer): pass

## `'string'`
class String(Primitive):
    ## + operator
    def __add__(self,o): return String(self.value + o.str())

## @}

## @defgroup container Container
## @brief objects targeted for data holding
## @{

## objects targeted for data holding
class Container(Qbject): pass

## variable
class Var(Container): pass

## constant
class Const(Var): pass

## LIFO stack
class Stack(Container): pass

## associative array (Python `{dict}`)
class Map(Container):
    ## `<<` operator specially for VM commands
    def __lshift__(self,fn):
        self.attr[fn.__name__] = VM(fn) ; return self
        
## ordered vector
class Vector(Container):
    ## vector can has empty name
    def __init__(self,V=''): Container.__init__(self, V)
    ## .py code generator
    def py(self):
        S = '['
        for i in self.nest: S += i.py() + ','
        if self.nest: S = S[:-1]
        return S + ']'

## @}

## @defgroup active Active
## @brief objects with executable semantics
## @{

## objects with **executable semantics**
class Active(Qbject): pass

## function
class Function(Active): pass
## **virtual machine command**: `void function(void)` works on data stack
class VM(Function):
    ## wrap given VM command function 
    def __init__(self,fn,immed=False):
        Active.__init__(self, fn.__name__, immed)
        ## wrap file handler
        self.fn = fn
    ## execute VM command
    def __call__(self): self.fn()

## class definition/constructor    
class Clazz(Active): pass
## class method
class Method(Function): pass

## @}

## @defgroup io IO
## @brief reduced support for file writing (for code autogen) 
## @{

## I/O
class IO(Qbject): pass

## File
class File(IO):
    ## create file for write only
    ## @param[in] V file name
    def __init__(self,V):
        IO.__init__(self, V)
        ## wrap file (write only)
        self.fh = open(V,'w')
    ## callable: write top element from stack
    def __call__(self):
        print >>self.fh,D.pop().py()

## Directory
class Dir(IO):
    ## create directory
    def __init__(self,V):
        IO.__init__(self, V)
        self['cwd'] = String(os.getcwd())
        try: os.mkdir(self.value)
        except OSError: pass # exists

## @}

## @}

## @defgroup lexer Syntax parser /lexer only/
## @brief powered by PLY library (c) David Beazley <<dave@dabeaz.com>>
## @{

import ply.lex as lex

## token types list:
## all names must correspond to lowercased literal names in the @ref sym 
tokens = ['symbol','string','integer']

## extra lexer states
states = (('string','exclusive'),)

## ignore chars in `<string>` state
t_string_ignore = ''

## start string token
def t_string(t):
    r'\''
    t.lexer.lexstring = ''
    t.lexer.push_state('string')
## finish string token
def t_string_string(t):
    r'\''
    t.lexer.pop_state()
    return String(t.lexer.lexstring)
## newline in string depricated
def t_string_newline(t):
    r'\n'
    raise SyntaxError(t)
## any char in string
def t_string_char(t):
    r'.'
    t.lexer.lexstring += t.value

## drop spaces
t_ignore = ' \t\r'
## drop comments
t_ignore_COMMENT = r'[\#\\].*\n|\(.*\)'

## increment line number
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## lexer error callback
def t_ANY_error(t): raise SyntaxError(t)

## number parsing
def t_integer(t):
    r'[0-9]+'
    return Integer(t.value)

## symbol /word name/
def t_symbol(t):
    r'[a-zA-Z0-9_\?\.\+\-\*\/\[\]\{\}\~]+'
    return Symbol(t.value)

## lexer
lexer = lex.lex()

## @}

## @defgroup fvm oFORTH Virtual Machine
## @brief FORTH-inspired stack engine based on OOP /no addressable memory/
## @{

## @defgroup voc Vocabulary
## @{

## main vocabulary
W = Map('FORTH')

## @}

## @defgroup stack Data stack and base operators
## @{

## data stack
D = Stack('DATA')

## `+ ( o1 o2 --> o1+o2)` operator
def add(): o2 = D.pop() ; o1 = D.pop() ; D << o1 + o2
W['+'] = VM(add)

## @}

## `BYE ( -- )` stop the whole system
def BYE(): sys.exit(0)
W << BYE 

## @defgroup debug Debug
## @brief minimal debug (stack/vocabulary dump)
## @{

## `? ( -- )` dump data stack
def q(): print D
W['?'] = VM(q,immed=True)

## `?? ( -- )` dump state and exit
def qq(): print W ; print '\nCOMPILE',COMPILE ; q() ; BYE()
W['??'] = VM(qq,immed=True)

## `.` clean data stack (use at end of every code block)
def dot(): D.clean()
W['.'] = VM(dot)

## @}

## @defgroup fileio File I/O
## minimal i/o for target files writing
## @{

W['r/o'] = String('r')
W['w/o'] = String('w')

## `FILE ( name mode -- file )` open file, `mode = r/o w/o r/w`
def FILE(): D << File(D.pop().value)
W << FILE

## @}

## @defgroup meta Meta
## @{

W['STAGE'] = Integer(0)

## @}

## @defgroup compiler Compiler
## @brief @ref Active objects constructor, not machine code
## @{

## `DEF ( object -- )` usage `def NewName` define new vocabulary item for object 
def DEF(): WORD() ; name = D.pop().value ; W[name] = D.pop()
W << DEF

## current definition or [] in interpreter mode
COMPILE = []

## `[` start vector compilation
def lq(): COMPILE.append( Vector() )
W['['] = VM(lq)
## `]` finish vector compilation
def rq(): D << COMPILE.pop() 
W[']'] = VM(rq,immed=True)

## @}

## @defgroup interpret Interpreter
## @brief <b>`o`</b>bject FORTH script
## @{

## `WORD ( -- wordname )` parse next literal from source code
def WORD():
    token = lexer.token()
    if not token: return False
    D << token ; return token ; print token
W << WORD

## `FIND ( wordname -- executable )` lookup in W
def FIND():
    name = D.pop().value
    try: D << W.attr[name]
    except KeyError:
        try: D << W.attr[name.upper()]
        except KeyError: raise KeyError(name)
W << FIND

## `EXECUTE ( executable -- )` execute object from stack
def EXECUTE(): D.pop()()
W << EXECUTE

## `\` ( -- wordname )` quote next syntax item as symbol without lookup
def quote():
    WORD()
    if COMPILE: COMPILE[0] << D.pop()
W['~'] = VM(quote,immed=True)

## `INTERPRET ( -- )` process source code
## @param[in] SRC from string
def INTERPRET(SRC=''):
    lexer.input(SRC)
    while True:
        if not WORD(): break;                   ## end of source
        if D.top().type in ['symbol']: FIND()   ## searchable
        if COMPILE and not D.top().immed:
                COMPILE[0] << D.pop()           ## compilation state
        else:   EXECUTE()                       ## interpretation state
W << INTERPRET
INTERPRET(SRC)

## @}

## @}

## @}
