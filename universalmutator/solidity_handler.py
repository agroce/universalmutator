import subprocess
import shutil

def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    if len(uniqueMutants) == 0:
        shutil.copy(tmpMutantName,tmpMutantName+".backup")
        shutil.copy(sourceFile,tmpMutantName)
        with open(".um.out.asm",'w') as file:    
            r = subprocess.call(["solc",tmpMutantName,"--asm"],stdout=file,stderr=file)
        with open(".um.out.asm",'r') as file:
            uniqueMutants[file.read()] = 1
    with open(".um.out.asm",'w') as file:    
        r = subprocess.call(["solc",tmpMutantName,"--asm"],stdout=file,stderr=file)
    if r == 0:
        with open(".um.out.asm",'r') as file:
            code = file.read()
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
