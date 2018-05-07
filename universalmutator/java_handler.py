import subprocess
import shutil
import os


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    classFile = sourceFile.replace(".java", ".class")
    try:
        shutil.copy(sourceFile, sourceFile + ".um.backup")
        if os.path.exists(classFile):
            shutil.copy(classFile, classFile + ".um.backup")
        shutil.copy(tmpMutantName, sourceFile)
        with open(".um.mutant_output", 'w') as file:
            r = subprocess.call(["javac", sourceFile],
                                stdout=file, stderr=file)
    finally:
        shutil.copy(sourceFile + ".um.backup", sourceFile)
        os.remove(sourceFile + ".um.backup")
        if os.path.exists(classFile + ".um.backup"):
            shutil.copy(classFile + ".um.backup", classFile)
            os.remove(classFile + ".um.backup")
    if r == 0:
        return "VALID"
    else:
        return "INVALID"
