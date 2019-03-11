import os
import subprocess
import shutil


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    backupName = tmpMutantName + ".backup." + str(os.getpid())
    outName = ".um.mutant_output." + str(os.getpid())
    if len(uniqueMutants) == 0:
        shutil.copy(tmpMutantName, backupName)
        shutil.copy(sourceFile, tmpMutantName)
        with open(outName, 'w') as file:
            r = subprocess.call(["rustc", tmpMutantName],
                                stdout=file, stderr=file)
        with open(tmpMutantName.replace(".rs", ""), 'rb') as file:
            uniqueMutants[file.read()] = 1
        shutil.copy(backupName, tmpMutantName)
    with open(outName, 'w') as file:
        r = subprocess.call(["rustc", tmpMutantName], stdout=file, stderr=file)
    if r == 0:
        with open(tmpMutantName.replace(".rs", ""), 'rb') as file:
            code = file.read()
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
