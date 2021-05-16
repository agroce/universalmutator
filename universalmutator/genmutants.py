from __future__ import print_function

import os
import random
import sys
import shutil
import subprocess

import universalmutator.mutator as mutator

import universalmutator.python_handler as python_handler
import universalmutator.c_handler as c_handler
import universalmutator.cpp_handler as cpp_handler
import universalmutator.java_handler as java_handler
import universalmutator.swift_handler as swift_handler
import universalmutator.rust_handler as rust_handler
import universalmutator.go_handler as go_handler
import universalmutator.solidity_handler as solidity_handler
import universalmutator.vyper_handler as vyper_handler
import universalmutator.fe_handler as fe_handler


def nullHandler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    return "VALID"


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
        if c.isspace() or c in ["*", "/", "#", "-"]:
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
                 ".cpp": "cpp",
                 ".c++": "cpp",
                 ".py": "python",
                 ".java": "java",
                 ".swift": "swift",
                 ".rs": "rust",
                 ".go": "go",
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
              "[--redundantOK] [--showRules]")
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
        print("       --noFastCheck: do not use fast dead code/comment detection heuristic")
        print("       --swap: also try adjacent-code swaps")
        print("       --redundantOK: keep redundant mutants (for compiler output issues)")
        print("       --showRules: show rule source used to generate each mutant")
        print()
        print("Currently supported languages: ", ", ".join(list(set(languages.values()))))
        sys.exit(0)

    noCheck = False
    if "--noCheck" in args:
        noCheck = True
        args.remove("--noCheck")

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

    cmd = None
    try:
        cmdpos = args.index("--cmd")
    except ValueError:
        cmdpos = -1

    tstl = False
    if "--tstl" in args:
        tstl = True
        args.remove("--tstl")

    fuzz = False
    if "--fuzz" in args:
        fuzz = True
        args.remove("--fuzz")

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
                "swift": swift_handler,
                "rust": rust_handler,
                "go": go_handler,
                "solidity": solidity_handler,
                "vyper": vyper_handler,
                "fe": fe_handler}

    cLikeLanguages = [
        "c",
        "java",
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

    source = []

    with open(sourceFile, 'r') as file:
        for l in file:
            source.append(l)

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

    if not noCheck:
        if cmd is not None:
            handler = cmdHandler
        elif language == "none":
            handler = nullHandler
        else:
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
        if (not noFastCheck) and (mutant[0] not in interestingLines) and (mutant[0] not in deadCodeLines):
            fastCheckMutant = (mutant[0], toGarbage(source[mutant[0] - 1]))
            mutator.makeMutant(source, fastCheckMutant, tmpMutantName)
            if compileFile is None:
                mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants)
            else:
                mutantResult = handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=compileFile)
            if mutantResult in ["VALID", "REDUNDANT"]:
                deadCodeLines.append(mutant[0])
                print("LINE", str(mutant[0]) + ":", source[mutant[0] - 1][:-1], end=" ")
                print("APPEARS TO BE COMMENT OR DEAD CODE, SKIPPING...")
            else:
                interestingLines.append(mutant[0])
        if mutant[0] in deadCodeLines:
            continue
        print("PROCESSING MUTANT:",
              str(mutant[0]) + ":", source[mutant[0] - 1][:-1], " ==> ", mutant[1][:-1], end="...")
        if showRules:
            print("(FROM:", mutant[2][1], end=")...")
        mutator.makeMutant(source, mutant, tmpMutantName)
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

    try:
        os.remove(tmpMutantName)
    except BaseException:
        pass


if __name__ == '__main__':
    main()
