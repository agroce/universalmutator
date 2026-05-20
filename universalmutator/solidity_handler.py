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


def _keep_temp_files():
    value = (os.environ.get("UM_KEEP_TEMP") or "").strip().lower()
    return value not in ("", "0", "false", "no")


def _cleanup_files(*paths):
    if _keep_temp_files():
        return
    for path in paths:
        if path is None:
            continue
        try:
            os.remove(path)
        except OSError:
            pass


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=None):
    pid = str(os.getpid())
    copyForImport = False
    sourceBackup = None
    mutantBackup = None
    if compileFile is None:
        compileFile = tmpMutantName
    else:
        sourceBackup = ".um.out." + pid + ".src_backup"
        shutil.copy(sourceFile, sourceBackup)
        copyForImport = True
    outName = ".um.out." + pid + ".asm"
    try:
        if len(uniqueMutants) == 0:
            mutantBackup = tmpMutantName + ".backup." + pid
            shutil.copy(tmpMutantName, mutantBackup)
            try:
                shutil.copy(sourceFile, tmpMutantName)
                with open(outName, 'w') as file:
                    subprocess.call(
                        ["solc", compileFile, "--asm", "--optimize"], stdout=file, stderr=file)
                with open(outName, 'r') as file:
                    if not copyForImport:
                        uniqueMutants[extractASM(file.read(), tmpMutantName)] = 1
                    else:
                        uniqueMutants[extractASM(file.read(), sourceFile)] = 1
            finally:
                if os.path.exists(mutantBackup):
                    shutil.copy(mutantBackup, tmpMutantName)

        if copyForImport:
            shutil.copy(tmpMutantName, sourceFile)
        try:
            with open(outName, 'w') as file:
                r = subprocess.call(
                    ["solc", compileFile, "--asm", "--optimize"], stdout=file, stderr=file)
        finally:
            if copyForImport and sourceBackup is not None and os.path.exists(sourceBackup):
                shutil.copy(sourceBackup, sourceFile)

        if r == 0:
            with open(outName, 'r') as file:
                if not copyForImport:
                    code = extractASM(file.read(), tmpMutantName)
                else:
                    code = extractASM(file.read(), sourceFile)
            if code in uniqueMutants:
                uniqueMutants[code] += 1
                return "REDUNDANT"
            uniqueMutants[code] = 1
            return "VALID"
        return "INVALID"
    finally:
        _cleanup_files(mutantBackup, sourceBackup, outName)
