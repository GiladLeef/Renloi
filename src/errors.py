cerrtopyerr = {
    "class pystring": "str"
}

class Error:
    def __init__(self, errortype, errormsg):
        self.errortype = errortype
        self.errormsg = errormsg
    
    def returnerror(self):
        return f"renloi: {self.errortype}: {self.errormsg}"


def cpperrortorenloierror(error: str):
    newerrorlines = []
    rawerrorlines = [line.strip() for line in error.split("\n")]
    while "" in rawerrorlines:
        rawerrorlines.remove("")
    errorlines = []
    for line in rawerrorlines:
        line = str(line)
        if not line == "" and "error: " in line:
            errorlines.append(line.split("error: ", 1)[1])

        else:
            errorlines.append(line.removeprefix("<stdin>: "))

    for error in errorlines:
        if error.endswith(" was not declared in this scope"):
            errortype = "NameError"
            errortok = error.removesuffix(" was not declared in this scope")[1:]
            errormsg = f"name '{errortok}' is not defined"
            newerrorlines.append(" " * 8 + Error(errortype, errormsg).returnerror())

        elif error.startswith("In function "):
            funcname = error.removeprefix("In function ")[:-2][1:].split(" ", 1)[1]
            error = f"In function '{funcname}':"
            newerrorlines.append(" " * 4 + error)  

        elif error.startswith("At "):
            newerrorlines.append(" " * 4 + error)

        elif error == "expected constructor, destructor, or type conversion before ‘(’ token":
            continue

        elif error == "expected declaration before ‘}’ token" :
            newerrorlines.append(" " * 4 + Error("SyntaxError", "semicolons and/or return values in main() are not supported, sorry").returnerror())

        elif error.startswith("call of overloaded ") :
            errorfunc = error.removeprefix("call of overloaded ").removesuffix(" is ambiguous")[1:][:-1]
            newerrorlines.append(" " * 8 + Error("NameError", f"call of overloaded {errorfunc} is unresolved").returnerror())

        elif error.startswith("conversion from ") :
            fromconv = error.removeprefix("conversion from ").split(" ", 1)[0][1:][:-1]
            toconv = error.removeprefix("conversion from ").split(" ", 1)[1].removeprefix("to non-scalar type ").split(" ", 1)[0][1:][:-1]
            newerrorlines.append(" " * 8 + Error("TypeError", f"'{fromconv}' cannot be converted/cast to '{toconv}'").returnerror())

        elif " has no member named " in error :
            obj, attr = error.replace(" has no member named ", ",,,").split(",,,", 2)
            obj = cerrtopyerr[obj[1:][:-1].strip()] if obj[1:][:-1] in cerrtopyerr else obj[1:][:-1]
            attr = attr[1:][:-1]
            newerrorlines.append(" " * 8 + Error("AttributeError", f"'{obj}' object has no attribute '{attr}'").returnerror())

        elif error == "syntax error before '}' token":
            newerrorlines.append(" " * 8 + Error("InternalError", "There seems to be something wrong with renloi. Please report it as an issue at https://github.com/giladleef/renloi/issues.").returnerror())

        else:
            newerrorlines.append(" " * 8 + "g++: " + error)
    
    return "\n".join(newerrorlines)
