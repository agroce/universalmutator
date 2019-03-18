from __future__ import print_function
import glob
import sys

import utils


def main():

    args = sys.argv

    if ("--help" in args) or (len(sys.argv) < 3):
        if len(sys.argv) < 3:
            print("ERROR: prioritize_mutants requires at least two arguments\n")
        print("USAGE: prioritize_mutants <infile[s]> <outfile> [N] [--cutoff <dist>]", end="")
        print("[--mutantDir <dir>] [--sourceDir <dir>]")
        print("       --mutantDir: directory with all mutants; defaults to current directory")
        print("       --sourceDir: directory of source files; defaults to current directory")
        print("       --cutoff:    if minimum distance is less than this, stop")
        sys.exit(0)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    infiles = glob.glob(infile)

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

    cutoff = 0.0
    try:
        cutoffpos = args.index("--cutoff")
    except ValueError:
        cutoffpos = -1

    if cutoffpos != -1:
        cutoff = args[cutoffpos + 1]
        args.remove("--cutoff")
        args.remove(cutoff)
        cutoff = float(cutoff)

    N = -1
    if len(args) >= 4:
        N = args[3]

    mutants = []
    for f in infiles:
        with open(f, 'r') as mfile:
            for line in mfile:
                name = line[:-1]
                suffix = "." + name.split(".")[-1]
                mpart = ".mutant." + name.split(".mutant.")[1]
                original = sdir + name.replace(mpart, suffix)
                mutants.append(utils.readMutant(name, original, mutantDir=mdir))
    print("READ", len(mutants), "MUTANTS")

    if N == -1:
        N = len(mutants)
    print("PRIORITIZING FIRST", N, "MUTANTS")
    if cutoff != 0.0:
        print("CUTOFF:", cutoff)

    ranking = utils.FPF(mutants, N, cutoff=cutoff)
    with open(outfile, 'w') as outf:
        for (m, r) in ranking:
            mname = m[0]
            outf.write(mname + "\n")


if __name__ == '__main__':
    main()
