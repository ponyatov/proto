
## @defgroup metainfo Metainformation
## @brief Project info
## @{

## module name
MODULE  = 'Q'
## short info
TITLE   = 'Qbject system'
## repository location
GITHUB  = 'https://github.com/ponyatov/Q'
## author
AUTHOR  = 'Dmitry Ponyatov'
## contact emain
EMAIL   = 'dponyatov@gmail.com'
## license
LICENSE = 'All rights reserved'

## longer project about
ABOUT   = '''
* OS IDE CAD/CAM/CAE RAD CAL (computer assisted learning)
* script languages: Python FORTH SmallTalk
* DB: (hyper)graph object knowledge database
* AI: Mynsky frames semantic hypergraph inference system
* metaprogramming and managed compilation
* @ref pls for learning via @ref GameDev
* embedded systems firmware development
  * C89/LLVM backend 
  * @ref STM32 
''' 

## README.md
README = '''
# %s
## %s
### ask for lessons how to reimplement it to know deep in use

(c) %s <<%s>>, %s

github: %s

%s
''' % (MODULE, TITLE, AUTHOR, EMAIL, LICENSE, GITHUB, ABOUT)

## @}
    
