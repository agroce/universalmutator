from __future__ import print_function
import argparse

from universalmutator import utils


def main():

    parser = argparse.ArgumentParser(prog="show_mutants",
                                     description="Display mutants listed in an input file.")
    parser.add_argument("infile", help="input file listing mutants")
    parser.add_argument("--concise", action="store_true", default=False,
                        help="display in concise mutant format")
    parser.add_argument("--mutantDir", default=".",
                        help="directory with all mutants; defaults to current directory")
    parser.add_argument("--sourceDir", default=".",
                        help="directory of source files; defaults to current directory")
    parsed = parser.parse_args()

    infile = parsed.infile
    concise = parsed.concise

    mdir = parsed.mutantDir
    if mdir[-1] != "/":
        mdir += "/"

    sdir = parsed.sourceDir
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
