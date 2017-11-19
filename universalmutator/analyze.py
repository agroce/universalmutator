import subprocess
import sys
import glob
import shutil
import os

def main():

    args = sys.argv

    if "--help" in args:
        print "USAGE: analyze_mutants <sourcefile> <cmd> [--mutantDir directory]"
        print "       <cmd> is command to execute to run tests"
        print "       --mutantDir: directory to put generated mutants in; defaults to current directory"        
        sys.exit(0)    
    
    mdir = None
    try:
        mdirpos = args.index("--mutantDir")
    except ValueError:
        mdirpos = -1
        
    if mdirpos != -1:
        mdir = args[mdirpos+1]
        args.remove("--mutantDir")
        args.remove(mdir)    
    
    src = args[1]
    tstCmd = args[2]
    ignore = []
    if len(args) > 3:
        with open (sys.argv[3]) as file:
            for l in file:
                ignore.append(l.split()[0])

    srcFile = src.split("/")[-1]
    srcEnd = (src.split(".")[-1]).split("/")[-1]

    count = 0.0
    killCount = 0.0

    with open("killed.txt",'w') as killed:
        with open ("notkilled.txt",'w') as notkilled:
            for f in glob.glob(mdir + "/" + srcFile.replace(srcEnd,"mutant.*." + srcEnd)):
                print f,
                if f in ignore:
                    print "SKIPPED"
                try:
                    shutil.copy(src,src+".um.backup")
                    shutil.copy(f,src)
                    with open(os.devnull,'w') as dnull:
                        r = subprocess.call(tstCmd,shell=True,stderr=dnull,stdout=dnull)
                    count += 1
                    if r == 0:
                        print "NOT KILLED"
                        notkilled.write(f+"\n")
                        notkilled.flush()
                    else:
                        killCount += 1
                        print "KILLED"
                        killed.write(f+"\n")
                        killed.flush()
                finally:
                    shutil.copy(src+".um.backup",src)
                    os.remove(src+".um.backup")
    print "MUTATION SCORE:",killCount/count
    

if __name__ == '__main__':
    main()        
                       
