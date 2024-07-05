import argparse
import json

from asp2cnl.compiler import compile_rule
from asp2cnl.parser import ASPParser
from cnl2nl.cnl2nl import compile_prompt, contact_llm_service

from cnl2asp.cnl2asp import Cnl2asp


def run_asp2nl():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asp2nl', action='store_true')
    parser.add_argument("-m", "--llm_model", type=str, default='openchat')
    parser.add_argument('input_file')
    parser.add_argument('definition_file')
    parser.add_argument('output_file', type=str, nargs='?', default='')
    args = parser.parse_args()

    input_file = args.input_file
    definition_file = args.definition_file
    llm_model = args.llm_model
    output_file = args.output_file

    program = open(input_file, "r").read()
    definitions = ASPParser(program).parse()
    prompt_compiler = compile_prompt()

    o = {'asp': [], 'cnl': []}
    with open(definition_file, "r") as f:
        symbols = Cnl2asp(f).get_symbols()
        for rule in definitions:
            o['asp'].append(rule.toString())
            o['cnl'].append(compile_rule(rule, symbols))

    o['nl'] = []
    for cnl in o['cnl']:
        print(f'Processing rule: {cnl}')
        o['nl'].append(contact_llm_service(model=llm_model, prompt=prompt_compiler(cnl)))

    print("\n** NL:")
    print('\n'.join(o['nl']))
    try:
        with open(output_file, 'w') as f:
            json.dump(o, f)
    except Exception as e:
        print("Error in writing output", str(e))
