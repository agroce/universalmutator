from __future__ import print_function
from tabulate import tabulate

import os
import random
import sys
import shutil
import subprocess
import argparse

from universalmutator import mutator

from universalmutator import c_handler
from universalmutator import cpp_handler
from universalmutator import python_handler
from universalmutator import java_handler
from universalmutator import javascript_handler
from universalmutator import swift_handler
from universalmutator import rust_handler
from universalmutator import go_handler
from universalmutator import lisp_handler
from universalmutator import solidity_handler
from universalmutator import vyper_handler
from universalmutator import fe_handler
from universalmutator import r_handler
from universalmutator import fortran_handler

def nullHandler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    return "VALID"

def fastCheckLine(mutant, source, sourceFile, uniqueMutants, compileFile, handler, deadCodeLines, interestingLines, tmpMutantName, lineNo):
    if compileFile is None:
        mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants)
    else:
        mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=compileFile)
    if mutantResult in ["VALID", "REDUNDANT"]:
        deadCodeLines.append(lineNo)
        print("LINE", str(lineNo) + ":", source[lineNo - 1][:-1], end=" ")
        print("APPEARS TO BE COMMENT OR DEAD CODE, SKIPPING...")
    else:
        interestingLines.append(lineNo)

def checkCombyDeadCode(deadCodeLines, mutant):
    for i in range(mutant[3][0], mutant[3][1]+1):
        if i not in deadCodeLines:
            return False
    return True

def cmdHandler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    if "MUTANT" not in cmd:
        # We asssume if the MUTANT isn't part of the command,
        # we need to move it into place, before, e.g., make
        backupName = sourceFile + ".um.backup." + str(os.getpid())
        shutil.copy(sourceFile, backupName)
        shutil.copy(tmpMutantName, sourceFile)
    try:
        with open(".um.mutant_output." + str(os.getpid()), 'w') as file:
            r = subprocess.call([cmd.replace("MUTANT", tmpMutantName)],
                                shell=True, stderr=file, stdout=file)
        if r == 0:
            return "VALID"
        return "INVALID"
    finally:
        # If we moved the mutant in, restore original
        if "MUTANT" not in cmd:
            shutil.copy(backupName, sourceFile)

def toGarbage(code):
    newCode = ""
    for c in code:
        if c == "(":
            newCode += " "
        elif c.isspace() or c in ["*", "/", "#", "-"]:
            newCode += c
        else:
            newCode += "Q"
    return newCode

cmd = None

def main():
    global cmd

    try:
        import custom_handler
    except BaseException:
        pass



    print("*** UNIVERSALMUTATOR ***")

    parser = argparse.ArgumentParser()

    parser.add_argument("sourcefile", help="a file to mutate", metavar="<sourcefile>")

    parser.add_argument("rules", nargs="*", metavar="<rule1> <rule2>", help="any amount of rules")

    parser.add_argument("--language", nargs=1, metavar="<language>")

    parser.add_argument("--noCheck", action="store_true", help="skips compilation/comparison and just generates mutant files")

    parser.add_argument("--cmd",nargs=1, help="executes command string, replacing MUTANT with the mutant name, "
        "and uses return code to determine mutant validity", metavar="<command string>")

    parser.add_argument("--mutantDir", nargs=1, help="directory to put generated mutants in; defaults to current directory", metavar="<dir>")
    
    parser.add_argument("--lines", nargs=1, help="only generate mutants for lines contained in <coverfile>", metavar="<coverfile>")

    parser.add_argument("--tstl", action="store_true", help="<coverfile> is TSTL output")

    parser.add_argument("--mutateInStrings",action="store_true", help="mutate inside strings (not just turn to empty string)")

    parser.add_argument("--mutateTestCode",action="store_true", help="mutate only test code")

    parser.add_argument("--mutateBoth", action="store_true", help="mutate both test and normal code")

    parser.add_argument("--ignore", nargs=1, help="ignore lines matching patterns in <file>", metavar="<file>")

    parser.add_argument("--compile",nargs=1, help="compile <file> instead of source (solidity handler only)", metavar="<file>")

    parser.add_argument("--comby", action="store_true",help="use comby as the method of mutating code")

    parser.add_argument("--noFastCheck", action="store_true", help="do not use fast dead code/comment detection heuristic")

    parser.add_argument("--swap", action="store_true", help="also try adjacent-code swaps")

    parser.add_argument("--redundantOK", action="store_true", help="keep redundant mutants (for compiler output issues)")

    parser.add_argument("--showRules", action="store_true", help="show rule source used to generate each mutant")

    parser.add_argument("--only", nargs=1, help="only use rule file <rule", metavar="<rule>")

    parser.add_argument("--printStat",action="store_true", help="print stats for the rules and generated mutants into files")

    parser.add_argument("--fuzz",action="store_true")

    args = parser.parse_args()

    if args.tstl and not args.lines:
        print("ERROR: Cannot call --tstl without calling --lines!")
        sys.exit(1)

    languages = {".c": "c",
                 ".h": "c",
                 ".cpp": "cpp",
                 ".c++": "cpp",
                 ".cc": "cpp",
                 ".hpp": "cpp",
                 ".py": "python",
                 ".java": "java",
                 ".js": "javascript",
                 ".ts": "javascript",
                 ".swift": "swift",
                 ".rs": "rust",
                 ".go": "go",
                 ".lisp": "lisp",
                 ".lsp": "lisp",
                 ".f": "fortran",
                 ".f90": "fortran",
                 ".for": "fortran",
                 ".R": "r",
                 ".sol": "solidity",
                 ".vy": "vyper",
                 ".fe": "fe"}

    noCheck = args.noCheck

    comby = args.comby

    redundantOK = args.redundantOK

    showRules = args.showRules

    mutateInStrings = args.mutateInStrings

    mutateTestCode = args.mutateTestCode

    mutateBoth = args.mutateBoth

    noFastCheck = args.noFastCheck

    doSwaps = args.swap

    tstl = args.tstl

    # What is this?
    fuzz = args.fuzz

    printStat = args.printStat

    cmd = args.cmd
   
    sourceFile = args.sourcefile
    ending = "." + sourceFile.split(".")[-1]

    lineFile = args.lines
    if lineFile is not None:
        with open(lineFile) as file:
            if not tstl:
                lines = list(map(int, file.read().split()))
            else:
                lines = []
                for l in file:
                    if "LINES" in l:
                        if sourceFile not in l:
                            continue
                        db = l.split("[")[1]
                        d = db[:-2].split(",")
                        for line in d:
                            lines.append(int(line))

    mdir = "."
    if args.mutantDir != None:
        mdir = args.mutantDir
    if mdir[-1] != "/":
        mdir += "/"

    ignoreFile = args.ignore

    compileFile = args.compile


    ignorePatterns = []
    if ignoreFile is not None:
        print("IGNORING PATTERNS DEFINED IN", ignoreFile)
        with open(ignoreFile, 'r') as ignoref:
            for l in ignoref:
                ignorePatterns.append(l[:-1])

    handlers = {"python": python_handler,
                "c": c_handler,
                "c++": cpp_handler,
                "cpp": cpp_handler,
                "java": java_handler,
                "javascript": javascript_handler,
                "swift": swift_handler,
                "rust": rust_handler,
                "r": r_handler,
                "fortran": fortran_handler,
                "go": go_handler,
                "lisp": lisp_handler,
                "solidity": solidity_handler,
                "vyper": vyper_handler,
                "fe": fe_handler}

    cLikeLanguages = [
        "c",
        "java",
        "javascript",
        "swift",
        "cpp",
        "c++",
        "rust",
        "solidity",
        "go"]

    try:
        handlers["custom"] == custom_handler
    except BaseException:
        pass

    sourceFile = args.sourcefile
    base = (".".join((sourceFile.split(".")[:-1]))).split("/")[-1]
    ending = "." + sourceFile.split(".")[-1]

    if args.only == None:
        if  args.language == None or args.rules == None:
            try:
                language = languages[ending]
            except KeyError:
                language = "none"
            otherRules = []
        else:
            language = args.language
            otherRules = args.rules

        if language not in handlers:
            if language.lower() in handlers:
                language = language.lower()

        if language in cLikeLanguages:
            otherRules.append("c_like.rules")

        if language == "vyper":
            otherRules.append("python.rules")
            otherRules.append("solidity.rules")

        if language == "fe":
            otherRules.append("python.rules")
            otherRules.append("solidity.rules")

        rules = ["universal.rules", language + ".rules"] + otherRules
        if fuzz:
            if language == "none":
                fuzzRules = ["universal.rules", "c_like.rules", "python.rules", "vyper.rules", "solidity.rules"]
                rules = list(set(fuzzRules + rules))
    else:
        rules = args.only
        try:
            language = languages[ending]
        except KeyError:
            language = "none"
        
        if language not in handlers:
            if language.lower() in handlers:
                language = language.lower()

    source = []

    with open(sourceFile, 'r') as file:
        for line in file:
            # remove non-ascii characters (comby issue)
            line_processed = line.encode('ascii', 'ignore').decode()
            source.append(line_processed)

    mutants = []

    if comby:
        mutants = mutator.mutants_comby(source, ruleFiles=rules, mutateTestCode=mutateTestCode, mutateBoth=mutateBoth,
                                ignorePatterns=ignorePatterns, ignoreStringOnly=not mutateInStrings, fuzzing=fuzz, language=ending)
    else:
        mutants = mutator.mutants_regexp(source, ruleFiles=rules, mutateTestCode=mutateTestCode, mutateBoth=mutateBoth,
                              ignorePatterns=ignorePatterns, ignoreStringOnly=not mutateInStrings, fuzzing=fuzz)
    if fuzz:
        if len(mutants) == 0:
            sys.exit(255)
        mutants = [random.choice(mutants)]  # Just pick one

    print(len(mutants), "MUTANTS GENERATED BY RULES")

    validMutants = []
    invalidMutants = []
    redundantMutants = []
    uniqueMutants = {}
    sourceJoined = ''

    if comby:
        noFastCheck = True

    dumbHandler = False
    if not noCheck:
        if cmd is not None:
            handler = cmdHandler
        elif language == "none":
            handler = nullHandler
        else:
            try:
                if handlers[language].dumb:
                    noFastCheck = True
                    dumbHandler = True
            except BaseException:
                pass
            handler = handlers[language].handler
    else:
        handler = nullHandler
        noFastCheck = True

    deadCodeLines = []
    interestingLines = []

    tmpMutantName = ".tmp_mutant." + str(os.getpid()) + ending
    mutantNo = 0
    for mutant in mutants:
        if (lineFile is not None) and mutant[0] not in lines:
            # skip if not a line to mutate
            continue
        if not noFastCheck:
            if comby:
                checkLines = []
                for i in range(mutant[3][0], mutant[3][1] + 1):
                    if i not in deadCodeLines or i not in interestingLines:
                        checkLines.append(i)
                for lineNo in checkLines:
                    fastCheckMutant = (lineNo, toGarbage(source[lineNo - 1]))
                    mCreated = mutator.makeMutant(source, fastCheckMutant, tmpMutantName)
                    if mCreated:
                        fastCheckLine(mutant, source, sourceFile, uniqueMutants, compileFile, handler, deadCodeLines, interestingLines, tmpMutantName, lineNo)
                if checkCombyDeadCode(deadCodeLines, mutant):
                    continue
            else:
                if (mutant[0] not in interestingLines) and (mutant[0] not in deadCodeLines):
                    fastCheckMutant = (mutant[0], toGarbage(source[mutant[0] - 1]))
                    mCreated = mutator.makeMutant(source, fastCheckMutant, tmpMutantName)
                    if mCreated:
                        fastCheckLine(mutant, source, sourceFile, uniqueMutants, compileFile, handler, deadCodeLines, interestingLines, tmpMutantName, mutant[0])
                if mutant[0] in deadCodeLines:
                    continue

        if comby:
            sourceJoined = ''.join(source)
            print("PROCESSING MUTANT:",
              "range" + str(mutant[0]) + ":", sourceJoined[mutant[0][0]:mutant[0][1]].replace("\n", "\\n"), " ==> ", mutant[1], end="...")
        else:
            print("PROCESSING MUTANT:",
              str(mutant[0]) + ":", source[mutant[0] - 1][:-1], " ==> ", mutant[1][:-1], end="...")
        if (not comby) and showRules:
            print("(FROM:", mutant[2][1], end=")...")

        if comby:
            mCreated = mutator.makeMutantComby(sourceJoined, mutant, tmpMutantName)
        else:
            mCreated = mutator.makeMutant(source, mutant, tmpMutantName)
        if not mCreated:
            print("REDUNDANT (SOURCE COPY!)")
            redundantMutants.append(mutant)
            continue

        if compileFile is None:
            mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants)
        else:
            mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=compileFile)
        print(mutantResult, end=" ")
        mutantName = mdir + base + ".mutant." + str(mutantNo) + ending
        if fuzz:
            mutantName = mdir + "fuzz.out"
        if (mutantResult == "VALID") or (mutantResult == "REDUNDANT" and redundantOK):
            print("[written to", mutantName + "]", end=" ")
            shutil.copy(tmpMutantName, mutantName)
            validMutants.append(mutant)
            mutantNo += 1
        elif mutantResult == "INVALID":
            invalidMutants.append(mutant)
        elif mutantResult == "REDUNDANT":
            redundantMutants.append(mutant)
        print()
        sys.stdout.flush()

    if doSwaps:
        print("TRYING CODE SWAPS...")
        swapList = []
        for lineNo in range(len(source)):
            if lineNo + 1 in deadCodeLines:
                continue
            swapList.append(lineNo)
        for i in range(0, len(swapList)-1):
            a = swapList[i]
            b = swapList[i+1]
            mutant = [a + 1] # Only the line is valid here
            print("TRYING TO SWAP LINES", a + 1, "AND", b + 1, end="...")
            newSource = source[:a]
            newSource.append(source[b])
            newSource += source[a+1:b]
            newSource.append(source[a])
            newSource += source[b+1:]
            with open(tmpMutantName, 'w') as file:
                for line in newSource:
                    file.write(line)
            if compileFile is None:
                mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants)
            else:
                mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=compileFile)
            print(mutantResult, end=" ")
            mutantName = mdir + base + ".mutant." + str(mutantNo) + ending
            if (mutantResult == "VALID") or (mutantResult == "REDUNDANT" and redundantOK):
                print("[written to", mutantName + "]", end=" ")
                shutil.copy(tmpMutantName, mutantName)
                validMutants.append(mutant)
                mutantNo += 1
            elif mutantResult == "INVALID":
                invalidMutants.append(mutant)
            elif mutantResult == "REDUNDANT":
                redundantMutants.append(mutant)
            print()
            sys.stdout.flush()

    print(len(validMutants), "VALID MUTANTS")
    print(len(invalidMutants), "INVALID MUTANTS")
    print(len(redundantMutants), "REDUNDANT MUTANTS")

    totalMutants = len(validMutants) + len(invalidMutants) + len(redundantMutants)
    valid_rate = 0 if totalMutants == 0 else (len(validMutants) * 100.0)/totalMutants
    print(f"Valid Percentage: {valid_rate}%")

    (rules, _, _) = mutator.parseRules(rules, comby= comby)

    if printStat:
        source = sourceJoined if comby else None
        printMutantsStat((validMutants, invalidMutants, redundantMutants), source)
        printRulesStat(rules, validMutants, invalidMutants)

    if dumbHandler:
        print()
        print("*"*80)
        print("WARNING:  because the handler does not compile and so has no pruning support,")
        print("all mutants were considered valid.  Consider using --cmd to build the target!")
        print("*"*80)
        print()

    try:
        os.remove(tmpMutantName)
    except BaseException:
        pass

def printMutantsStat(mutants, source = None):
    def dumpToFile(fileName, mutants):
        fis = open(fileName, "w")
        i = 0
        for mutant in mutants:
            i += 1
            sys.stdout.flush()

            fis.write(f"{i}.\n")
            fis.write(mutant[2][0])
            fis.write('\n')
            if source is not None:
                fis.write("source:\n")
                fis.write(source[mutant[0][0]:mutant[0][1]])
                fis.write('\n')
            fis.write("mutant:\n")
            fis.write(mutant[1])
            fis.write('\n\n')
        fis.close()

    validMutants, invalidMutants, redundantMutants = mutants
    dumpToFile('valid_mutants.txt', validMutants)
    dumpToFile('invalid_mutants.txt', invalidMutants)
    dumpToFile('redundant_mutants.txt', redundantMutants)

def printRulesStat(rules, validMutants, invalidMutants):
    valid_cnt = {}
    invalid_cnt = {}

    for mutant in validMutants:
        lhs, rhs = mutant[-1]
        if (lhs,rhs) not in valid_cnt:
            valid_cnt[(lhs,rhs)] = 0
        valid_cnt[(lhs,rhs)] += 1

    for mutant in invalidMutants:
        lhs, rhs = mutant[-1]
        if (lhs,rhs) not in invalid_cnt:
            invalid_cnt[(lhs,rhs)] = 0
        invalid_cnt[(lhs,rhs)] += 1

    fis = open("rules_count.txt", "w")
    i = 0
    table = []
    table.append(["#","Rule","No. of Valids", "No. of Invalids"])

    for ((lhs, rhs), _) in rules:
        if (lhs,rhs) not in valid_cnt:
            valid_cnt[(lhs,rhs)] = 0
        if (lhs,rhs) not in invalid_cnt:
            invalid_cnt[(lhs,rhs)] = 0
        i += 1

        table.append([f'{i}',f'{lhs} ==> {rhs}', f'{valid_cnt[(lhs,rhs)]}', f'{invalid_cnt[(lhs,rhs)]}'])

    fis.write(tabulate(table,tablefmt="grid"))
    sys.stdout.flush()
    fis.close()

if __name__ == '__main__':
    main()
