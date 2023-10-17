import sys
ROOT_CNL2ASP_PATH = 'C:/Users/Kristian/git/cnl2asp/cnl2asp/'
sys.path.insert(0, ROOT_CNL2ASP_PATH + 'src')

from lark import Lark
import os.path
from io import StringIO

from asp2cnl.parser import ASPTransformer, ASPContentTree, ClassicalLiteral, Disjunction

from cnl2asp.cnl2asp import Cnl2asp

aspCoreParser = Lark(open(os.path.join(os.path.dirname(__file__), "asp_core_2_grammar/asp_grammar.lark"), "r").read())

def get_symbol(symbols, symbol_name):
    res: list = [symbols[i] for i in
                            range(len(symbols)) if
                            symbols[i].predicate == symbol_name]
    return res[0]

def asp2cnlTranslate():
    results = StringIO()

    #program = "atom(X) | bianco(Y) :- cicccio(Z)."
    #program = ""
    #print (aspCoreParser.parse(program).pretty())
    #print(ASPTransformer().transform(aspCoreParser.parse(program)))
    program = open(os.path.join(os.path.dirname(__file__), "test.asp"), "r").read()
    content_tree: ASPContentTree = ASPTransformer().transform(aspCoreParser.parse(program))
    definitions = [content_tree.rules[i] for i in range(len(content_tree.rules))]

    f = open(os.path.join(os.path.dirname(__file__), ROOT_CNL2ASP_PATH, "examples/input_file"), "r")    
    symbols = Cnl2asp(f).get_symbols()
    #print(symbols)
    #print(get_symbol(symbols, "work in"))

    
    for rule in definitions:
        if rule.isFact():
            atom = rule.head[0].atoms[0] 
            
            if len(atom.terms) == 1:
                #Eg. pub(1). --> 1 is a pub.
                results.write(atom.terms[0].replace('"', '').capitalize()) 
                results.write(" ")
                results.write("is a") 
                results.write(atom.name)                 
                results.write(".")        
            
                results.write("\n")

            elif len(atom.terms) == 2:                
                #if "_" in atom.name:                               
                    #Eg. work_in("john",1). --> Waiter John works in pub 1.
                    symb = get_symbol(symbols, atom.name.replace("_", " "))
                    results.write(symb.attributes[0].replace('"', '').capitalize())
                    results.write(" ")
                    results.write(atom.terms[0].replace('"', '').capitalize())
                    results.write(" ")
                    results.write(symb.predicate)
                    results.write(" ")
                    results.write(atom.terms[1].replace('"', ''))
                    results.write(".")

                    results.write("\n")
            

    #print(definitions[0].isFact())
    #print(definitions)
    return results.getvalue()

