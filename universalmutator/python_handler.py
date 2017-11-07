import marshal
import os
import subprocess
import pkg_resources

def getPythonCode(fname):
    # Courtesy of Ned Batchelder, just get the code object from the .pyc file
    f = open(fname, "rb")
    magic = f.read(4)
    moddate = f.read(4)
    # Note that for Python 3.3+ you'd need another f.read(4) here since the format changed
    code = marshal.load(f)
    return code

def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    with pkg_resources.resource_stream('universalmutator', 'static/handlemutant.py') as pyhandler:
        with open("handlemutant.py",'w') as file:
            for l in pyhandler:
                file.write(l)
            
    if len(uniqueMutants) == 0:
            sourceCompiled = sourceFile.replace(".py",".pyc")
            if os.path.exists(sourceCompiled):
                uniqueMutants [getPythonCode(sourceCompiled)] = 1
    
    compiled = tmpMutantName.replace(".py",".pyc")
    if os.path.exists(compiled):
        os.remove(compiled)
    with open("mutant_output",'w') as file:
        subprocess.call(["python","handlemutant.py"],stdout=file,stderr=file)
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
