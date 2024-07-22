import unittest

import os
import sys
sys.path += [os.path.abspath(__file__ + "/../../../../..")]

import os.path
from io import StringIO

from asp2cnl.compiler import compile_rule
from asp2cnl.parser import ASPParser

from cnl2asp.cnl2asp import Cnl2asp

class TestRules(unittest.TestCase):
    def test_simple(self):
        results = StringIO()
                
        program = open(os.path.join(os.path.dirname(__file__), "encoding.asp"), "r").read()
        definitions = ASPParser(program).parse()

        expectedCnl = open(os.path.join(os.path.dirname(__file__), "expected_output.cnl"), 'r').readlines()
        counterLine = 0

        with open(os.path.join(os.path.dirname(__file__), "schema.cnl"), "r") as f:
            symbols = Cnl2asp(f).get_symbols()     
            for rule in definitions:           
                results.write("RULE: ")
                results.write("\n")
                results.write(rule.toString())
                results.write("\n")
                results.write("\n")
                results.write("TRANSLATED IN: ")
                results.write("\n")
                compiled = compile_rule(rule, symbols)
                results.write(compiled)     
                results.write("\n")
                outFileDisk = os.path.join(os.path.dirname(__file__), "output.cnl")
                with open(outFileDisk, "w") as out_file:
                    f.seek(0)                    
                    out_file.write(f.read())
                with open(outFileDisk, "a") as out_file:
                    out_file.write(compiled)
                    self.assertEqual(compiled.rstrip(), expectedCnl[counterLine].rstrip(), "Expected CNL sentence '" + expectedCnl[counterLine] + "'; got '" + compiled + "'")
                #print("Translating: " + compiled) 
                with open(outFileDisk, "r") as in_file:                    
                    cnl2asp = Cnl2asp(in_file)
                    result = cnl2asp.compile()            
                    results.write("TRANSLATION BACK: ")
                    results.write("\n")
                    results.write(result)
                results.write("\n")
                results.write("------------------")
                counterLine = counterLine + 1
                results.write("\n")
            print("Results: \n")       
            print(results.getvalue())

if __name__ == '__main__':
    unittest.main()
