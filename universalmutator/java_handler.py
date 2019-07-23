import os
import subprocess
import shutil


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    backupName = sourceFile + ".um.backup." + str(os.getpid())
    classFile = sourceFile.replace(".java", ".class")
    classBackupName = classFile + ".um.backup" + str(os.getpid())
    try:
        shutil.copy(sourceFile, backupName)
        if os.path.exists(classFile):
            shutil.copy(classFile, classBackupName)
        shutil.copy(tmpMutantName, sourceFile)
        with open(".um.mutant_output" + str(os.getpid()), 'w') as file:
            r = subprocess.call(["javac", sourceFile],
                                stdout=file, stderr=file)
    finally:
        shutil.copy(backupName, sourceFile)
        os.remove(backupName)
        if os.path.exists(classBackupName):
            shutil.copy(classBackupName, classFile)
            os.remove(classBackupName)
    if r == 0:
        return "VALID"
    else:
        return "INVALID"
