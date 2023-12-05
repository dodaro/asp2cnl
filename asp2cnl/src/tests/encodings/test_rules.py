import unittest

import os
import sys
##ROOT_CNL2ASP_PATH = 'C:/Users/Kristian/git/cnl/cnl2asp/'
##sys.path += [os.path.abspath(__file__ + "/../.."), ROOT_CNL2ASP_PATH + 'src']
sys.path += [os.path.abspath(__file__ + "/../..")]

import os.path
from io import StringIO

from asp2cnl.compiler import compile
from asp2cnl.parser import ASPParser

from cnl2asp.cnl2asp import Cnl2asp

##from lark import Lark
##aspCoreParser = Lark(open(os.path.join(os.path.dirname(__file__), "../asp2cnl/asp_core_2_grammar/asp_grammar.lark"), "r").read())

class TestRules(unittest.TestCase):
    def test_simple(self):
        results = StringIO()
        
        #program = open(os.path.join(os.path.dirname(__file__), "singleTest.asp"), "r").read()
        program = open(os.path.join(os.path.dirname(__file__), "test_rules.asp"), "r").read()
        ##content_tree: ASPContentTree = ASPTransformer().transform(aspCoreParser.parse(program))
        #print(content_tree)
        ##definitions = [content_tree.rules[i] for i in range(len(content_tree.rules))]
        definitions = ASPParser(program).parse()

        with open(os.path.join(os.path.dirname(__file__), "facts1.cnl"), "r") as f:
            symbols = Cnl2asp(f).get_symbols()
            #print(symbols)
            #print(get_symbol(symbols, "work in"))
            #print("ResultsA: \n")       
            for rule in definitions:           
                results.write("RULE: ")
                results.write("\n")
                results.write(rule.toString())
                results.write("\n")
                results.write("\n")
                results.write("TRANSLATED IN: ")
                results.write("\n")
                compiled = compile(rule, symbols)
                results.write(compiled)     
                results.write("\n")
                outFileDisk = os.path.join(os.path.dirname(__file__), "output.cnl")
                with open(outFileDisk, "w") as out_file:
                    f.seek(0)                    
                    out_file.write(f.read())
                with open(outFileDisk, "a") as out_file:
                    out_file.write(compiled)           
                #print("Translating: " + compiled) 
                with open(outFileDisk, "r") as in_file:                    
                    cnl2asp = Cnl2asp(in_file)
                    result = cnl2asp.compile()            
                    results.write("TRANSLATION BACK: ")
                    results.write("\n")
                    results.write(result)
                results.write("\n")
                results.write("------------------")
                
                results.write("\n")
            print("Results: \n")       
            print(results.getvalue())

if __name__ == '__main__':
    unittest.main()
