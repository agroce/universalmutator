import subprocess
import shutil
import os

def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    return "VALID"
    classFile = sourceFile.replace(".java",".class")    
    if len(uniqueMutants) == 0:
        try:
            if os.path.exists(classFile):
                shutil.copy(classFile,".um.backup."+classFile)                        
            with open(".um.mutant_output",'w') as file:    
                r = subprocess.call(["javac",sourceFile],stdout=file,stderr=file)
            with open(classFile,'rb') as file:
                uniqueMutants[file.read()] = 1
        finally:
            if os.path.exists(".um.backup."+classFile):
                shutil.copy(".um.backup."+classFile,classFile)                            
    try:
        shutil.copy(sourceFile,".um.backup."+sourceFile)
        if os.path.exists(classFile):
            shutil.copy(classFile,".um.backup."+classFile)        
        shutil.copy(tmpMutantName,sourceFile)                
        with open(".um.mutant_output",'w') as file:    
            r = subprocess.call(["javac",sourceFile],stdout=file,stderr=file)
    finally:
        shutil.copy(".um.backup."+sourceFile,sourceFile)
        if os.path.exists(".um.backup."+classFile):
            shutil.copy(".um.backup."+classFile,classFile)                
    if r == 0:
        with open(classFile,'rb') as file:
            code = file.read()
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
