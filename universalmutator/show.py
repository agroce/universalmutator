from __future__ import print_function
import sys
import argparse

from universalmutator import utils


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile",nargs = 1, metavar="<infile>")

    parser.add_argument("--mutantDir", nargs=1, metavar="<dir>", help = "directory with all mutants; defaults to current directory")

    parser.add_argument("--sourceDir", nargs=1, metavar="<dir>", help = "directory of source files; defaults to current directory")

    parser.add_argument("--concise", action="store_true", help="display in concise mutant format")

    args = parser.parse_args()

    infile = args.infile

    concise = args.concise
 
    mdir= args.mutantDir
    if mdir == None:
        mdir = "."
    if mdir[-1] != "/":
        mdir += "/"

    sdir= args.sourceDir
    if sdir == None:
        sdir = "."
    if sdir[-1] != "/":
        sdir += "/"

    mutants = []
    with open(infile, 'r') as mfile:
        for line in mfile:
            name = line[:-1]
            suffix = "." + name.split(".")[-1]
            mpart = ".mutant." + name.split(".mutant.")[1]
            original = sdir + name.replace(mpart, suffix)
            mutants.append(utils.readMutant(name, original, mutantDir=mdir))
    print("READ", len(mutants), "MUTANTS")

    pos = 1
    for m in mutants:
        print("*"*80)
        print("MUTANT #" + str(pos) + ":")
        pos += 1
        utils.show(m, concise=concise, mutantDir=mdir)


if __name__ == '__main__':
    main()
