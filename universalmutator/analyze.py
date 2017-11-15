import subprocess
import sys
import glob

def main():

    src = sys.argv[1]
    tstCmd = sys.argv[2]

    srcEnd = src.split(".")[-1]


    for f in glob.glob(src.replace(srcEnd,".mutant.*." + srcEnd)):
        print f


if __name__ == '__main__':
    main()        
                       
