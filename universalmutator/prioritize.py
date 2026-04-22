from __future__ import print_function
import glob
import sys
import argparse

from universalmutator import utils


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("infile",nargs = 1, metavar="<infile>")

    parser.add_argument("outfile",nargs = 1, metavar="<outfile>")

    parser.add_argument("N", nargs = "?", type=int, metavar="[N]")

    parser.add_argument("--addinfile", nargs="+", metavar="<infile2>, <infile3>")

    parser.add_argument("--cutoff", nargs=1, metavar="<dist>",type=float, help="if minimum distance is less than <dist>, stop")

    parser.add_argument("--verbose", help="produce verbose output", action="store_true")

    parser.add_argument("--noSDPriority", action="store_true", help= "do not prioritize statement deletions over other mutants")

    parser.add_argument("--mutantDir", nargs=1, metavar="<dir>", help = "directory with all mutants; defaults to current directory")

    parser.add_argument("--sourceDir", nargs=1, metavar="<dir>", help = "directory of source files; defaults to current directory")

    args = parser.parse_args()

    infile = args.infile

    outfile = args.outfile

    infiles = glob.glob(infile)

    verbose = args.verbose
    if verbose == None:
        verbose = False

    noSDPriority = args.noSDPriority
    if noSDPriority == None:
        noSDPriority = False

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

    
    cutoff = args.cutoff
    if cutoff == None:
        cutoff = 0.0

    N = args.N
    if N == None:
        N = -1

    mutants = []
    for f in infiles:
        with open(f, 'r') as mfile:
            for line in mfile:
                name = line[:-1]
                suffix = "." + name.split(".")[-1]
                mpart = ".mutant." + name.split(".mutant.")[1]
                original = name.replace(mpart, suffix)
                try:
                    mutants.append(utils.readMutant(name, original, mutantDir=mdir, sourceDir=sdir))
                except AssertionError:
                    print("WARNING:", name, "AND SOURCE ARE IDENTICAL")
    print("READ", len(mutants), "MUTANTS")

    if N == -1:
        N = len(mutants)

    sdmutants = []
    if not noSDPriority:
        print("IDENTIFYING STATEMENT DELETION MUTANTS")
        sdmutants = list(filter(utils.isStatementDeletion, mutants))
        for m in sdmutants:
            mutants.remove(m)
        print("PRIORITIZING", len(sdmutants), "STATEMENT DELETIONS")
        if len(sdmutants) > 0:
            ranking = utils.FPF(sdmutants, N, cutoff=cutoff, verbose=verbose, mutantDir=mdir,
                                sourceDir=sdir)
            with open(outfile, 'w') as outf:
                for (m, _) in ranking:
                    mname = m[0]
                    outf.write(mname + "\n")
        else:
            with open(outfile, 'w') as outf:
                pass
        print()
    else:
        with open(outfile, 'w') as outf:
            pass

    print("PRIORITIZING", int(N) - len(sdmutants), "MUTANTS")

    ranking = utils.FPF(mutants, N - len(sdmutants), cutoff=cutoff, verbose=verbose, avoid=sdmutants,
                        mutantDir=mdir, sourceDir=sdir)
    with open(outfile, 'a') as outf:
        for (m, _) in ranking:
            mname = m[0]
            outf.write(mname + "\n")


if __name__ == '__main__':
    main()
