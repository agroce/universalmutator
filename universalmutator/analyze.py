from __future__ import print_function

import subprocess
import sys
import glob
import shutil
import signal
import time
import random
import os


def main():

    args = sys.argv

    if ("--help" in args) or (len(sys.argv) < 3):
        if len(sys.argv) < 3:
            print("ERROR: analyze_mutants requires at least two arguments\n")
        print("USAGE: analyze_mutants <sourcefile> <cmd> [--mutantDir <dir>] [--fromFile <mutantfile>]")
        print("       <cmd> is command to execute to run tests; non-zero return indicates mutant killed")
        print("       --mutantDir: directory with all mutants; defaults to current directory")
        print("       --fromFile: file containing list of mutants to process; others ignored")
        print("       --timeout <val>: change the timeout setting")
        print("       --verbose: show output of mutants")
        print("       --seed: random seed for shuffling of mutants")
        print("       --noShuffle: do not randomize order of mutants")
        print("       --resume: use existing killed.txt and notkilled.txt, resume mutation analysis")
        print("       --prefix: add a prefix to killed.txt and notkilled.txt")
        sys.exit(0)

    verbose = "--verbose" in sys.argv
    if verbose:
        args.remove("--verbose")

    resume = "--resume" in sys.argv
    if resume:
        args.remove("--resume")

    noShuffle = "--noShuffle" in sys.argv
    if noShuffle:
        args.remove("--noShuffle")

    prefix = None
    try:
        prefixpos = args.index("--prefix")
    except ValueError:
        prefixpos = -1

    if prefixpos != -1:
        prefix = args[prefixpos + 1]
        args.remove("--prefix")
        args.remove(prefix)

    fromFile = None
    try:
        filepos = args.index("--fromFile")
    except ValueError:
        filepos = -1

    if filepos != -1:
        fromFile = args[filepos + 1]
        args.remove("--fromFile")
        args.remove(fromFile)

    seed = None
    try:
        seedpos = args.index("--seed")
    except ValueError:
        seedpos = -1

    if seedpos != -1:
        seed = args[seedpos + 1]
        args.remove("--seed")
        args.remove(seed)
        seed = int(seed)

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
    srcEnd = "." + ((src.split(".")[-1]).split("/")[-1])

    count = 0.0
    killCount = 0.0

    killFileName = "killed.txt"
    notkillFileName = "notkilled.txt"
    if prefix is not None:
        killFileName = prefix + "." + killFileName
        notkillFileName = prefix + "." + notkillFileName

    print("ANALYZING", src)
    print("COMMAND: **", tstCmd, "**")

    allTheMutants = glob.glob(mdir + srcBase.replace(srcEnd, ".mutant*" + srcEnd))

    if onlyMutants is not None:
        newMutants = []
        for f in allTheMutants:
            if f.split("/")[-1] in onlyMutants:
                newMutants.append(f)
        allTheMutants = newMutants

    if seed is not None:
        random.seed(seed)

    if not noShuffle:
        random.shuffle(allTheMutants)

    allStart = time.time()

    if resume:
        alreadyKilled = []
        alreadyNotKilled = []
        if not (os.path.exists(killFileName) and os.path.exists(notkillFileName)):
            print("ATTEMPTING TO RESUME, BUT NO PREVIOUS RESULTS FOUND")
        else:
            with open(killFileName, 'r') as killed:
                with open(notkillFileName, 'r') as notkilled:
                    for line in killed:
                        if line == "\n":
                            continue
                        alreadyKilled.append(line[:-1])
                        count += 1
                        killCount += 1
                    for line in notkilled:
                        if line == "\n":
                            continue
                        alreadyNotKilled.append(line[:-1])
                        count += 1
            print("RESUMING FROM EXISTING RUN, WITH", int(killCount), "KILLED MUTANTS OUT OF", int(count))

    with open(killFileName, 'w') as killed:
        with open(notkillFileName, 'w') as notkilled:
            if resume:
                for line in alreadyKilled:
                    killed.write(line + "\n")
                for line in alreadyNotKilled:
                    notkilled.write(line + "\n")
            for f in allTheMutants:
                if resume:
                    if (f.split("/")[-1] in alreadyKilled) or (f.split("/")[-1] in alreadyNotKilled):
                        continue
                print("#" + str(int(count) + 1) + ":", end=" ")
                print("[" + str(round(time.time() - allStart, 2)) + "s", end=" ")
                print(str(round(count / len(allTheMutants) * 100.0, 2)) + "% DONE]")
                print("  " + f, end=" ")
                if f in ignore:
                    print("SKIPPED")
                try:
                    shutil.copy(src, src + ".um.backup")
                    shutil.copy(f, src)

                    start = time.time()

                    if not verbose:
                        with open(os.devnull, 'w') as dnull:
                            P = subprocess.Popen(
                                tstCmd, shell=True, stderr=dnull, stdout=dnull,
                                preexec_fn=os.setsid)
                    else:
                        P = subprocess.Popen(tstCmd, shell=True, preexec_fn=os.setsid)

                    while P.poll() is None and (time.time() - start) < timeout:
                        time.sleep(0.05)

                    if P.poll() is None:
                        if verbose:
                            print("HAD TO TERMINATE DUE TO TIMEOUT!")
                        os.killpg(os.getpgid(P.pid), signal.SIGTERM)

                    r = P.returncode
                    runtime = time.time() - start

                    count += 1
                    if r == 0:
                        print("NOT KILLED")
                        notkilled.write(f.split("/")[-1] + "\n")
                        notkilled.flush()
                    else:
                        killCount += 1
                        print("KILLED IN", runtime)
                        killed.write(f.split("/")[-1] + "\n")
                        killed.flush()
                    print("  RUNNING SCORE:", killCount / count)
                    sys.stdout.flush()
                finally:
                    shutil.copy(src + ".um.backup", src)
                    os.remove(src + ".um.backup")
    print("MUTATION SCORE:", killCount / count)


if __name__ == '__main__':
    main()
