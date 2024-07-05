import argparse

from asp2cnl.asp2cnl import run_asp2cnl
from asp2nl.asp2nl import run_asp2nl
from cnl2nl.cnl2nl import run_cnl2nl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asp2cnl', action='store_true')
    parser.add_argument('--cnl2nl', action='store_true')
    parser.add_argument('--asp2nl', action='store_true')

    if parser.parse_known_args()[0].asp2cnl:
        run_asp2cnl()

    # Configuration for cnl2nl
    if parser.parse_known_args()[0].cnl2nl:
        run_cnl2nl()

    # Configuration for asp2nl
    if parser.parse_known_args()[0].asp2nl:
        run_asp2nl()


if __name__ == '__main__':
    main()
