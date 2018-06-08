## @file
## @brief zero stage implementation

import os,sys
## source code
try:                SRC = open(sys.argv[1]).read()
except IndexError:  SRC = open(sys.argv[0]+'.src').read()

## @defgroup sym Symbolic class system
## @brief <a href="http://ponyatov.quora.com/On-computer-language-design-Symbolic-data-type-system">symbolic in the sense of computer algebra</a>
## @{

## base object class, such named for avoiding Python3 interference with `Object`
class Qbject:
    ## construct as `<type:value>` pair 
    ## **universal object can hold nested elements**
    def __init__(self, V):
        ## object type
        self.type = self.__class__.__name__.lower()
        ## single value
        self.value = V
        ## `attr{}`ibutes /associative array/
        self.attr = {}
        ## init `nest[]`
        self.clean()
    ## clean `nest[]`
    def clean(self):
        ## storage for `nest[]`ed elements /ordered/
        self.nest = []
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
    ## `print object` operator
    def __repr__(self):
        return self.dump()
    ## short header-only dump
    ## @returns string `<type:value>` 
    def head(self,prefix=''):
        return '%s<%s:%s> %X' % (prefix, self.type, self.value, id(self))
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

## `'string'`
class String(Primitive): pass

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
class Vector(Container): pass

## @}

## @defgroup active Active
## @brief objects with executable semantics
## @{

## objects with **executable semantics**
class Active(Qbject): pass

## **virtual machine command**: `void function(void)` works on data stack
class VM(Active):
    ## wrap given VM command function 
    def __init__(self,fn):
        Active.__init__(self, fn.__name__)
        ## wrap file handler
        self.fn = fn
    ## execute VM command
    def __call__(self): self.fn()

## @}

## @defgroup fileio File I/O
## @brief reduced support for file writing (for code autogen) 
## @{

## I/O
class IO(Qbject): pass

## File
class File(IO):
    ## open/create file
    ## @param[in] mode r/w
    ## @param[in] V file name
    def __init__(self,V, mode):
        IO.__init__(self, V)
        self['mode'] = String(mode)
        ## wrap file
        self.fh = open(V,mode)

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
tokens = ['symbol']

## drop spaces
t_ignore = ' \t\r'
## drop comments
t_ignore_COMMENT = r'[\#\\].*\n|\(.*\)'

## increment line number
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## lexer error callback
def t_error(t): raise SyntaxError(t)

## symbol /word name/
def t_symbol(t):
    r'[a-zA-Z0-9_\?\`\.\+\-\*\/]+'
    return Symbol(t.value)

## lexer
lexer = lex.lex()

## @}

## @defgroup fvm oFORTH Virtual Machine
## @brief FORTH-inspired stack engine based on OOP /no addressable memory/
## @{

## data stack
D = Stack('DATA')

## main vocabulary
W = Map('FORTH')

## `BYE ( -- )` stop the whole system
def BYE(): sys.exit(0)
W << BYE 

## @defgroup debug Debug
## @brief minimal debug (stack/vocabulary dump)
## @{

## `? ( -- )` dump data stack
def q(): print D
W['?'] = VM(q)

## `?? ( -- )` dump state and exit
def qq(): q(); print W ; BYE()
W['??'] = VM(qq)

## `.` clean data stack (use at end of every code block)
def dot(): D.clean()
W['.'] = VM(dot)

## @}

## @defgroup io File I/O
## minimal i/o for target files writing
## @{

W['r/o'] = String('r')
W['w/o'] = String('w')

## `FILE ( name mode -- file )` open file, `mode = r/o w/o r/w`
def FILE():
    mode = D.pop().value ; name = D.pop().value
    D << File(name,mode)
W << FILE

## @}

## @defgroup compiler Compiler
## @brief @ref Active objects constructor, not machine code
## @{

## `DEF ( object -- )` usage `def NewName` define new vocabulary item for object 
def DEF(): WORD() ; name = D.pop().value ; W[name] = D.pop()
W << DEF

## current definition or None in interpreter mode
COMPILE = None

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
        except KeyError: raise SyntaxError(name)
W << FIND

## `EXECUTE ( executable -- )` execute object from stack
def EXECUTE(): D.pop()()
W << EXECUTE

## `\` ( -- wordname )` quote next syntax item as symbol without lookup
def quote(): WORD()
W['`'] = VM(quote)

## `INTERPRET ( -- )` process source code
## @param[in] SRC from string
def INTERPRET(SRC=''):
    lexer.input(SRC)
    while True:
        if not WORD(): break;   ## end of source
        FIND()
        EXECUTE()
W << INTERPRET

INTERPRET(SRC)

## @}

## @}
