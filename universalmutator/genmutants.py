from __future__ import print_function

import os
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


def nullHandler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    return "VALID"


def cmdHandler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    global cmd

    with open(".um.mutant_output." + str(os.getpid()), 'w') as file:
        r = subprocess.call([cmd.replace("MUTANT", tmpMutantName)],
                            shell=True, stderr=file, stdout=file)
    if r == 0:
        return "VALID"
    else:
        return "INVALID"


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
                 ".vy": "vyper"}

    print("*** UNIVERSALMUTATOR ***")

    if ("--help" in args) or (len(sys.argv) < 2):
        if len(sys.argv) < 2:
            print("ERROR: mutate requires at least one argument (a file to mutate)\n")
        print("USAGE: mutate <sourcefile> [<language>] [<rule1> <rule2>...]",
              "[--noCheck] [--cmd <command string>] [--mutantDir <dir>]",
              "[--lines <coverfile> [--tstl]]")
        print()
        print("       --noCheck: skips compilation/comparison and just generates mutant files")
        print("       --cmd executes command string, replacing MUTANT with the mutant name, and uses return code")
        print("             to determine mutant validity")
        print("       --mutantDir: directory to put generated mutants in; defaults to current directory")
        print("       --lines: only generate mutants for lines contained in <coverfile>")
        print("       --tstl: <coverfile> is TSTL output")
        print()
        print("Currently supported languages: ", ", ".join(list(set(languages.values()))))
        sys.exit(0)

    noCheck = False
    if "--noCheck" in args:
        noCheck = True
        args.remove("--noCheck")

    cmd = None
    try:
        cmdpos = args.index("--cmd")
    except ValueError:
        cmdpos = -1

    tstl = False
    if "--tstl" in args:
        tstl = True
        args.remove("--tstl")

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
                lines = map(int, file.read().split())
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

    mdir = ""
    try:
        mdirpos = args.index("--mutantDir")
    except ValueError:
        mdirpos = -1

    if mdirpos != -1:
        mdir = args[mdirpos + 1]
        args.remove("--mutantDir")
        args.remove(mdir)
        mdir += "/"

    handlers = {"python": python_handler,
                "c": c_handler,
                "c++": cpp_handler,
                "cpp": cpp_handler,
                "java": java_handler,
                "swift": swift_handler,
                "rust": rust_handler,
                "go": go_handler,
                "solidity": solidity_handler,
                "vyper": vyper_handler}

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
        language = languages[ending]
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

    rules = ["universal.rules", language + ".rules"] + otherRules

    source = []

    with open(sourceFile, 'r') as file:
        for l in file:
            source.append(l)

    mutants = mutator.mutants(source, rules=rules)

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

    tmpMutantName = ".tmp_mutant." + str(os.getpid()) + ending
    mutantNo = 0
    for mutant in mutants:
        if (lineFile is not None) and mutant[0] not in lines:
            # skip if not a line to mutate
            continue
        print("PROCESSING MUTANT:",
              str(mutant[0]) + ":", source[mutant[0] - 1][:-1], " ==> ", mutant[1][:-1], end="...")
        mutator.makeMutant(source, mutant, tmpMutantName)
        mutantResult = handler(
            tmpMutantName,
            mutant,
            sourceFile,
            uniqueMutants)
        print(mutantResult, end=" ")
        mutantName = mdir + base + ".mutant." + str(mutantNo) + ending
        if mutantResult == "VALID":
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
