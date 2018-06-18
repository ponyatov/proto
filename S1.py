## @file
## @brief prototype knowledge database implementation /stage 1/

## @defgroup stage1 Stage 1
## @brief Autogenerated @ref stage1 in S1.py
## @{

import os,sys,re

## @defgroup s1sym Symbolic class system
## @{

## base object class, such named for avoiding Python3 interference with `Object`
class Qbject:
    ## construct as `<type:value>` pair 
    ## **universal object can hold nested elements**
    def __init__(self,V):
        ## object type
        self.type = self.__class__.__name__.lower()
        ## single value
        self.value = V
        ## `attr{}`ibutes /associative array/
        self.attr = {}
        ## init `nest[]`ed elements /ordered vector/
        self.nest = []
        
    ## `print object` operator
    def __repr__(self): return self.dump()
    ## full dump in tree form
    ## @returns string 
    def dump(self,depth=0,prefix=''):
        S = self.pad(depth) + self.head(prefix)
        for i in self.attr:
            S += self.attr[i].dump(depth+1,prefix='%s = '%i)
        return S
    ## left pad for treee output
    ## @returns string `'\\n\\t...'`
    def pad(self,N): return '\n' + '\t'*N
    ## short header-only dump
    ## @returns string `<type:value>` 
    def head(self,prefix=''): return '%s<%s:%s>' % (prefix,self.type,self.str())
    ## value in string
    def str(self): return self.value
    
    ## `container[key]=object` operator: **store to object** by attribute key 
    def __setitem__(self,key,o): self.attr[key] = o ; return self
    ## `object[key]` operator: **lookup** in `attr{}`ibutes
    def __getitem__(self,key): return self.attr[key]

## @defgroup s1prim Primitive
## @{

class Primitive(Qbject): pass

class Symbol(Primitive): pass

class String(Primitive):
    def str(self):
        S = '\''
        for c in self.value:
            if c == '\n': S += '\\n'
            elif c == '\t': S += '\\t'
            else: S += c
        return S+'\''
        

class Number(Primitive): pass

class Integer(Number): pass

## @}

## @defgroup s1container Container
## @{

class Container(Qbject): pass

class Stack(Container): pass

class Map(Container): pass

## @}

## @defgroup s1active Active
## @{

class Active(Qbject): pass

class Function(Active): pass

class Operator(Qbject): pass

## @}

## @}

## @defgroup s1lexer Syntax parser
## @brief powered with
## <a href="http://ponyatov.quora.com/Text-data-formats-Parsing-with-Python-and-PLY-library">PLY library</a>
## `(c) David M Beazley` 
## @{

import ply.lex  as lex
import ply.yacc as yacc

## @brief token types binded with @ref Qbject
## @details Every Qbject type can be matched by regexp in string form
## will be used as token by PLY library. To do it all Qbjects was done 
## compatible with PLY requirements for token: 
## they must contain predefined set of fields @see PLY manual.
##
## every token type must be equal to lowercased 
## name of correspondent Qbject class
tokens = ['comment','symbol','string','number','hex','bin','operator','const']

states = (('string','exclusive'),)

t_string_ignore = ''

def t_string(t):
    r'\''
    t.lexer.push_state('string')
    t.lexer.lexstring = ''
    t.lexer.posstring = t.lexer.lexpos
def t_string_string(t):
    r'\''
    t.lexer.pop_state()
    t.lexpos = t.lexer.posstring
    t.value = t.lexer.lexstring
    return t
def t_string_any(t):
    r'.'
    t.lexer.lexstring += t.value

t_ignore = ' \t\r\n'

def t_ANY_error(t): raise SyntaxError(t)

def t_comment(t):
    r'[\#\\].*\n|\(.*\)'
    return t

def t_hex(t):
    r'0x[0-9a-fA-F]+'
    t.type = 'number' ; return t
def t_bin(t):
    r'0b[01]+'
    t.type = 'number' ; return t
def t_number(t):
    r'[\+\-]?[0-9]+(\.[0-9]*)?([eE][\+\-][0-9]+)?'
    return t

def t_symbol(t):
    r'[a-zA-Z0-9_\.]+'
    if re.match(r'^[A-Z]+$',t.value): t.type = 'const'
    return t

def t_operator(t):
    r'[\<\>\:\;\=\@\+\-\*\/]'
    return t

lexer = lex.lex()

## @}

## @defgroup s1fvm oFORTH Virtual Machine
## @{

## data stack
D = Stack('DATA')

## vocabulary
W = Map('FORTH')

## @}

## @defgroup s2meta Metainfo
## @{

## short module name
MODULE  = 'proto'
## short info about module (oneliner)
TITLE   = 'prototype knowledge database implementation'
## author
AUTHOR  = 'Dmitry Ponyatov <<dponyatov@gmail.com>>'
## licence info
LICENCE = 'All rights reserved'
## github repo
GITHUB  = 'https://github.com/ponyatov/proto'
## manual
MANUAL  = 'Quora blog: http://www.quora.com/profile/Dmitry-Ponyatov/all_posts'
## autogenerated ABOUT
ABOUT  = '''
# %s
### %s

(c) %s %s

github: %s
manual: %s
'''%(MODULE,TITLE,AUTHOR,LICENCE,GITHUB,MANUAL)

W['MODULE']  = String(MODULE)
W['TITLE']   = String(TITLE)
W['AUTHOR']  = String(AUTHOR)
W['LICENCE'] = String(LICENCE)
W['GITHUB']  = String(GITHUB)
W['MANUAL']  = String(MANUAL)
W['ABOUT']   = String(ABOUT)

W['STAGE']   = Number(re.findall(r'S(\d)\.py$',sys.argv[0])[0])

## @} 

## @defgroup s1gui GUI
## @brief light set of GUI view/controllers and micro/IDE
## @{

import wx, wx.stc

## GUI element
class GUI(Qbject): pass

## window
class Frame(GUI):
    ## construct window
    def __init__(self,V):
        GUI.__init__(self, V)
        ## wrapped wxframe
        self.frame = wx.Frame(None,title=V)
    ## close window event forwarder
    def Close(self): self.frame.Close()

## menu        
class Menu(GUI):
    ## construct menu
    ## @param[in] frame owner frame  
    def __init__(self,frame):
        GUI.__init__(self, frame.value)
        ## menubar
        self.menubar = wx.MenuBar() ; frame.frame.SetMenuBar(self.menubar)
        ## file menu
        self.file = wx.Menu() ; self.menubar.Append(self.file,'&File')
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        self.backup = self.file.Append(wx.ID_APPLY,'&Backup\tCtrl+E')
        ## file/quit
        self.quit = self.file.Append(wx.ID_EXIT,'&Quit')
        ## debug menu
        self.debug = wx.Menu() ; self.menubar.Append(self.debug,'&Debug')
        ## debug/update
        self.update = self.debug.Append(wx.ID_REFRESH,'&Update\tF12')
        ## debug/vocabulary dump window toggle
        self.voc = self.debug.Append(wx.ID_ANY,'&Vocabulary\tF8',kind=wx.ITEM_CHECK)
        ## debug/stack dump window toggle
        self.stack = self.debug.Append(wx.ID_ANY,'&Stack\tF9',kind=wx.ITEM_CHECK)
        ## help menu
        self.help = wx.Menu() ; self.menubar.Append(self.help,'&Help')
        ## help/about
        self.about = self.help.Append(wx.ID_ABOUT,'&About\tF1')
        
## editor widget (Scintilla wrapper)
class Editor(GUI):
    ## @param[in] V file name
    ## @param[in] frame parent Frame instance
    def __init__(self,V,frame):
        GUI.__init__(self, V)
        self['frame'] = Frame(V)
        ## wx.stc.StyledEditor wrapper (Scintilla)
        self.editor = wx.stc.StyledTextCtrl(frame.frame)
        ## set default styling in editor
        self.editor.SetTabWidth(4)
        self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                        'face:%s,size:%s' % (font.FaceName, font.PointSize))
        ## colorizer
        self.initColorizer()
    ## init colorizer
    def initColorizer(self):
        self.style_COMMENT = 1
        self.editor.StyleSetSpec(self.style_COMMENT,'fore:#0000FF')
        self.style_NUMBER = 2
        self.editor.StyleSetSpec(self.style_NUMBER,'fore:#008800')
        self.style_OPERATOR = 3
        self.editor.StyleSetSpec(self.style_OPERATOR,'fore:#AA0000')
        self.style_CONST = 4
        self.editor.StyleSetSpec(self.style_CONST,'fore:#008888')
        self.style_STRING = 5
        self.editor.StyleSetSpec(self.style_STRING,'fore:#888800')
        # bind colorizer event
        self.editor.Bind(wx.stc.EVT_STC_STYLENEEDED,self.onStyle)
    ## styling event callback
    def onStyle(self,event):
        lexer.input(self.editor.GetValue())
        while True:
            token = lexer.token()
            if not token: break
            self.editor.StartStyling(token.lexpos,0xFF)
            if token.type in ['comment']:
                self.editor.SetStyling(len(token.value),self.style_COMMENT)
            elif token.type in ['number']:
                self.editor.SetStyling(len(token.value),self.style_NUMBER)
            elif token.type in ['operator']:
                self.editor.SetStyling(len(token.value),self.style_OPERATOR)
            elif token.type in ['const']:
                self.editor.SetStyling(len(token.value),self.style_CONST)
            elif token.type in ['string']:
                self.editor.SetStyling(len(token.value),self.style_STRING)
    ## set text contents value
    def SetValue(self,value): self.editor.SetValue(value)
    ## get text contents
    def GetValue(self): return self.editor.GetValue()
        
## IDE window (base GUI widget in micro IDE)
class IDE(GUI):
    ## construct editor
    ## @param[in] V with given file name (and title)
    def __init__(self,V):
        GUI.__init__(self, V)
        frame = self['frame'] = Frame(V)
        menu = self['menu'] = Menu(frame)
        ## styled editor
        self['editor'] = Editor(V,frame)
        self.onLoad()
        ## menu/key bindings
        frame.frame.Bind(wx.EVT_MENU,self.onClose,menu.quit)
        frame.frame.Bind(wx.EVT_MENU,self.onSave,menu.save)
        frame.frame.Bind(wx.EVT_MENU,self.onVoc,menu.voc)
        frame.frame.Bind(wx.EVT_MENU,self.onStack,menu.stack)
        frame.frame.Bind(wx.EVT_MENU,self.onUpdate,menu.update)
        frame.frame.Bind(wx.EVT_MENU,lambda e:wx.MessageBox(ABOUT),menu.about)
    ## show frame forwarder        
    def Show(self): self['frame'].frame.Show()
    ## editor visible
    def isVisible(self): return self['frame'].frame.IsShown()
    ## update callback [F12]
    def onUpdate(self,event):
        if   wxVoc.isVisible():   wxVoc['editor'].editor.SetValue(W.dump())
        if wxStack.isVisible(): wxStack['editor'].editor.SetValue(D.dump())
    ## vocabulary window update callback
    def onVoc(self,event):
        F = wxVoc['frame'].frame
        if F.IsShown(): F.Hide()
        else:           F.Show() ; self.onUpdate(event)
    ## stack window update callback
    def onStack(self,event):
        F = wxStack['frame'].frame
        if F.IsShown(): F.Hide()
        else:           F.Show() ; self.onUpdate(event)
    ## close editor
    def Close(self): self['frame'].frame.Close()
    ## event on editor exit
    def onClose(self,event):
        wxMain.Close()
        wxVoc.Close()
        wxStack.Close()
        sys.exit(0)
    ## event on editor start (load file from window title)
    def onLoad(self):
        try: F = open(self.value,'r')
        except IOError: return
        self['editor'].SetValue(F.read()) ; F.close()
    ## event on save callback
    def onSave(self,event):
        F = open(self.value,'w') ; F.write(self['editor'].GetValue()) ; F.close()

## @}

## @}

## wxPython application
wxapp = wx.App()

# large monospace font adopted for screen size
## fetch screen height as base for font scale
displaY = wx.GetDisplaySizeMM()[1]
## fetch available font from system
font = wx.Font(displaY / 0x10,
               wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

## uIDE vocabulary dump
wxVoc   = IDE(sys.argv[0]+'.words')
## uIDE stack dump
wxStack = IDE(sys.argv[0]+'.stack')
## uIDE workpad editor
wxMain  = IDE(sys.argv[0]+'.src') ; wxMain.Show()

wxapp.MainLoop()
