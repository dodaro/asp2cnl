import argparse
import os
import json

from cnl2asp.cnl2asp import Cnl2asp
from cnl2nl.cnl2nl import compile_prompt, contact_llm_service

from src.asp2cnl.compiler import compile
from src.asp2cnl.parser import ASPParser

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('definition_file')
    parser.add_argument('output_file', type=str, nargs='?', default='asp2cnl2nl.json')
    parser.add_argument('llm_model', type=str, default='openchat')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    definition_file = args.definition_file
    program = open(input_file, "r").read()
    definitions = ASPParser(program).parse()

    prompt_compiler = compile_prompt()

    o = {'asp': [], 'cnl': []}
    with open(definition_file, "r") as f:
        symbols = Cnl2asp(f).get_symbols() 
        for rule in definitions:        
            o['asp'].append(rule.toString())         
            o['cnl'].append(compile(rule, symbols))
       
    o['nl'] = [contact_llm_service(model=args.model, prompt=prompt_compiler(cnl)) for cnl in o['cnl']]

    try:
        with open(output_file, 'w') as f:
            json.dump(o, f)
    except Exception as e:
        print("Error in writing output", str(e))