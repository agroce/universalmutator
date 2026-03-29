from __future__ import print_function

import argparse
import glob


def main():

    parser = argparse.ArgumentParser(prog="check_covered",
                                     description="Filter mutants to those on lines covered by a coverage file.")
    parser.add_argument("sourcefile", help="source file being mutated")
    parser.add_argument("coverfile", help="coverage file")
    parser.add_argument("outfile", help="output file to write covered mutant names into")
    parser.add_argument("--mutantDir", default=".",
                        help="directory with all mutants; defaults to current directory")
    parser.add_argument("--tstl", action="store_true", default=False,
                        help="process coverfile that is output from TSTL internal report")
    parsed = parser.parse_args()

    mdir = parsed.mutantDir
    if mdir[-1] != "/":
        mdir += "/"

    src = parsed.sourcefile
    coverFile = parsed.coverfile
    outFile = parsed.outfile
    tstl = parsed.tstl

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
