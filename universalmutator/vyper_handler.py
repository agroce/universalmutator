import os
import subprocess
import shutil


def extractOpcodes(text, filename):
    return text


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    outName = ".um.out." + str(os.getpid()) + ".opcodes"
    if len(uniqueMutants) == 0:
        shutil.copy(tmpMutantName, tmpMutantName + ".backup." + str(os.getpid()))
        shutil.copy(sourceFile, tmpMutantName)
        with open(outName, 'w') as file:
            r = subprocess.call(
                ["vyper", tmpMutantName, "-f", "opcodes"], stdout=file, stderr=file)
        with open(outName, 'r') as file:
            uniqueMutants[extractOpcodes(file.read(), tmpMutantName)] = 1
    with open(outName, 'w') as file:
        r = subprocess.call(["vyper", tmpMutantName, "-f",
                             "opcodes"], stdout=file, stderr=file)
    if r == 0:
        with open(outName, 'r') as file:
            code = extractOpcodes(file.read(), tmpMutantName)
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
