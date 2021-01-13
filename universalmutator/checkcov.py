from __future__ import print_function

import sys
import glob


def main():

    args = sys.argv

    if ("--help" in args) or (len(sys.argv) < 4):
        if len(sys.argv) < 4:
            print("ERROR: check_covered requires at least three arguments\n")
        print("USAGE: check_covered <sourcefile> <coverfile> <outfile> [--tstl] [--mutantDir directory]")
        print("       --mutantDir: directory to put generated mutants in; defaults to current directory")
        print("       --tstl: process <coverfile> that is output from TSTL internal report")
        sys.exit(0)

    mdir = "."
    try:
        mdirpos = args.index("--mutantDir")
    except ValueError:
        mdirpos = -1

    if mdirpos != -1:
        mdir = args[mdirpos + 1]
        args.remove("--mutantDir")
        args.remove(mdir)
    if mdir[-1] != "/":
        mdir += "/"

    src = args[1]
    coverFile = args[2]
    outFile = args[3]

    tstl = "--tstl" in sys.argv

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
