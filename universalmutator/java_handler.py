import subprocess
import shutil
import os

def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    classFile = sourceFile.replace(".java",".class")                       
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
        return "VALID"
    else:
        return "INVALID"
