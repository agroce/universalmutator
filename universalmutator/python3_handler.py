import marshal
import os
import subprocess
import pkg_resources


def getPythonCode(fname):
    # Courtesy of Ned Batchelder, just get the code object from the .pyc file
    f = open(fname, "rb")
    f.read(4)
    f.read(4)
    f.read(4)  # For python 3.3+
    code = marshal.load(f)
    return code


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    with pkg_resources.resource_stream('src', 'static/handlemutant.py') as pyhandler:
        with open(".um.handlemutant.py", 'w') as file:
            for l in pyhandler:
                file.write(l)

    if len(uniqueMutants) == 0:
        sourceCompiled = sourceFile.replace(".py", ".pyc")
        if os.path.exists(sourceCompiled):
            uniqueMutants[getPythonCode(sourceCompiled)] = 1

    compiled = tmpMutantName.replace(".py", ".pyc")
    if os.path.exists(compiled):
        os.remove(compiled)
    with open(".um.mutant_output", 'w') as file:
        subprocess.call(["python3", ".um.handlemutant.py"],
                        stdout=file, stderr=file)
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
