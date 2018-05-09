from __future__ import print_function

import subprocess
import sys
import glob
import shutil
import time
import os


def main():

    args = sys.argv

    if "--help" in args:
        print("USAGE: analyze_mutants <sourcefile> <cmd> [--mutantDir <dir>] [--fromFile <mutantfile>]")
        print("       <cmd> is command to execute to run tests")
        print("       --mutantDir: directory to put generated mutants in; defaults to current directory")
        print("       --fromFile: file containing list of mutants to process; others ignored")
        print("       --timeout <val>: change the timeout setting")
        print("       --verbose: show output of mutants")
        sys.exit(0)

    verbose = "--verbose" in sys.argv
    if verbose:
        args.remove("--verbose")

    fromFile = None
    try:
        filepos = args.index("--fromFile")
    except ValueError:
        filepos = -1

    if filepos != -1:
        fromFile = args[filepos + 1]
        args.remove("--fromFile")
        args.remove(fromFile)

    timeout = 30
    try:
        topos = args.index("--timeout")
    except ValueError:
        topos = -1

    if topos != -1:
        timeout = args[topos + 1]
        args.remove("--timeout")
        args.remove(timeout)
        timeout = float(timeout)

    onlyMutants = None
    if fromFile is not None:
        with open(fromFile, 'r') as file:
            onlyMutants = file.read().split()

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

    src = args[1]
    tstCmd = [args[2]]
    ignore = []
    if len(args) > 3:
        with open(sys.argv[3]) as file:
            for l in file:
                ignore.append(l.split()[0])

    srcBase = src.split("/")[-1]
    srcEnd = (src.split(".")[-1]).split("/")[-1]

    count = 0.0
    killCount = 0.0

    print("ANALYZING", src)
    print("COMMAND: **", tstCmd, "**")

    with open("killed.txt", 'w') as killed:
        with open("notkilled.txt", 'w') as notkilled:
            for f in glob.glob(
                mdir +
                srcBase.replace(
                    srcEnd,
                    "mutant.*." +
                    srcEnd)):
                if (onlyMutants is not None) and (
                        f.split("/")[-1] not in onlyMutants):
                    continue
                print(f, end=" ")
                if f in ignore:
                    print("SKIPPED")
                try:
                    shutil.copy(src, src + ".um.backup")
                    shutil.copy(f, src)

                    start = time.time()

                    if not verbose:
                        with open(os.devnull, 'w') as dnull:
                            P = subprocess.Popen(
                                tstCmd, shell=True, stderr=dnull, stdout=dnull)
                    else:
                        P = subprocess.Popen(tstCmd, shell=True)

                    while P.poll() is None and (time.time() - start) < timeout:
                        time.sleep(0.05)

                    if P.poll() is None:
                        if verbose:
                            print("HAD TO TERMINATE DUE TO TIMEOUT!")
                        P.terminate()

                    r = P.returncode

                    count += 1
                    if r == 0:
                        print("NOT KILLED")
                        notkilled.write(f + "\n")
                        notkilled.flush()
                    else:
                        killCount += 1
                        print("KILLED")
                        killed.write(f + "\n")
                        killed.flush()
                finally:
                    shutil.copy(src + ".um.backup", src)
                    os.remove(src + ".um.backup")
    print("MUTATION SCORE:", killCount / count)


if __name__ == '__main__':
    main()
