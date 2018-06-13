import marshal
import os
import sys
import py_compile


def buildCode(c):
    val = []
    try:
        val.append(c.co_code)
    except BaseException:
        if type(c) == str:
            val.append("@STRING@:" + c)
        else:
            val.append(c)
    try:
        for cc in c.co_consts:
            bc = buildCode(cc)
            try:
                if bc[0].find("@STRING@") == 0:
                    bc = bc[1:]
            except BaseException:
                pass
            val.append(bc)
    except BaseException:
        pass
    return tuple(val)


def getPythonCode(fname):
    # Courtesy of Ned Batchelder, just get the code object from the .pyc file
    f = open(fname, "rb")
    f.read(4)
    f.read(4)
    if sys.version_info >= (3, 3):
        f.read(4)
    code = marshal.load(f)
    return buildCode(code)


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    compiled = tmpMutantName.replace(".py", ".pyc")

    if os.path.exists(compiled):
        os.remove(compiled)

    try:
        py_compile.compile(tmpMutantName, doraise=True, cfile=compiled)
    except py_compile.PyCompileError:
        return "INVALID"

    if len(uniqueMutants) == 0:
        sourceCompiled = sourceFile.replace(".py", ".pyc")
        py_compile.compile(sourceFile, cfile=sourceCompiled)
        if os.path.exists(sourceCompiled):
            uniqueMutants[getPythonCode(sourceCompiled)] = 1

    if os.path.exists(compiled):
        code = getPythonCode(compiled)
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
