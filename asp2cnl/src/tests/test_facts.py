import unittest

import os
import sys
ROOT_CNL2ASP_PATH = 'C:/Users/Kristian/git/cnl2asp/cnl2asp/'

sys.path += [os.path.abspath(__file__ + "/../.."), ROOT_CNL2ASP_PATH + 'src']

import os.path
from io import StringIO

from asp2cnl.parser import ASPTransformer, ASPContentTree, ClassicalLiteral, Disjunction
from asp2cnl.compiler import compile
from cnl2asp.cnl2asp import Cnl2asp

from lark import Lark
aspCoreParser = Lark(open(os.path.join(os.path.dirname(__file__), "../asp2cnl/asp_core_2_grammar/asp_grammar.lark"), "r").read())

class TestFacts(unittest.TestCase):
    def test_with_all_symbols(self):
        results = StringIO()
        
        program = open(os.path.join(os.path.dirname(__file__), "test_facts.asp"), "r").read()
        content_tree: ASPContentTree = ASPTransformer().transform(aspCoreParser.parse(program))
        definitions = [content_tree.rules[i] for i in range(len(content_tree.rules))]

        f = open(os.path.join(os.path.dirname(__file__), "facts1.cnl"), "r")    
        symbols = Cnl2asp(f).get_symbols()
        #print(symbols)
        #print(get_symbol(symbols, "work in"))
        
        for rule in definitions:
            print("RULE: " + rule)
            print("TRANSLATED IN: ")
            results.write(compile(rule, symbols))            
        print(results.getvalue())

if __name__ == '__main__':
    unittest.main()
