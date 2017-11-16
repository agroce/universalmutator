import subprocess
import sys
import glob
import shutil
import os

def main():

    src = sys.argv[1]
    coverFile = sys.argv[2]
    outFile = sys.argv[3]

    tstl = "--tstl" in sys.argv

    srcEnd = src.split(".")[-1]

    with open(coverFile) as file:
        if not tstl:
            lines = map(int,file.read().split())
        else:
            lines = []
            for l in file:
                if "LINES" in l:
                    if src not in l:
                        continue
                    db = l.split("[")[1]
                    d = db[:-2].split(",")
                    for line in d:
                        lines.append(int(line))
    

    with open(outFile,'w') as notCovered:
        for f in glob.glob(src.replace(srcEnd,"mutant.*." + srcEnd)):
            with open(".mutant_diff",'w') as file:
                diff = subprocess.call(["diff",src,f],stdout=file,stderr=file)
            with open(".mutant_diff") as file:
                for l in file:
                    if "c" in l:
                        line = int(l.split("c")[0])
                        break
                    elif "a" in l:
                        line = int(l.split("a")[0])
                        break
                    elif "d" in l:
                        line = int(l.split("d")[0])
                        break
            if line not in lines:
                notCovered.write(f+"\n")

if __name__ == '__main__':
    main()        
                       
