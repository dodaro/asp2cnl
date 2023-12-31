import sys
##ROOT_CNL2ASP_PATH = 'C:/Users/Kristian/git/cnl/cnl2asp/'
##sys.path.insert(0, ROOT_CNL2ASP_PATH + 'src')

from lark import Lark
import os.path
from io import StringIO

from asp2cnl.parser import ASPTransformer, ASPContentTree, ClassicalLiteral, Disjunction
from asp2cnl.compiler import compile

from cnl2asp.cnl2asp import Cnl2asp


aspCoreParser = Lark(open(os.path.join(os.path.dirname(__file__), "asp_core_2_grammar/asp_grammar.lark"), "r").read())



def asp2cnlTranslate():
    program = open(os.path.join(os.path.dirname(__file__), "test.asp"), "r").read()
    print (aspCoreParser.parse(program).pretty())

def asp2cnlTransform():
    program = open(os.path.join(os.path.dirname(__file__), "test.asp"), "r").read()
    print (aspCoreParser.parse(program).pretty())
    content_tree: ASPContentTree = ASPTransformer().transform(aspCoreParser.parse(program))
    print(content_tree)

def printCnl2AspSentence(sentence):
    result = None
    with open("test_cnl", "w") as out_file:
        out_file.write(sentence)                           
    with open("test_cnl", "r") as in_file:                    
        cnl2asp = Cnl2asp(in_file)
        result = cnl2asp.compile()
    return result

    
   

