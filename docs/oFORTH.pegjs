// oFORTH PEG grammar for PEG.js

start "PEG grammar entry point"
	= element*

element "any syntax element"
	= comment
    / dropspaces
    / string
    
comment
	= prefix:[\\\#] body:[^\n]* eol:"\n"

dropspaces "drop spaces"
	= [ \t\r\n]+

string "string literal"
	= "'" .* "'"
