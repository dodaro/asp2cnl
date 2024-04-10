import argparse
import os
#import sys
#sys.path.append(os.getcwd()+'/asp2cnl/src')

import json

from compiler import *
from parser import ASPParser

from cnl2asp.cnl2asp import Cnl2asp
from io import StringIO

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",  '--input_file', required=True)
    parser.add_argument("-d", '--definition_file', required=True)
    parser.add_argument("-o", '--output_file', type=str, required=False, default='asp2cnl2nl.json')   
    parser.add_argument("-s", '--std', action='store_true')   


    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    definition_file = args.definition_file
    program = open(input_file, "r").read()
    definitions = ASPParser(program).parse()

    cnl_results = StringIO()
    with open(definition_file, "r") as f:
        symbols = Cnl2asp(f).get_symbols()
        o = {'asp': [], 'cnl': []}
        for rule in definitions:
            o['asp'].append(rule.toString())
            compiled = compile(rule, symbols)
            o['cnl'].append(compiled)
            if args.std:
                print(compiled)                
    try:
        with open(output_file, "w") as f:
            json.dump(o, f)
            #if out_file.write(cnl_results.getvalue()):
            #    print("Compilation completed.")
    except Exception as e:
        print("Error in writing output", str(e))    
    #print("Results: \n")
    #print(cnl_results.getvalue())