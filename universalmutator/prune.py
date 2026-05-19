from __future__ import print_function
import argparse
import re

from universalmutator import utils


def main():

    parser = argparse.ArgumentParser(prog="prune_mutants",
                                     description="Prune a mutant list using a constraint configuration file.")
    parser.add_argument("infile", help="input file listing mutants")
    parser.add_argument("outfile", help="output file for the pruned mutant list")
    parser.add_argument("config", help="pruning configuration file")
    parser.add_argument("--mutantDir", default=".",
                        help="directory with all mutants; defaults to current directory")
    parser.add_argument("--sourceDir", default=".",
                        help="directory of source files; defaults to current directory")
    parsed = parser.parse_args()

    infile = parsed.infile
    outfile = parsed.outfile
    config = parsed.config

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

    constraints = {}
    constraints["orig"] = []
    constraints["mutant"] = []
    constraints["change"] = []
    constraints["function"] = []
    constraints["contract"] = []
    constraints["source"] = []
    constraints["line"] = []
    for v in constraints.keys():
        constraints["!" + v] = []
    for v in constraints.keys():
        constraints[v + "_RE"] = []

    baseTypes = set()

    with open(config, 'r') as cfile:
        for line in cfile:
            r = line.rstrip('\n')
            (ctype, crule) = r.split(": ", 1)
            if ctype not in constraints:
                print("INVALID CONSTRAINT TYPE IN PRUNING RULE:", line)
            if "_RE" in ctype:
                crule = re.compile(crule)
            baseTypes.add(ctype.replace("_RE", "").replace("!", ""))
            constraints[ctype].append(crule)

    pruned = []

    properties = {}
    for m in mutants:
        prunedYet = False
        (mfile, sourcefile, pos, orig, mutant) = m
        properties["orig"] = orig
        properties["mutant"] = mutant
        properties["line"] = pos
        properties["source"] = sourcefile
        if "change" in baseTypes:
            properties["change"] = utils.change(m)
        if "function" in baseTypes:
            properties["function"] = utils.solidityFunction(m)
        if "contract" in baseTypes:
            properties["contract"] = utils.solidityContract(m)
        for ctype in constraints:
            field = ctype.replace("_RE", "").replace("!", "")
            negated = ctype[0] == "!"
            regexp = "_RE" in ctype
            for c in constraints[ctype]:
                if "line" in ctype:
                    cstart = int(c.split("-")[0])
                    cend = int(c.split("-")[1])
                    matched = (properties[field] >= cstart) and (properties[field] <= cend)
                elif not regexp:
                    matched = c in properties[field]
                else:
                    matched = regexp.search(c, properties[field])
                result = not ((matched is None) or (matched is False))
                if negated:
                    result = not result
                if result:
                    print("=" * 80)
                    print("PRUNING MUTANT DUE TO RULE:", ctype + ":", c)
                    utils.show(m)
                    pruned.append(mfile)
                    prunedYet = True
                    break
            if prunedYet:
                break
    print("=" * 80)
    print("PRUNED", len(pruned), "MUTANTS")
    with open(outfile, 'w') as newmfile:
        for m in mutants:
            if m[0] not in pruned:
                newmfile.write(m[0] + "\n")


if __name__ == '__main__':
    main()
