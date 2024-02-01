from __future__ import print_function
from tabulate import tabulate

import os
import random
from re import T
import sys
import shutil
import subprocess

import universalmutator.mutator as mutator

import universalmutator.c_handler as c_handler
import universalmutator.cpp_handler as cpp_handler
import universalmutator.python_handler as python_handler
import universalmutator.java_handler as java_handler
import universalmutator.javascript_handler as javascript_handler
import universalmutator.swift_handler as swift_handler
import universalmutator.rust_handler as rust_handler
import universalmutator.go_handler as go_handler
import universalmutator.lisp_handler as lisp_handler
import universalmutator.solidity_handler as solidity_handler
import universalmutator.vyper_handler as vyper_handler
import universalmutator.fe_handler as fe_handler
import universalmutator.r_handler as r_handler
import universalmutator.fortran_handler as fortran_handler

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
    global cmd

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
        else:
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


def main():
    global cmd

    try:
        import custom_handler
    except BaseException:
        pass

    args = sys.argv

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

    print("*** UNIVERSALMUTATOR ***")

    if ("--help" in args) or (len(sys.argv) < 2):
        if len(sys.argv) < 2:
            print("ERROR: mutate requires at least one argument (a file to mutate)\n")
        print("USAGE: mutate <sourcefile> [<language>] [<rule1> <rule2>...]",
              "[--noCheck] [--cmd <command string>] [--mutantDir <dir>]",
              "[--lines <coverfile> [--tstl]] [--mutateTestCode] [--mutateBoth]",
              "[--ignore <file>] [--compile <file>] [--noFastCheck] [--swap]",
              "[--redundantOK] [--showRules] [--only <rule>]")
        print()
        print("       --noCheck: skips compilation/comparison and just generates mutant files")
        print("       --cmd executes command string, replacing MUTANT with the mutant name, and uses return code")
        print("             to determine mutant validity")
        print("       --mutantDir: directory to put generated mutants in; defaults to current directory")
        print("       --lines: only generate mutants for lines contained in <coverfile>")
        print("       --tstl: <coverfile> is TSTL output")
        print("       --mutateInStrings: mutate inside strings (not just turn to empty string)")
        print("       --mutateTestCode: mutate only test code")
        print("       --mutateBoth: mutate both test and normal code")
        print("       --ignore <file>: ignore lines matching patterns in <file>")
        print("       --compile <file>: compile <file> instead of source (solidity handler only)")
        print("       --comby: use comby as the method of mutating code")
        print("       --noFastCheck: do not use fast dead code/comment detection heuristic")
        print("       --swap: also try adjacent-code swaps")
        print("       --redundantOK: keep redundant mutants (for compiler output issues)")
        print("       --showRules: show rule source used to generate each mutant")
        print("       --only <rule>: only use rule file <rule>")
        print("       --printStat: print stats for the rules and generated mutants into files")
        print()
        print("Currently supported languages: ", ", ".join(list(set(languages.values()))))
        print("If not supplying a command to compile/build, you should use --noCheck for C, C++,")
        print("javascript, and other languages with only a default handler.")
        sys.exit(0)

    noCheck = False
    if "--noCheck" in args:
        noCheck = True
        args.remove("--noCheck")

    comby = False
    if "--comby" in args:
        comby = True
        args.remove("--comby")

    redundantOK = False
    if "--redundantOK" in args:
        redundantOK = True
        args.remove("--redundantOK")

    showRules = False
    if "--showRules" in args:
        showRules = True
        args.remove("--showRules")

    mutateInStrings = False
    if "--mutateInStrings" in args:
        mutateInStrings = True
        args.remove("--mutateInStrings")

    mutateTestCode = False
    if "--mutateTestCode" in args:
        mutateTestCode = True
        args.remove("--mutateTestCode")

    mutateBoth = False
    if "--mutateBoth" in args:
        mutateBoth = True
        args.remove("--mutateBoth")

    noFastCheck = False
    if "--noFastCheck" in args:
        noFastCheck = True
        args.remove("--noFastCheck")

    doSwaps = False
    if "--swap" in args:
        doSwaps = True
        args.remove("--swap")

    tstl = False
    if "--tstl" in args:
        tstl = True
        args.remove("--tstl")

    fuzz = False
    if "--fuzz" in args:
        fuzz = True
        args.remove("--fuzz")

    printStat = False
    if "--printStat" in args:
        printStat = True
        args.remove("--printStat")

    cmd = None
    try:
        cmdpos = args.index("--cmd")
    except ValueError:
        cmdpos = -1

    if cmdpos != -1:
        cmd = args[cmdpos + 1]
        args.remove("--cmd")
        args.remove(cmd)

    sourceFile = args[1]
    ending = "." + sourceFile.split(".")[-1]

    lineFile = None
    try:
        linepos = args.index("--lines")
    except ValueError:
        linepos = -1

    if linepos != -1:
        lineFile = args[linepos + 1]
        args.remove("--lines")
        args.remove(lineFile)

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
    try:
        mdirpos = args.index("--mutantDir")
    except ValueError:
        mdirpos = -1

    if mdirpos != -1:
        mdir = args[mdirpos + 1]
        args.remove("--mutantDir")
        args.remove(mdir)
    if mdir[-1] != "/":
        mdir += "/"

    ignoreFile = None
    try:
        ignorepos = args.index("--ignore")
    except ValueError:
        ignorepos = -1

    if ignorepos != -1:
        ignoreFile = args[ignorepos + 1]
        args.remove("--ignore")
        args.remove(ignoreFile)

    compileFile = None
    try:
        compilepos = args.index("--compile")
    except ValueError:
        compilepos = -1

    if compilepos != -1:
        compileFile = args[compilepos + 1]
        args.remove("--compile")
        args.remove(compileFile)

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

    sourceFile = args[1]
    ending = "." + sourceFile.split(".")[-1]

    if len(args) < 3:
        try:
            language = languages[ending]
        except KeyError:
            language = "none"
        otherRules = []
    else:
        if ".rules" in args[2]:
            language = languages[ending]
            otherRules = args[2:]
        else:
            language = args[2]
            otherRules = args[3:]

    if language not in handlers:
        if language.lower() in handlers:
            language = language.lower()

    base = (".".join((sourceFile.split(".")[:-1]))).split("/")[-1]

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

    if "--only" in args:
        onlyPos = args.index("--only")
        rules = [args[onlyPos + 1]]

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
        mutants = mutator.mutants(source, ruleFiles=rules, mutateTestCode=mutateTestCode, mutateBoth=mutateBoth,
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
            except:
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
        if (not noFastCheck):
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
            if (lineNo + 1) in deadCodeLines:
                continue
            swapList.append(lineNo)
        for i in range(0, len(swapList)-1):
            a = swapList[i]
            b = swapList[i+1]
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
    
    (rules, ignoreRules, skipRules) = mutator.parseRules(rules, comby= comby)

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
            fis.write(mutant[2][0]); fis.write('\n')
            if source is not None:
                fis.write("source:\n"); fis.write(source[mutant[0][0]:mutant[0][1]]); fis.write('\n')
            fis.write("mutant:\n"); fis.write(mutant[1]); fis.write('\n\n')
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

    for ((lhs, rhs), ruleUsed) in rules:
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
