"""Renloi programming language

usage:
    renloi compile [-ldo FILE] <file>
    renloi run [-td] <file>
    renloi [-hv]

options:
    -h, --help                  Shows this help menu
    -v, --version               Shows the version
    -l, --llvm                  Emit llvm code
    -o FILE, --output FILE      Output file
    -t, --timer                 Time the execution
    -d, --debug                 Debug mode
"""

import os
from typing import Dict, Any

from docopt import docopt
from renloi.compiler.code_generator import CodeGenerator
from renloi.lexer import Lexer
from renloi.parser import Parser
from renloi.type_checker import Preprocessor
from renloi.utils import error


def process_file(rn_file: str) -> CodeGenerator:
    if not os.path.isfile(rn_file):
        error(rn_file + " is not a valid file")

    code = open(rn_file, encoding="utf8").read()
    lexer = Lexer(code, rn_file)
    parser = Parser(lexer)
    prog = parser.parse()
    symtab_builder = Preprocessor(rn_file)
    symtab_builder.check(prog)

    generator = CodeGenerator(rn_file)
    generator.generate_code(prog)

    return generator


def _run(arg_list: Dict[str, Any]) -> None:
    rn_file: str = arg_list['<file>']
    timer: bool = arg_list['--timer']
    debug: bool = arg_list['--debug']

    generator = process_file(rn_file)
    generator.evaluate(not debug, debug, timer)


def _compile(arg_list: Dict[str, Any]) -> None:
    rn_file: str = arg_list['<file>']
    output: str = arg_list['--output']
    emit_llvm: bool = arg_list['--llvm']
    debug: bool = arg_list['--debug']

    generator = process_file(rn_file)
    generator.compile(rn_file, not debug, output, emit_llvm)


if __name__ == "__main__":
    args: Dict[str, Any] = docopt(__doc__, version='v0.1.0')

    if args['compile']:
        _compile(args)
    elif args['run']:
        _run(args)
    else:
        exit(__doc__)
