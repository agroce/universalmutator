import glob
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
        try:
            shutil.rmtree(".tmp_mutant_fe")
        except EnvironmentError:
            pass
        with open(outName, 'w') as file:
            r = subprocess.call(
                ["fe", tmpMutantName, "--emit", "yul", "--overwrite", "-o", ".tmp_mutant_fe"], stdout=file, stderr=file)
        code = ""
        for yulf in glob.glob(".tmp_mutant_fe/*/*.yul"):
            with open(yulf, 'r') as file:
                code += extractOpcodes(file.read(), tmpMutantName)
        uniqueMutants[code] = 1
    try:
        shutil.rmtree(".tmp_mutant_fe")
    except EnvironmentError:
        pass
    with open(outName, 'w') as file:
        r = subprocess.call(["fe", tmpMutantName, "--emit",
                             "yul", "--overwrite", "-o", ".tmp_mutant_fe"], stdout=file, stderr=file)
    if r == 0:
        code = ""
        for yulf in glob.glob(".tmp_mutant_fe/*/*.yul"):
            with open(yulf, 'r') as file:
                code += extractOpcodes(file.read(), tmpMutantName)
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
