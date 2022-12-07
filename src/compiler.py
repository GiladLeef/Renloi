import platform
import time

from colorama import Fore

import tokenise

PLATFORM = platform.system()

def red(string): return Fore.RED + string + Fore.RESET

invopmap = {v: k for k, v in tokenise.tokmap.items()}

implemented = [
    ('KW', 'def'),
    ('KW', 'for'),
    ('KW', 'if'),
    ('KW', 'elif'),
    ('KW', 'else'),
    ('KW', 'while'),
    ('KW', 'match'),
    ('KW', 'case'),
    ('KW', 'return'),
    ('KW', 'continue'),
    ('KW', 'break'),
    ('KW', 'pass'),
    ('KW', 'import'),
    ('KW', "True"),
    ("KW", "False"),
    ("KW", "try"),
    ("KW", "except"),
    ("KW", "raise"),


    ('SIG', 'NEWLINE'),
    ('SIG', 'BLOCK_START'),
    ('SIG', 'BLOCK_END'),
    ('SIG', 'TYPEPOINTER'),
    ('SIG', 'FUNCTYPEPOINTER'),
    ('SIG', 'COMMA')
]

pyexceptiontocpp = {
    "Exception": "...",
    "FileNotFoundError": "std::filesystem::__cxx11::filesystem_error"
    
}

implementedtypes = [
    "STRING",
    "FSTRING",
    "FLOAT"
]

implementedmodules = [
    "math",
    "num",
    "os",
    "sys",
    "rnd"
]

types = ["str", "int", "float", "list", "bool", "strlist", "floatlist", "None"]

typecomparisons = ["const std::type_info& inttype = typeid(int);", "const std::type_info& floattype = typeid(float);"]

includes = ["iostream", "string", "./lib/range.hpp", "cmath",
            "sstream", "./lib/format.h", "vector", "./lib/boost/multiprecision/cpp_int.hpp", "typeinfo", "./lib/std.hpp"]

using = ["util::lang::range"]

pytypetoctype = {
    "str": "pystring",
    "strlist": "strlist",
    "floatlist": "floatlist",
    "list": "intlist",
    "int": "bigint",
    "float": "long double",
    "None": "void",
    "bool": "bool"
}


typedefs = [
    ("boost::multiprecision::cpp_int", "bigint"),
    ("std::vector<pystring>", "strlist"),
    ("std::vector<bigint>", "intlist"),
    ("std::vector<float>", "floatlist"),

]


def findlastkw(tokens, currentind):
    for i in range(currentind, -1, -1):
        if tokens[i][0] == "KW":
            return tokens[i]

def findlastopind(tokens, currentind, find = None):
    for i in range(currentind, -1, -1):
        if tokens[i][0] == "OP":
            if find is not None:
                if tokens[i][1] == find:
                    return i

                else:
                    continue

            else:
                return None

def findnextopind(tokens, currentind, find = None):
    for i in range(currentind, len(tokens)):
        if tokens[i][0] == "OP":
            if find is not None:
                if tokens[i][1] == find:
                    return i

                else:
                    continue

            else:
                return None



def findnextfunctypeptr(tokens: list, currentind):
    try:
        return tokens.index(("SIG", "FUNCTYPEPOINTER"), currentind)

    except ValueError:
        return None


def parsetabamount(tabtok):
    return int(str(tabtok[1]).removesuffix(" TAB"))


def removenewlinedups(x):
    return [x[i] for i in range(len(x)) if (i == 0) or (x[i] != x[i-1]) or (x[i] != ("SIG", "NEWLINE"))]

def removeblanks(x):
    return [tok for tok in x if tok != ("SIG", "BLANK")]


class Compile:
    def __init__(self, tokens: list, verbose: bool, filename: str):
        self.tokens = tokens
        self.type = 0
        self.value = 1
        self.verbose = verbose
        self.filename = filename

        self.oktokens = self.checktokens()

    def iteratetokens(self):
        code = """#define FMT_HEADER_ONLY\n"""
        for include in includes:
            code += f'#include "{include}"\n'
        for use in using:
            code += f"using {use};\n"
        for typedef in typedefs:
            code += f"typedef {typedef[0]} {typedef[1]};"
        for typecomp in typecomparisons:
            code += typecomp + " "

        code += '\nstd::string operator * (std::string a, unsigned int b) {std::string output = "";while (b--) {output += a;}return output;}\n'

        if ("KW", "def") not in self.oktokens and ("KW", "class") not in self.oktokens:
            code += "int main(int argc, char *argv[]){\n"

        if self.verbose:
            print(f"[INFO]: Started converting {self.filename} to C++ IR;\n")

        start_time = time.perf_counter()

        for i in range(len(self.oktokens)):
            if self.oktokens[i][self.type] == "TYPE":
                if self.oktokens[i+1] == ("OP", "LPAREN"):
                    self.oktokens[i] = ("NAME", self.oktokens[i][self.value])

            if self.oktokens[i][self.type] == "KW":
                gobackby = 1

                if self.oktokens[i-1] == ("SIG", "NEWLINE"):
                    gobackby = 2

                if self.oktokens[i-gobackby][self.type] != "SIG" and not str(self.oktokens[i-gobackby][self.value]).endswith(" TAB"):
                    if self.oktokens[i+1][0] != "FUNC" and self.oktokens[i] != ("KW", "continue") and self.oktokens[i] != ("KW", "return") and self.oktokens[i] != ("KW", "import") and self.oktokens[i] != ("KW", "True") and self.oktokens[i] != ("KW", "False") and self.oktokens[i] != ("KW", "for"):
                        pass

            if self.oktokens[i][self.type] == "VAR":
                if self.oktokens[i+1] == ('SIG', 'TYPEPOINTER'):
                    if self.oktokens[i+2][1] in types:
                        typeofvar = self.oktokens[i+2][1]
                    else:
                        print(
                            red(f"error: invalid type specified for var '{self.oktokens[i][self.value]}'"))
                        exit(1)
                    ctypeofvar = pytypetoctype[typeofvar]
                    varname = self.oktokens[i][self.value]
                    code += f"{ctypeofvar} {varname}"

                else:
                    code += f"auto {self.oktokens[i][self.value]}"


            if self.oktokens[i][self.type] == "FUNCREF" or self.oktokens[i][self.type] == "VARREF":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "OP":
                if self.oktokens[i][self.value] == "LPAREN":
                    code += "("

                elif self.oktokens[i][self.value] == "RPAREN":
                    code += ")"

                elif self.oktokens[i][self.value] == "LSPAREN":
                    if self.oktokens[i-1][self.type] != "NAME":
                        code += "{"

                    else:
                        code += "["
                        srsparenind = findnextopind(self.oktokens, i, "RSPAREN")
                        if srsparenind is not None:
                            self.oktokens[srsparenind] = ("OP", "SRSPAREN")


                elif self.oktokens[i][self.value] == "RSPAREN":
                    code += "}"

                elif self.oktokens[i][self.value] == "SRSPAREN":
                    code += "]"

                elif self.oktokens[i][self.value] == "in":
                    code += ": "

                elif self.oktokens[i][self.value] == "or":
                    code += " || "

                elif self.oktokens[i][self.value] == "and":
                    code += " && "

                elif self.oktokens[i][self.value] == "not":
                    code += "!"

                else:
                    mapped = invopmap[self.oktokens[i][self.value]]
                    if mapped != ";":
                        code += " " + mapped + " "

            elif self.oktokens[i][self.type] == "STRING" or self.oktokens[i][self.type] == "INT" or self.oktokens[i][self.type] == "FLOAT":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "SIG":
                if self.oktokens[i][self.value] == "NEWLINE":
                    if i + 1 != len(self.oktokens):
                        if self.oktokens[i-1][self.type] != "SIG" and not str(self.oktokens[i-1][self.value]).endswith(" TAB") and self.oktokens[i-1][0] != "IMPORT_MODULE":
                            code += ";"

                    code += "\n"

                if self.oktokens[i][self.type] == "SIG" and str(self.oktokens[i][self.value]).endswith("TAB"):
                    code += "    " * parsetabamount(self.oktokens[i])

                if self.oktokens[i] == ("SIG", "COMMA"):
                    code += ","

                if self.oktokens[i] == ("SIG", "DOT"):
                    code += "."

                elif self.oktokens[i] == ("SIG", "BLOCK_START"):
                    code += "{"
                elif self.oktokens[i] == ("SIG", "BLOCK_END"):
                    code += "}"

            elif self.oktokens[i][self.type] == "KW":
                if self.oktokens[i][self.value] == "def":
                    if self.oktokens[i+1] == ('FUNC', 'main'):
                        code += "int "

                    else:
                        indoftypedec = findnextfunctypeptr(self.oktokens, i)
                        if indoftypedec is not None:
                            if self.oktokens[indoftypedec + 1][self.value] in types:
                                code += pytypetoctype[self.oktokens[indoftypedec + 1][self.value]] + " "
                        else:
                            code += "auto "

                elif self.oktokens[i][self.value] == "for":
                    itervarname = self.oktokens[i+1][self.value]
                    code += f"for("

                elif self.oktokens[i][self.value] == "if":
                    code += "if("

                elif self.oktokens[i][self.value] == "elif":
                    code += "else if("

                elif self.oktokens[i][self.value] == "else":
                    code += "else"

                elif self.oktokens[i][self.value] == "while":
                    code += "while("

                elif self.oktokens[i][self.value] == "try":
                    code += "try"

                elif self.oktokens[i][self.value] == "except":
                    code += "catch("

                elif self.oktokens[i][self.value] == "continue":
                    code += "continue"

                elif self.oktokens[i][self.value] == "break":
                    code += "break"
                    
                elif self.oktokens[i][self.value] == "pass":
                    code += "pass"

                elif self.oktokens[i][self.value] == "return":
                    code += "return "

                elif self.oktokens[i][self.value] == "True":
                    code += "true "

                elif self.oktokens[i][self.value] == "False":
                    code += "false "

                elif self.oktokens[i][self.value] == "import":
                    code = f'#include "./lib/py{self.oktokens[i+1][self.value]}.hpp"\n{str(self.oktokens[i+1][self.value]).capitalize()} {self.oktokens[i+1][self.value]};\n' + code

                else:
                    print(
                        red(f"error: keyword '{self.oktokens[i][self.value]}' is not yet implemented, sorry"))
                    exit(1)

            elif self.oktokens[i][self.type] == "FUNC":
                code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "NAME":
                if self.oktokens[i][self.value] in pyexceptiontocpp:
                    code += pyexceptiontocpp[self.oktokens[i][self.value]]
                else:
                    code += self.oktokens[i][self.value]

            elif self.oktokens[i][self.type] == "PARAM":
                if self.oktokens[i+1] == ("SIG", "TYPEPOINTER"):
                    if self.oktokens[i+2][1] in types:
                        typeofparam = self.oktokens[i+2][1]
                    else:
                        print(
                            red(f"error: invalid type specified for param '{self.oktokens[i][self.value]}'"))
                        exit(1)
                    ctypeofparam = pytypetoctype[typeofparam]
                    paramname = self.oktokens[i][self.value]
                    code += f"{ctypeofparam} {paramname}"

                else:
                    code += f"auto {self.oktokens[i][self.value]}"

            elif self.oktokens[i][self.type] == "IMPORTREF":
                code += self.oktokens[i][self.value] if self.oktokens[i][self.value] != "random" else "rnd"

            elif self.oktokens[i][self.type] == "METHOD":
                code += self.oktokens[i][self.value]

            if i + 1 != len(self.oktokens):
                if self.oktokens[i+1] == ("SIG", "BLOCK_END") and self.oktokens[i] != ("SIG", "NEWLINE") and self.oktokens[i] != ("SIG", "BLOCK_END"):
                    code += ";"
                if self.oktokens[i+1] == ("SIG", "BLOCK_START"):
                    blockkw = findlastkw(self.oktokens, i)
                    if blockkw not in [('KW', 'def'), ('KW', 'else'), ('KW', 'try')]:
                        code += ")"

        if ("KW", "def") not in self.oktokens and ("KW", "class") not in self.oktokens:
            pass

        end_time = time.perf_counter()

        cpplines = code.split("\n")

        newcpplines = cpplines

        """
        newcpplines = []
        for line in cpplines:
            if line.split(" ")[0] == "auto":
                varname = line.split(" ")[1].removesuffix(";")
                newcpplines.append(line + f"if(typeid({varname}) == inttype){{bigint {varname} {line.removeprefix('auto ' + varname)}}} else if(typeid({varname}) == floattype){{long double {varname} {line.removeprefix('auto ' + varname)}}}")

            else:
                newcpplines.append(line)

        """

        code = "\n".join(newcpplines)

        if self.verbose:
            print(f"[INFO]: Converted {self.filename} to C++ IR successfully in {round(end_time - start_time, 3)}s ({round(end_time - start_time, 3) * 1000}ms)\n")

        return code, self.oktokens

    def checktokens(self):
        oktokens = []

        for token in self.tokens:
            if token[self.type] == "IMPORT_MODULE" and token[self.value] not in implementedmodules:
                print(red(f"error: module/library {token[self.value]} is not implemented yet, sorry'"))
                exit(1)

            if token[self.type] == "SIG" and str(token[self.value]).endswith(" TAB"):
                oktokens.append(token)
                continue

            if token not in implemented:
                if token[self.type] not in ["STRING", "FSTRING", "FLOAT", "NAME", "FUNC", "VAR", "SIG", "PARAM", "TYPE", "INT", "OP", "VARREF", "FUNCREF", "IMPORTREF", "IMPORT_MODULE", "METHOD"]:
                    continue

                if token[self.type] == "OP":
                    pass

            oktokens.append(token)

        temp = []

        for i in range(len(oktokens)):
            if oktokens[i] == ("KW", "import") and oktokens[i+1][self.type] != "IMPORT_MODULE":
                continue

            temp.append(oktokens[i])

        oktokens = temp

        oktokens = removeblanks(removenewlinedups(oktokens))

        return oktokens
