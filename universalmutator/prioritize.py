from __future__ import print_function
import argparse
import glob

from universalmutator import utils


def main():

    parser = argparse.ArgumentParser(prog="prioritize_mutants",
                                     description="Prioritize a set of mutants using furthest-point-first ranking.")
    parser.add_argument("infile", help="input file (glob pattern supported) listing mutants")
    parser.add_argument("outfile", help="output file for prioritized mutant list")
    parser.add_argument("N", nargs="?", type=int, default=None,
                        help="optional maximum number of mutants to select")
    parser.add_argument("--verbose", action="store_true", default=False,
                        help="produce verbose output")
    parser.add_argument("--noSDPriority", action="store_true", default=False,
                        help="do not prioritize statement deletions over other mutants")
    parser.add_argument("--mutantDir", default=".",
                        help="directory with all mutants; defaults to current directory")
    parser.add_argument("--sourceDir", default=".",
                        help="directory of source files; defaults to current directory")
    parser.add_argument("--cutoff", type=float, default=0.0,
                        help="if minimum distance is less than this value, stop")
    parsed = parser.parse_args()

    infile = parsed.infile
    outfile = parsed.outfile
    verbose = parsed.verbose
    noSDPriority = parsed.noSDPriority
    cutoff = parsed.cutoff

    mdir = parsed.mutantDir
    if mdir[-1] != "/":
        mdir += "/"

    sdir = parsed.sourceDir
    if sdir[-1] != "/":
        sdir += "/"

    N = parsed.N if parsed.N is not None else -1

    infiles = glob.glob(infile)

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
