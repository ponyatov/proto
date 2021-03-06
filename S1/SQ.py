 
## @defgroup forth oFORTH
## @brief object FORTH interpreter
## @{
 
## @defgroup parser Syntax parser
## @brief powered with
## <a href="http://www.dabeaz.com/ply/ply.html">PLY library</a>
## @details (c) David M. Beazley 
## @{
 
import ply.lex  as lex
import ply.yacc as yacc
 
## token types binded with @ref qbject
## @details Every Qbject type can be matched by regexp in string form
## will be used as token by PLY library. To do it all Qbjects was done 
## compatible with PLY requirements for token: 
## they must contain predefined set of fields @see PLY manual.
##
## every token type must be equal to lowercased 
## name of correspondent Qbject class
tokens = ['comment','operator','defoperator','symbol','string',
          'number','integer','hex','binary']
 
## drop spaces
t_ignore = ' \t\r'
 
## @defgroup stringlex String lexer state
## @brief Special lexer state for string parsing with `\t\r\n..` control chars
## @{
 
## extra lexer states
states = (('string','exclusive'),)
 
## ignore in `<string>` state
t_string_ignore = ''
## begin `<string>` state
def t_string(t):
    r'\''
    t.lexer.push_state('string')    # push to <string> lexer mode
    t.lexer.lexstring = ''          # prepare empty string value collector
    t.lexer.posstring = t.lexpos    # save position for editor colorizer
    t.lexer.toklen = 1              # collect original lexeme length in editor
## end `<string>` state
def t_string_string(t):
    r'\''
    t.lexer.pop_state()             # return from <string> lexer mode
    t.value = t.lexer.lexstring     # use collected string value
    t.lexpos = t.lexer.posstring    # use saved postion (first char in editor)
    t.toklen = t.lexer.toklen+1     # use lexeme length (with \n as 2 chars)
    return String(t.value, token=t) # return resulting string token
## `\t`abulation
def t_string_tab(t):
    r'\\t'
    t.lexer.lexstring += '\t' ; t.lexer.toklen += len(t.value)    
## carriage `\r`eturn    
def t_string_cr(t):
    r'\\r'
    t.lexer.lexstring += '\r' ; t.lexer.toklen += len(t.value)
## line feed `\n`    
def t_string_lf(t):
    r'\\n'
    t.lexer.lexstring += '\n' ; t.lexer.toklen += len(t.value)
## any other char in `<string>` mode 
def t_string_char(t):
    r'.'
    t.lexer.lexstring += t.value ; t.lexer.toklen += len(t.value)
     
## @}
 
## line counter
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
 
## comment lexeme
def t_comment(t):
    r'[\#\\].*\n|\(.*?\)'
    return Comment(t.value, token=t)
 
## hex
def t_hex(t):
    r'0x[0-9A-Fa-f]+'
    return Hex(t.value, token=t)
 
## binary
def t_binary(t):
    r'0b[01]+'
    return Binary(t.value, token=t)
 
## number
def t_number(t):
    r'[\+\-]?[0-9]+\.([0-9]*)?([eE][\+\-]?[0-9]+)?'
    return Number(t.value, token=t)
 
## integer
def t_integer(t):
    r'[\+\-]?[0-9]+'
    return Integer(t.value, token=t)
 
## operator
def t_operator(t):
    r'[\(\)\<\>\@\.\+\-\*\/\`]'
    return Operator(t.value, token=t)
 
## compiler words
def t_defopeator(t):
    r'[\[\]\,\:\;\=]'
    return DefOperator(t.value, token=t)
 
## symbol
def t_symbol(t):
    r'[a-zA-Z0-9_]+'
    return Symbol(t.value, token=t)
 
## required lexer error callback 
def t_ANY_error(t): raise SyntaxError(t)
 
## FORTH lexer
## @todo use stack to allow `.inc` directive
lexer = lex.lex()
 
## @}
 
## @defgroup stack Data stack
## @brief `and` stack operations
## @{
 
## data stack
D = Stack('DATA')
 
## @}
 
## @defgroup voc Vocabulary
## @brief System-wide bindings between symbols (word names) and (executable) objects
## @{
 
## system vocabulary
 
W = Voc('FORTH')
# try: W = restore('FORTH')
# except IOError:
#     W = Voc('FORTH')
#     W << WORD << FIND << INTERPRET
#     W['.'] = Function(dot)
#     backup(W)
 
## @}
 
## @defgroup debug Debug
## @{
 
## @brief `. ( .. -- ) ` clean interpreter state in every code logic block `= DROPALL` 
## @details drop data stack
def dot(): D.dropall()
W['.'] = Function(dot,doc=' . ( ... -- ) cleanup at end of code block ')
 
## @}
 
## @defgroup interpret Interpreter
## @{
 
## `WORD ( -- symbol )` parse next word name
def WORD():
    while True:
        token = lexer.token()                   # parse next lexeme
        if not token: return None               # end of source
        if token.type == 'comment': continue    # skip comments
        D << token ; return token               # found good token
W << WORD
 
## `FIND ( wordname -- callable )` lookup definition/callable object in vocabulary
def FIND():
    WN = D.pop().value ; D << W[WN]
W << FIND
     
## `EXECUTE ( callable|primitive -- ...|primitive )` execute callable
def EXECUTE(): D.pop()()
W << EXECUTE
 
## `\` ( -- )` put next symbol literally without lookup in vocabulary
## (like :atom prefix in Elixir)
def tick(): WORD() 
W['`'] = Function(tick,immed=True,
                  doc=' ` (--) quote: put next symbol literally ')
 
## `INTERPRET ( -- )` interpreter loop
def INTERPRET(SRC=''):
    lexer.input(SRC)
    while True:
        if not WORD(): break            # end of source: break interpreter loop
        if D.top().type in ['symbol','operator','defoperator']:
            FIND()
        if not COMPILE or D.top().immed:# interpreter mode or immed object
            EXECUTE()
        else: COMPILE << D.pop()        # compiler mode
    main.onRefresh(None)
W << INTERPRET
 
## @}
 
## @defgroup compiler Compiler
## @brief compiles definitnios into internal representation, not machine code 
## @{
 
## Vm register contains current definition or None in tnterpreter mode
COMPILE = None
 
## `: ( -- )` begin colon definition
def colon():
    global COMPILE
    WORD() ; WN = D.pop().value
    W[WN] = COMPILE = ColonDef(WN)
W[':'] = Function(colon)
 
## `; ( -- )` end colon definition
def semicolon(): global COMPILE ; COMPILE = None
W[';'] = Function(semicolon,immed=True)
 
## `nop ( -- )` no nothing (test function for compiler)
def nop(): pass
W << nop
 
## @}
 
## @defgroup queue IDE/FORTH queue
## @brief queue holds requests to FORTH interpreter
## @{
 
import threading,Queue
 
## queue holds requests to FORTH interpreter
Q = Queue.Queue()
 
## request processing thread
class FORTH_thread(threading.Thread):
    ## expand with `stop` flag
    def __init__(self):
        threading.Thread.__init__(self)
        ## thread stop flag
        self.stop = False
    ## loop processing
    def run(self):
        global COMPILE
        while not self.stop:
            try: INTERPRET(Q.get(timeout=1))
            except Queue.Empty: pass
            except KeyError, err: print KeyError,err ; COMPILE = None
## singleton            
forth_thread = FORTH_thread()
 
## @}
 
## @}
 
## @defgroup gui GUI
## `wxPython` wrappers and microIDE
## @{
 
# use wxPython
import wx
# and Scintilla editor
import wx.stc
 
# need 
 
## wxApplication
app = wx.App()
 
# large monospace font adopted for screen size
## fetch screen height as base for font scale
displaY = wx.GetDisplaySizeMM()[1]
## fetch available font from system
font = wx.Font(displaY / 0x11,
               wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
 
## @defgroup editor IDE/Text editor
## @{
 
## text editor window
class Editor(wx.Frame):
    ## construct text editor
    ## @param[in] parent window
    ## @param[in] title window title
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.initMenu()
        self.initEditor()
    ## initialize menu
    def initMenu(self):
        ## menu
        self.menu = wx.MenuBar() ; self.SetMenuBar(self.menu)
         
        ## file
        self.file = wx.Menu() ; self.menu.Append(self.file, '&File')
        ## file/save
        self.save = self.file.Append(wx.ID_SAVE, '&Save')
        self.Bind(wx.EVT_MENU,self.onSave,self.save)
        ## file/backup
        self.backup = self.file.Append(wx.ID_APPLY,'&Backup\tCtrl+E')
        self.Bind(wx.EVT_MENU, self.onBackup, self.backup)
        ## file/quit
        self.quit = self.file.Append(wx.ID_EXIT, '&Quit')
        self.Bind(wx.EVT_MENU, self.onClose, self.quit)
         
        ## debug
        self.debug = wx.Menu() ; self.menu.Append(self.debug,'&Debug')
        ## debug/refresh
        self.refresh = self.debug.Append(wx.ID_REFRESH,'&Refresh\tF12')
        self.Bind(wx.EVT_MENU, self.onRefresh, self.refresh)
        ## debug/vocabulary
        self.words = self.debug.Append(wx.ID_ANY,'&Vocabulary\tF8',kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.toggleWords, self.words)
        ## debug/stack
        self.stack = self.debug.Append(wx.ID_ANY,'&Stack\tF9',kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.toggleStack, self.stack)
 
        ## help
        self.help = wx.Menu() ; self.menu.Append(self.help, '&Help')
        ## help/about
        self.about = self.help.Append(wx.ID_ABOUT, '&About\tF1')
        self.Bind(wx.EVT_MENU, lambda e:wx.MessageBox(README), self.about)
         
    ## initialize editor
    def initEditor(self):
        ## editor
        self.editor = wx.stc.StyledTextCtrl(self)
        ## set default styling in editor
        self.editor.SetTabWidth(4)
        self.editor.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                        'face:%s,size:%s' % (font.FaceName, font.PointSize))
        self.initColorizer()
        # load default file
        self.onLoad(None)
        # bind keys
        self.editor.Bind(wx.EVT_CHAR, self.onKey)
    ## initialize colorizer
    def initColorizer(self):
        # define styles
        ## comment
        self.style_COMMENT = 1
        self.editor.StyleSetSpec(self.style_COMMENT,'fore:#0000FF')
        ## operator
        self.style_OPERATOR = 2
        self.editor.StyleSetSpec(self.style_OPERATOR,'fore:#008800')
        ## compiler words
        self.style_COMPILER = 3
        self.editor.StyleSetSpec(self.style_COMPILER,'fore:#FF0000')
        ## number literals
        self.style_NUMBER = 4
        self.editor.StyleSetSpec(self.style_NUMBER,'fore:#008888')
        ## string literal
        self.style_STRING = 5
        self.editor.StyleSetSpec(self.style_STRING,'fore:#888800')
        # bind colorizer event
        self.editor.Bind(wx.stc.EVT_STC_STYLENEEDED,self.onStyle)
    ## colorizer callback
    def onStyle(self,e):
        lexer.input(self.editor.GetValue())
        while True:
            token = lexer.token()
            if not token: break  # end of source
            self.editor.StartStyling(token.lexpos, 0xFF)
            if token.type == 'comment':
                self.editor.SetStyling(token.toklen,self.style_COMMENT)
            elif token.type == 'operator':
                self.editor.SetStyling(token.toklen,self.style_OPERATOR)
            elif token.type == 'defoperator':
                self.editor.SetStyling(token.toklen,self.style_COMPILER)
            elif token.type in ['number','integer','hex','binary']:
                self.editor.SetStyling(token.toklen,self.style_NUMBER)
            elif token.type == 'string':
                self.editor.SetStyling(token.toklen,self.style_STRING)
            else:
                self.editor.SetStyling(0,0)
                 
    ## key press callback
    def onKey(self,e):
        char = e.GetKeyCode() ; ctrl = e.CmdDown() ; shift = e.ShiftDown()
        if char == 0x0D and ctrl or shift:
            Q.put(self.editor.GetSelectedText())
        e.Skip()
     
    ## toggle words window
    def toggleWords(self,e):
        if words.IsShown(): words.Hide()
        else:               words.Show() ; self.onRefresh(None)
    ## toggle stack window
    def toggleStack(self,e):
        if stack.IsShown(): stack.Hide()
        else:               stack.Show() ; self.onRefresh(None)
    ## update debug windows
    def onRefresh(self,e):
        if words.IsShown(): words.editor.SetValue(W.dump())
        if stack.IsShown(): stack.editor.SetValue(D.dump())
    ## close GUI
    def onClose(self,e):
        main.Close() ; stack.Close() ; words.Close()
    ## save callback
    def onSave(self,e):
        F = open(self.Title,'w') ; F.write(self.editor.GetValue()) ; F.close()
    ## load calback
    def onLoad(self,e):
        try:
            F = open(self.Title,'r') ; self.editor.SetValue(F.read()) ; F.close()
        except IOError: pass # no file
    ## backup (hybernation)
    def onBackup(self,e): backup()
 
## main window
main = Editor(None, title = sys.argv[0] + '.src') ; main.Show()
#main.editor.SetValue(README)
 
## stack window
stack = Editor(main, title = sys.argv[0] + '.stack')
 
## vocabulary window
words = Editor(main, title = sys.argv[0] + '.words')
 
## @}
 
## start GUI in separate thread
class GUI_thread(threading.Thread):
    ## run wxApplication in thread to fix problem with errors in `FORTH/Q.get`
    def run(self): app.MainLoop()
## GUI thread singleton
gui_thread = GUI_thread() 
 
## @}
 
if __name__ == '__main__':
    restore()
    forth_thread.start()
    gui_thread.start()
    gui_thread.join()
    ## thread stop flag
    forth_thread.stop = True ; forth_thread.join()
