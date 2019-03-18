from __future__ import print_function
import sys

import utils


def main():

    args = sys.argv

    if ("--help" in args) or (len(sys.argv) < 2):
        if len(sys.argv) < 2:
            print("ERROR: show_mutants requires at least one argument\n")
        print("USAGE: show_mutants <infile> [--mutantDir <dir>] [--sourceDir <dir>]")
        print("       --mutantDir: directory with all mutants; defaults to current directory")
        print("       --sourceDir: directory of source files; defaults to current directory")
        sys.exit(0)

    infile = sys.argv[1]

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

    sdir = ""
    try:
        sdirpos = args.index("--sourceDir")
    except ValueError:
        sdirpos = -1

    if sdirpos != -1:
        sdir = args[sdirpos + 1]
        args.remove("--sourceDir")
        args.remove(sdir)
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
        utils.show(m)


if __name__ == '__main__':
    main()
