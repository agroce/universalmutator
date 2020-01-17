from __future__ import print_function

import re
import pkg_resources
import random


def compileRules(ruleFiles):
    rulesText = []

    for ruleFile in ruleFiles:
        if ".rules" not in ruleFile:
            ruleFile += ".rules"
        try:
            with pkg_resources.resource_stream('universalmutator', 'static/' + ruleFile) as builtInRule:
                for line in builtInRule:
                    line = line.decode()
                    rulesText.append((line, "builtin:" + ruleFile))
        except BaseException:
            print("FAILED TO FIND RULE", ruleFile, "AS BUILT-IN...")
            try:
                with open(ruleFile, 'r') as file:
                    for l in file:
                        rulesText.append((l, ruleFile))
            except BaseException:
                print("COULD NOT FIND RULE FILE", ruleFile + "!  SKIPPING...")

    rules = []
    ignoreRules = []
    skipRules = []
    ruleLineNo = 0

    for (r, ruleSource) in rulesText:
        ruleLineNo += 1
        if r == "\n":
            continue
        if " ==> " not in r:
            if " ==>" in r:
                s = r.split(" ==>")
            else:
                if r[0] == "#":  # Don't warn about comments
                    continue
                print("*" * 60)
                print("WARNING:")
                print("RULE:", r, "FROM", ruleSource)
                print("DOES NOT MATCH EXPECTED FORMAT, AND SO WAS IGNORED")
                print("*" * 60)
                continue  # Allow blank lines and comments, just ignore lines without a transformation
        else:
            s = r.split(" ==> ")
        try:
            lhs = re.compile(s[0])
        except BaseException:
            print("*" * 60)
            print("FAILED TO COMPILE RULE:", r, "FROM", ruleSource)
            print("*" * 60)
            continue
        if (len(s[1]) > 0) and (s[1][-1] == "\n"):
            rhs = s[1][:-1]
        else:
            rhs = s[1]
        if rhs == "DO_NOT_MUTATE":
            ignoreRules.append(lhs)
        elif rhs == "SKIP_MUTATING_REST":
            skipRules.append(lhs)
        else:
            rules.append(((lhs, rhs), (r, ruleSource + ":" + str(ruleLineNo))))

    return (rules, ignoreRules, skipRules)


def mutants(source, ruleFiles=["universal.rules"], mutateTestCode=False, mutateBoth=False,
            ignorePatterns=None, ignoreStringOnly=False, fuzzing=False):

    print("MUTATING WITH RULES:", ", ".join(ruleFiles))

    (rules, ignoreRules, skipRules) = compileRules(ruleFiles)

    for p in ignorePatterns:
        try:
            lhs = re.compile(p)
        except BaseException:
            print("*" * 60)
            print("FAILED TO COMPILE IGNORE PATTERN:", p)
            print("*" * 60)
            continue
        ignoreRules.append(lhs)

    mutants = []
    produced = {}
    lineno = 0
    stringSkipped = 0
    inTestCode = False
    if fuzzing:
        # Pick a random target line, ignore others
        if len(source) == 0:
            return []
        targetLine = random.randrange(1, len(source) + 1)
    for l in source:
        lineno += 1
        if fuzzing and (lineno != targetLine):
            continue
        if inTestCode:
            if "@END_TEST_CODE" in l:
                inTestCode = False
            if (not mutateTestCode) and (not mutateBoth):
                continue
        else:
            if "@BEGIN_TEST_CODE" in l:
                inTestCode = True
                continue
            if mutateTestCode and (not mutateBoth):
                continue
        skipLine = False
        for lhs in ignoreRules:
            if lhs.search(l):
                skipLine = True
                break
        if skipLine:
            continue
        abandon = False
        for ((lhs, rhs), ruleUsed) in rules:
            skipPos = len(l)
            for skipRule in skipRules:
                skipp = skipRule.search(l, 0)
                if skipp and (skipp.start() < skipPos):
                    skipPos = skipp.start()
            pos = 0
            p = lhs.search(l, pos)
            while p and (pos < skipPos):
                pos = p.start() + 1
                try:
                    mutant = l[:p.start()] + lhs.sub(rhs, l[p.start():], count=1)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print("WARNING: Applying mutation raised an exception:", e)
                    print("Abandoning mutation of line", lineno)
                    abandon = True
                    break
                if mutant[-1] != "\n":
                    mutant += "\n"
                skipDueToString = False
                if ignoreStringOnly:
                    noStringsOrig = ""
                    inString = False
                    slen = 0
                    for spos in range(0, len(l)):
                        if not inString:
                            noStringsOrig += l[spos]
                            if l[spos] == '"':
                                inString = True
                                slen = 0
                        else:
                            slen += 1
                            if l[spos] == '"':
                                noStringsOrig += str(slen > 2)
                                noStringsOrig += l[spos]
                                inString = False
                    noStringsMutant = ""
                    inString = False
                    slen = 0
                    for spos in range(0, len(mutant)):
                        if not inString:
                            noStringsMutant += mutant[spos]
                            if mutant[spos] == '"':
                                inString = True
                                slen = 0
                        else:
                            slen += 1
                            if mutant[spos] == '"':
                                noStringsMutant += str(slen > 2)
                                noStringsMutant += mutant[spos]
                                inString = False
                    if noStringsOrig == noStringsMutant:
                        skipDueToString = True
                        stringSkipped += 1
                if (mutant != l) and ((lineno, mutant) not in produced) and (not skipDueToString):
                    mutants.append((lineno, mutant, ruleUsed))
                    produced[(lineno, mutant)] = True
                p = lhs.search(l, pos)
            if abandon:
                break

    if stringSkipped > 0:
        print("SKIPPED", stringSkipped, "MUTANTS ONLY CHANGING STRING LITERALS")
    return mutants


def makeMutant(source, mutant, path):
    lineModified = mutant[0]
    newCode = mutant[1]
    with open(path, 'w') as file:
        lineno = 0
        for l in source:
            lineno += 1
            if lineno != lineModified:
                file.write(l)
            else:
                file.write(newCode)
