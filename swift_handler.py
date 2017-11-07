import subprocess

def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):

    with open("mutant_output",'w') as file:    
        r = subprocess.call(["swiftc",tmpMutantName],stdout=file,stderr=file)
    if r == 0:
        return "VALID"
    else:
        return "INVALID"
