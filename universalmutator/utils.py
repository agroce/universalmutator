import Levenshtein


def changeString(m):
    (mfile, sourcefile, pos, orig, mutant) = m
    eops = Levenshtein.editops(orig, mutant)
    blocks = Levenshtein.matching_blocks(eops, orig, mutant)
    if len(blocks) > 4:
        return mutant
    keep = ''.join([orig[x[0]:x[0]+x[2]] for x in blocks])
    notKeep = ""
    pos = 0
    wasDot = False
    for c in range(0, len(orig)):
        if orig[c] == keep[pos]:
            pos += 1
            if not wasDot:
                notKeep += "..."
                wasDot = True
        else:
            notKeep += orig[c]
            wasDot = False
    notKeep += "==>"
    pos = 0
    wasDot = False
    for c in range(0, len(mutant)):
        if mutant[c] == keep[pos]:
            pos += 1
            if not wasDot:
                notKeep += "..."
                wasDot = True
        else:
            notKeep += mutant[c]
            wasDot = False
    return notKeep


def readMutant(mutant, source, mutantDir=None):
    mfile = mutant
    if mutantDir is not None:
        mfile = mutantDir + "/" + mfile
    with open(source, 'r') as readSource:
        scode = readSource.readlines()
    with open(mfile, 'r') as readmfile:
        mcode = readmfile.readlines()
    pos = 0
    # We expect one location of change, contiguous
    diffFound = False
    for line in scode:
        if line != mcode[pos]:
            diffFound = True
            break
        pos += 1
    assert diffFound, "mutant and source are identical!"
    return (mutant, source, pos, scode[pos], mcode[pos])
