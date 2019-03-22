from __future__ import print_function
import time

import Levenshtein


def show(m):
    (mfile, sourcefile, pos, orig, mutant) = m
    print(mfile + ": " + sourcefile + ":" + str(pos + 1))
    print(orig, end="")
    print(" ==> ", change(m))
    print(mutant, end="")


def change(m):
    (mfile, sourcefile, pos, orig, mutant) = m
    eops = Levenshtein.editops(orig, mutant)
    blocks = Levenshtein.matching_blocks(eops, orig, mutant)
    if len(blocks) > 4:
        return mutant[:-1]
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
        if (pos < len(keep)) and mutant[c] == keep[pos]:
            pos += 1
            if not wasDot:
                notKeep += "..."
                wasDot = True
        else:
            notKeep += mutant[c]
            wasDot = False
    return notKeep


mdistanceCache = {}


def d(m1, m2, changeWeight=5.0, origWeight=0.1, mutantWeight=0.1, codeWeight=0.5, useCache=True):
    global mdistanceCache
    if m1 == m2:
        return 0
    if useCache:
        if (m1, m2) in mdistanceCache:
            return mdistanceCache[(m1, m2)]
    (mfile1, sourcefile1, pos1, orig1, mutant1) = m1
    (mfile2, sourcefile2, pos2, orig2, mutant2) = m2
    d = changeWeight * (1.0 - (Levenshtein.ratio(change(m1), change(m2))))
    d += origWeight * (1.0 - Levenshtein.ratio(orig1, orig2))
    d += mutantWeight * (1.0 - Levenshtein.ratio(mutant1, mutant2))
    if (sourcefile1 != sourcefile2):
        d += codeWeight
    else:
        pd = abs(pos1 - pos2)
        if pd > 10:
            d += codeWeight * 0.5
        else:
            d += codeWeight * (0.5 * (pd / 11.0))
    if useCache:
        mdistanceCache[(m1, m2)] = d
    return d


def FPF(mlist, N, f=None, d=d, cutoff=0.0, verbose=True, avoid=[]):
    start = time.time()
    if f is None:
        ranking = [(mlist[0], -1)]
    else:
        maxf = 0
        best = None
        for m in mlist:
            fm = f(m)
            if fm > maxf:
                best = m
                maxf = fm
        ranking = [(best, -1)]
    if verbose:
        print("*"*80)
        show(ranking[0][0])
    while (len(ranking) < N) and (len(ranking) < len(mlist)):
        best = None
        maxMin = -1
        for m1 in mlist:
            dmin = -1
            for (m2, _) in ranking:
                dm1m2 = d(m1, m2)
                if (dm1m2 < dmin) or (dmin == -1):
                    dmin = dm1m2
            for m2 in avoid:
                dm1m2 = d(m1, m2)
                if (dm1m2 < dmin) or (dmin == -1):
                    dmin = dm1m2
            if dmin > maxMin:
                best = m1
                maxMin = dmin
        if verbose:
            print("*"*80)
            elapsed = time.time() - start
            print("RANKED", len(ranking) + 1, "MUTANTS IN", elapsed, "SECONDS")
            show(best)
            print("DISTANCE:", maxMin)
        ranking.append((best, maxMin))
        if maxMin < cutoff:
            break
    return ranking


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
    assert diffFound, "mutant " + mfile + " and source " + source + " are identical!"
    return (mutant, source, pos, scode[pos], mcode[pos])
