import os
import subprocess
import shutil


def extractASM(text, filename):
    newText = ""
    lines = text.split("\n")
    assemblyStart = False
    for l in lines:
        if assemblyStart:
            if (filename not in l) and ("auxdata: 0x" not in l):
                newText += (l + "\n")
        elif l.find("EVM assembly:") == 0:
            assemblyStart = True
    return newText


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=None):
    copyForImport = False
    if compileFile is None:
        compileFile = tmpMutantName
    else:
        shutil.copy(sourceFile, ".um.out." + str(os.getpid()) + ".src_backup")
        copyForImport = True
    outName = ".um.out." + str(os.getpid()) + ".asm"
    if len(uniqueMutants) == 0:
        shutil.copy(tmpMutantName, tmpMutantName + ".backup." + str(os.getpid()))
        shutil.copy(sourceFile, tmpMutantName)
        with open(outName, 'w') as file:
            r = subprocess.call(
                ["solc", compileFile, "--asm", "--optimize"], stdout=file, stderr=file)
        with open(outName, 'r') as file:
            if not copyForImport:
                uniqueMutants[extractASM(file.read(), tmpMutantName)] = 1
            else:
                uniqueMutants[extractASM(file.read(), sourceFile)] = 1
        shutil.copy(tmpMutantName + ".backup." + str(os.getpid()), tmpMutantName)
    if copyForImport:
        shutil.copy(tmpMutantName, sourceFile)
    try:
        with open(outName, 'w') as file:
            r = subprocess.call(["solc", compileFile, "--asm",
                                 "--optimize"], stdout=file, stderr=file)
    finally:
        if copyForImport:
            shutil.copy(".um.out." + str(os.getpid()) + ".src_backup", sourceFile)
    if r == 0:
        with open(outName, 'r') as file:
            if not copyForImport:
                code = extractASM(file.read(), tmpMutantName)
            else:
                code = extractASM(file.read(), sourceFile)
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
