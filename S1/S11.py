
## @brief token types binded with @ref Qbject
## @details Every Qbject type can be matched by regexp in string form
## will be used as token by PLY library. To do it all Qbjects was done 
## compatible with PLY requirements for token: 
## they must contain predefined set of fields @see PLY manual.
##
## every token type must be equal to lowercased 
## name of correspondent Qbject class

tokens = ['comment','symbol','number','num','exp','int','hex','bin',
          'operator','defoperator','string','const']

## lexer states: extra `string` mode
states = (('string','exclusive'),)

## don't ignore anything in string
t_string_ignore = ''

## string lexer rule: start `string` mode 
def t_string(t):
    r'\''
    t.lexer.push_state('string')
    t.lexer.lexstring = ''
    t.lexer.posstring = t.lexer.lexpos
## string lexer rule: stop `string` mode 
def t_string_string(t):
    r'\''
    t.lexer.pop_state()
    t.value  = t.lexer.lexstring
    t.lexpos = t.lexer.posstring + len(t.value)
    return String(t.value,token=t)
## any character
def t_string_char(t):
    r'.'
    t.lexer.lexstring += t.value

## drop spaces
t_ignore = ' \t\r\n'

## lexer error callback
def t_ANY_error(t): raise SyntaxError(t)

## comment lexer rule
def t_comment(t):
    r'[\\\#].*\n|\(.*?\)'
    t.lexpos = t.lexer.lexpos
    return Comment(t.value.replace('\n',''),token=t)

## hex number
def t_hex(t):
    r'0x[0-9a-fA-f]+'
    t.lexpos = t.lexer.lexpos
    return Number(t.value,token=t)

## binary number
def t_bin(t):
    r'0b[01]+'
    t.lexpos = t.lexer.lexpos
    return Number(t.value,token=t)

## number
def t_number(t):
    r'[\+\-]?[0-9]+\.[0-9]*([eE][\+\-]?[0-9]+)?'
    t.lexpos = t.lexer.lexpos
    return Number(t.value,token=t)

## exponential number variant
def t_exp(t):
    r'[\+\-]?[0-9]+([eE][\+\-]?[0-9]+)?'
    t.lexpos = t.lexer.lexpos
    return Number(t.value,token=t)

## integer
def t_int(t):
    r'[\+\-]?[0-9]+'
    t.lexpos = t.lexer.lexpos
    return Number(t.value,token=t)

## definition operator
def t_defoperator(t):
    r'[\:\;]'
    t.lexpos = t.lexer.lexpos
    return DefOperator(t.value,token=t)

## operator
def t_operator(t):
    r'[\<\>\+\-\*\/\=\@\!]'
    t.lexpos = t.lexer.lexpos
    return Operator(t.value,token=t)

## symbol: word name
def t_symbol(t):
    r'[a-zA-Z0-9_]+'
    t.lexpos = t.lexer.lexpos
    return Symbol(t.value,token=t)

## lexer
lexer = lex.lex()

## @}

## @defgroup s1fqueue Interpreter Queue
## @brief Interface between oFORTH and GUI/network query services
## @{
import Queue,threading

## oFORTH/GUI interpreter interface queue
Q = Queue.Queue()

## REPL interpreter loop
def INTERPRET(SRC=''):
    L = lex.lex() ; L.input(SRC)        ## feed lexer
    while True:
        token = L.token()
        if not token: break     ## end of source
        print token
        
## interpreter query processing thread class
class th_INTERPRET(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop = False
    def run(self):
        while not self.stop:
            try: INTERPRET(Q.get(timeout=1))
            except Queue.Empty: pass
## oFORTH thread
forth = th_INTERPRET()

## @}

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
        ## file/save
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        ## file/backup (vocabulary)
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
        ## comment style
        self.style_COMMENT = 1
        self.editor.StyleSetSpec(self.style_COMMENT,'fore:grey')
        ## number style
        self.style_NUMBER = 2
        self.editor.StyleSetSpec(self.style_NUMBER,'fore:darkgreen')
        ## defoperator
        self.style_DEFOP = 3
        self.editor.StyleSetSpec(self.style_DEFOP,'fore:red')
        ## operator
        self.style_OP = 4
        self.editor.StyleSetSpec(self.style_OP,'fore:darkcyan')
        ## string literal
        self.style_STRING = 5
        self.editor.StyleSetSpec(self.style_STRING,'fore:darkblue')
        ## constant literal
        self.style_CONST = 6
        self.editor.StyleSetSpec(self.style_CONST,'fore:brown')
        # bind colorizer event
        self.editor.Bind(wx.stc.EVT_STC_STYLENEEDED,self.onStyle)
    ## colorizer styling event callback
    def onStyle(self,e):
        lexer.input(self.editor.GetValue())
        while True:
            token = lexer.token()
            if not token: break                             # end of source
            self.editor.StartStyling(token.lexpos, 0xFF)
            if token.type == 'comment':
                self.editor.SetStyling(token.lexlen,self.style_COMMENT)
            elif token.type == 'number':
                self.editor.SetStyling(token.lexlen,self.style_NUMBER)
            elif token.type == 'string':
                self.editor.SetStyling(token.lexlen,self.style_STRING)
            elif token.type == 'operator':
                self.editor.SetStyling(token.lexlen,self.style_OP)
            elif token.type == 'defoperator':
                self.editor.SetStyling(token.lexlen,self.style_DEFOP)
            elif token.type == 'symbol' and re.match(r'[A-Z]+',token.value):
                self.editor.SetStyling(token.lexlen,self.style_CONST)
            else:
                self.editor.SetStyling(0,0)
    ## set text contents value
    def SetValue(self,value): self.editor.SetValue(value)
    ## get text value from wrapped wx.stc
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
        frame.frame.Bind(wx.EVT_MENU,self.onSave,menu.save)
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
        wxMain['frame'].Close()
        wxVoc['frame'].Close() ; wxStack['frame'].Close()
        sys.exit(0)
    ## save file
    def onSave(self,event):
        F = open(self.value,'w')
        F.write(self['editor'].GetValue())
        F.close()
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

## GUI thread class
class th_GUI(threading.Thread):
    def run(self):
        wxapp.MainLoop()
## GUI thread
gui = th_GUI()

forth.start()
gui.start()
gui.join()
forth.stop = True ; forth.join()
