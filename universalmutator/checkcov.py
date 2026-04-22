from __future__ import print_function

import sys
import glob
import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("sourcefile",nargs = 1, metavar="<sourcefile>")

    parser.add_argument("coverfile",nargs = 1, metavar="<coverfile>")

    parser.add_argument("outfile",nargs = 1, metavar="<outfile>")

    parser.add_argument("--tstl", action="store_true", help = "process <coverfile> that is output from TSTL internal report")

    parser.add_argument("--mutantDir", nargs=1, metavar="directory", help = "directory to put generated mutants in; defaults to current directory")

    args = parser.parse_args()

    mdir= args.mutantDir
    if mdir == None:
        mdir = "."
    if mdir[-1] != "/":
        mdir += "/"

    src = args.sourcefile
    coverFile = args.coverfile
    outFile = args.outfile

    tstl = args.tstl
    if tstl == None:
        tstl = False

    srcBase = src.split("/")[-1]
    srcEnd = src.split(".")[-1]

    with open(coverFile) as file:
        if not tstl:
            lines = list(map(int, file.read().split()))
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

    with open(outFile, 'w') as coveredFile:
        for f in glob.glob(
            mdir +
            srcBase.replace(
                srcEnd,
                "mutant.*." +
                srcEnd)):
            with open(src, 'r') as sf:
                sfLines = sf.readlines()
            with open(f, 'r') as mf:
                mfLines = mf.readlines()
            line = 1
            for i in range(0, min(len(sfLines), len(mfLines))):
                if sfLines[i] != mfLines[i]:
                    break
                line += 1
            print(f, line)
            if line in lines:
                coveredFile.write(f.split("/")[-1] + "\n")


if __name__ == '__main__':
    main()
