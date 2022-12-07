import argparse
import os
import platform
import shlex
import subprocess
import time
from argparse import Namespace

from colorama import Fore

import compiler
import errors
import tokenise


def run_compile(flags: Namespace):
    _platform = platform.system()

    def red(string): return Fore.RED + string + Fore.RESET

    filename = flags.source_file

    if not os.path.isfile(filename):
        print(red(f"[ERROR]: '{filename}' not found. Please check the file name and try again"))
        exit(1)

    info = flags.info
    run = flags.run
    run_and_del = flags.runanddelete
    print_tokens = flags.tokens
    raw_tokens = flags.rawtokens
    failprint = flags.failprint
    _print = flags.print
    output = flags.output
    fastmath = flags.fastmath
    verbose = flags.verbose
    check = flags.check
    gpp_errors = flags.gpperrors

    if raw_tokens:
        print(tokenise.gettokens(filename=filename, verbose=verbose))
        exit()

    if info:
        print(f"\n[INFO]: Started compiling {filename}\n")

    start_time = time.perf_counter()

    compiledcode, tokens = compiler.Compile(
        tokens=tokenise.gettokens(filename=filename, verbose=verbose),
        verbose=verbose,
        filename=filename
    ).iteratetokens()

    if print_tokens:
        print(tokens)
        exit(1)

    if _print:
        print(compiledcode)
        exit(1)

    outname = filename.split('.')[0]
    if output:
        outname = output
    elif _platform not in ("Linux", "Darwin"):
        outname += '.exe'

    if fastmath:
        opt = '-O3'
    elif _platform == "Linux":
        opt = '-O2'
    else:
        opt = '-O3'

    cmd = [
        "g++",
        "-std=c++2a",
        opt,
        "-w",
        "-xc++",
        "-o", outname,
        "-",
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if _platform in ("Linux", "Darwin"):
        process.stdin.write(compiledcode.encode('utf-8'))
    else:
        process.stdin.write(str.encode(compiledcode))
        # XXX: not sure if this is actually needed on Windows
        process.stdin.close()

    output, error = process.communicate()

    end_time = time.perf_counter()


    if error != b"":
        errorstr = errors.cpperrortorenloierror(error.decode(
            'utf-8')) if not gpp_errors else error.decode('utf-8')
        if not gpp_errors and not check:
            print(red(f"renloi: CompilationError:\n{errorstr}"))

        elif gpp_errors:
            print(red(errorstr))

        if check:
            print(
                red(f"[INFO]: Errors in the compilation of '{filename}'; unsuccessful check"))

        if failprint:
            print(compiledcode)
            exit(1)

    if output == b"":
        filename = filename.split('.')[0].replace(
            "/", "\\\\") if _platform != "Linux" else filename.split('.')[0]
        if info and not check:
            print(
                f"[INFO]: Finished compiling '{filename}' in {round(end_time-start_time, 2)}s ({round(end_time-start_time, 2) * 1000}ms)\n")

        if check:
            print(
                f"[INFO] No errors in the compilation of '{filename}.rn'; successful check")
            os.remove(filename.split('.')[0]) if _platform == "Linux" else os.remove(
                filename + ".exe")
            exit(0)

        if run_and_del:
            os.system(
                f"./{filename.split('.')[0]}") if _platform == "Linux" else os.system(f".\{filename}.exe")
            os.remove(filename.split('.')[0]) if _platform == "Linux" else os.remove(
                filename + ".exe")

        elif run:
            os.system(
                f"./{filename.split('.')[0]}") if _platform == "Linux" else os.system(f".\{filename}.exe")


def main():
    parser = argparse.ArgumentParser(prog='renloi')
    parser.add_argument(
        '-i', '--info', action='store_true',
        help='Print additional information about compilation (such as time taken). Defaults to off.'
    )
    parser.add_argument(
        '-r', '--run', action='store_true',
        help='Run the generated executable automatically after compilation. Defaults to off.'
    )
    parser.add_argument(
        '-rd', '--runanddelete', action='store_true',
        help='Run the generated executable automatically after compilation, and then delete it. Defaults to off.'
    )
    parser.add_argument(
        '-o', '--output', type=str, default='',
        help='The string specified after the flag will be the name of the generated executable. '
             'Defaults to the name of the Renloi file that was passed in.'
    )
    parser.add_argument(
        '-fm', '--fastmath', action='store_true',
        help='Perform aggressive optimisations speed on calculations at the cost of some precision. Defaults to off.'
    )
    parser.add_argument(
        '-c', '--check', action='store_true',
        help='Check if the program will compile without actually compiling it. Defaults to off.'
    )
    parser.add_argument(
        '-t', '--tokens', action='store_true',
        help='Print tokens and exit. Defaults to off.'
    )
    parser.add_argument(
        '-rt', '--rawtokens', action='store_true',
        help='Print raw/unfiltered tokens and exit. Defaults to off.'
    )
    parser.add_argument(
        '-fp', '--failprint', action='store_true',
        help='Print generated C++ code if compilation fails. Defaults to off.'
    )
    parser.add_argument(
        '-p', '--print', action='store_true',
        help='Print generated C++ code and exit. Defaults to off.'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Run with verbose logging. Defaults to off.'
    )
    parser.add_argument(
        '-ge', '--gpperrors', action='store_true',
        help='Print g++ errors compiler errors instead of renloi ones. Defaults to off.'
    )
    parser.add_argument('source_file', type=str, help='Source file')
    parsed_args = parser.parse_args()
    run_compile(flags=parsed_args)


if __name__ == "__main__":
    main()
