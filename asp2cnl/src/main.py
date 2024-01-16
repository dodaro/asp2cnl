import argparse

from asp2cnl.compiler import compile
from asp2cnl.parser import ASPParser
from cnl2asp.cnl2asp import Cnl2asp
from io import StringIO

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('definition_file')
    parser.add_argument('output_file', type=str, nargs='?', default='out.txt')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    definition_file = args.definition_file
    program = open(input_file, "r").read()
    definitions = ASPParser(program).parse()

    cnl_results = StringIO()
    with open(definition_file, "r") as f:
        symbols = Cnl2asp(f).get_symbols() 
        for rule in definitions:                  
            compiled = compile(rule, symbols)
            cnl_results.write(compiled)     
            cnl_results.write("\n")
    try:
        with open(output_file, "w") as out_file:
            if out_file.write(cnl_results.getvalue()):
                print("Compilation completed.")
    except Exception as e:
        print("Error in writing output", str(e))    
    print("Results: \n")       
    print(cnl_results.getvalue())