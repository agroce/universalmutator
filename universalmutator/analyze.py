import subprocess
import sys
import glob
import shutil
import os

def main():

    src = sys.argv[1]
    tstCmd = sys.argv[2]
    ignore = []
    if len(sys.argv) > 3:
        with open (sys.argv[3]) as file:
            for l in file:
                ignore.append(l.split()[0])

    srcEnd = src.split(".")[-1]

    with open("killed.txt",'w') as killed:
        with open ("notkilled.txt",'w') as notkilled:
            for f in glob.glob(src.replace(srcEnd,"mutant.*." + srcEnd)):
                print f,
                if f in ignored;
                    print "SKIPPED"
                try:
                    shutil.copy(src,".backup."+src)
                    shutil.copy(f,src)
                    with open(os.devnull,'w') as dnull:
                        r = subprocess.call(tstCmd,shell=True,stderr=dnull,stdout=dnull)
                    if r == 0:
                        print "NOT KILLED"
                        notkilled.write(f+"\n")
                        notkilled.flush()
                    else:
                        print "KILLED"
                        killed.write(f+"\n")
                        killed.flush()
                finally:
                    shutil.copy(".backup."+src,src)

if __name__ == '__main__':
    main()        
                       
