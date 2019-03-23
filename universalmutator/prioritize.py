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
        print("       --verbose:       produce verbose output")
        print("       --noSDPriority:  do not prioritize statement deletions over other mutants")
        print("       --mutantDir:     directory with all mutants; defaults to current directory")
        print("       --sourceDir:     directory of source files; defaults to current directory")
        print("       --cutoff:        if minimum distance is less than <dist>, stop")
        sys.exit(0)

    infile = sys.argv[1]
    outfile = sys.argv[2]

    infiles = glob.glob(infile)

    verbose = False
    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True

    noSDPriority = False
    if "--noSDPriority" in args:
        args.remove("--noSDPriority")
        noSDPriority = True

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
        N = int(args[3])

    mutants = []
    for f in infiles:
        with open(f, 'r') as mfile:
            for line in mfile:
                name = line[:-1]
                suffix = "." + name.split(".")[-1]
                mpart = ".mutant." + name.split(".mutant.")[1]
                original = sdir + name.replace(mpart, suffix)
                try:
                    mutants.append(utils.readMutant(name, original, mutantDir=mdir))
                except AssertionError:
                    print("WARNING:", name, "AND SOURCE ARE IDENTICAL")
    print("READ", len(mutants), "MUTANTS")

    if N == -1:
        N = len(mutants)

    sdmutants = []
    if not noSDPriority:
        print("IDENTIFYING STATEMENT DELETION MUTANTS")
        for m in mutants:
            if utils.change(m) == "...==>.../*...*/...":
                sdmutants.append(m)
        for m in sdmutants:
            mutants.remove(m)
        print("PRIORITIZING", len(sdmutants), "STATEMENT DELETIONS")
        if len(sdmutants) > 0:
            ranking = utils.FPF(sdmutants, N, cutoff=cutoff, verbose=verbose)
            with open(outfile, 'w') as outf:
                for (m, r) in ranking:
                    mname = m[0]
                    outf.write(mname + "\n")
        print()
    else:
        with open(outfile, 'w') as outf:
            pass

    print("PRIORITIZING", int(N) - len(sdmutants), "MUTANTS")

    ranking = utils.FPF(mutants, N - len(sdmutants), cutoff=cutoff, verbose=verbose, avoid=sdmutants)
    with open(outfile, 'a') as outf:
        for (m, r) in ranking:
            mname = m[0]
            outf.write(mname + "\n")


if __name__ == '__main__':
    main()
