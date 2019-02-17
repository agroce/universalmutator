from __future__ import print_function

import subprocess
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

    mdir = ""
    try:
        mdirpos = args.index("--mutantDir")
    except ValueError:
        mdirpos = -1

    if mdirpos != -1:
        mdir = args[mdirpos + 1]
        args.remove("--mutantDir")
        args.remove(mdir)
        mdir += "/"

    src = args[1]
    coverFile = args[2]
    outFile = args[3]

    tstl = "--tstl" in sys.argv

    srcBase = src.split("/")[-1]
    srcEnd = src.split(".")[-1]

    with open(coverFile) as file:
        if not tstl:
            lines = map(int, file.read().split())
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
            with open(".mutant_diff", 'w') as file:
                subprocess.call(["diff", src, f], stdout=file, stderr=file)
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
            if line in lines:
                coveredFile.write(f.split("/")[-1] + "\n")


if __name__ == '__main__':
    main()
