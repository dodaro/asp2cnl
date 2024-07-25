import argparse
import json

from asp2cnl.compiler import *
from asp2cnl.parser import ASPParser

from cnl2asp.cnl2asp import Cnl2asp


def run_asp2cnl():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asp2cnl', action='store_true')
    parser.add_argument('input_file')
    parser.add_argument('definition_file')
    parser.add_argument('output_file', type=str, nargs='?', default='')
    parser.add_argument('--format_output_file', type=str, nargs='?', default='json')
    parser.add_argument("-s", '--silent', action='store_true')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    definition_file = args.definition_file
    silent = args.silent
    format_output_file = args.format_output_file

    program = open(input_file, "r").read()
    definitions = ASPParser(program).parse()

    with open(definition_file, "r") as f:
        symbols = Cnl2asp(f).get_symbols()
        o = {'asp': [], 'cnl': []}
        for rule in definitions:
            o['asp'].append(rule.toString().strip())
            compiled = compile_rule(rule, symbols)
            o['cnl'].append(compiled)
            if not silent:
                print(compiled)
    if output_file:
        try:
            with open(output_file, "w") as f:
                if format_output_file == "json":
                    json.dump(o, f)
                elif format_output_file == "standard":
                    for cnl in o['cnl']:
                        f.write(cnl + "\n")
                elif format_output_file == "aspcnl":
                    counter = 0
                    for cnl in o['cnl']:
                        f.write(o['asp'][counter] + "\n")
                        f.write("% " + cnl + "\n\n")
                        counter += 1


        except Exception as e:
            print("Error in writing output", str(e))
