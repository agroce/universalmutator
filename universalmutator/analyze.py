from __future__ import print_function

import difflib
import subprocess
import sys
import platform
import glob
import shutil
import signal
import time
import random
import os
import py_compile
import argparse

def main():

    isWindows = platform.system()

    parser = argparse.ArgumentParser()

    parser.add_argument("sourcefile", help="a file to mutate", metavar="<sourcefile>")

    parser.add_argument("cmd", help="<cmd> is command to execute to run tests; non-zero return indicates mutant killed", metavar="<cmd>")

    parser.add_argument("--mutantDir", help ="directory with all mutants; defaults to current directory", nargs = 1, metavar="<dir>")

    parser.add_argument("--fromFile", help="file containing list of mutants to process; others ignored", nargs=1, metavar="<mutantfile>")

    parser.add_argument("--timeout",nargs=1, help = "change the timeout setting", metavar="val",type=int)

    parser.add_argument("--show", action="store_true", help="show mutants")

    parser.add_argument("--verbose", help="show mutants and output of analysis", action="store_true")

    parser.add_argument("--seed", help="random seed for shuffling of mutants", nargs=1, type=int, metavar="<integer seed>")

    parser.add_argument("--noShuffle", help="do not randomize order of mutants", action="store_true")

    parser.add_argument("--resume", help="use existing killed.txt and notkilled.txt, resume mutation analysis", action="store_true")

    parser.add_argument("--prefix", help="add a prefix to killed.txt and notkilled.txt", nargs=1, metavar="<prefix>")

    parser.add_argument("--numMutants", help="run with specific number of mutants", nargs=1, metavar="<int>", type=int)

    parser.add_argument("--compileCommand", help="compile command to run in selecting mutants", action="store_true")

    args = parser.parse_args()

    verbose = args.verbose

    showM = args.show

    resume = args.resume

    noShuffle = args.noShuffle

    prefix = args.prefix


    fromFile = args.fromFile
    
    seed = args.seed

    timeout = args.timeout
    if timeout == None:
        timeout=30

    numMutants = args.numMutants
    if(numMutants == None):
        numMutants = -1

    compileCommand = args.compileCommand

    onlyMutants = None
    
    if fromFile is not None:
        with open(fromFile, 'r') as file:
            onlyMutants = file.read().split()

    mdir= args.mutantDir
    if mdir == None:
        mdir = "."
    if mdir[-1] != "/":
        mdir += "/"

    src = args.sourcefile
    tstCmd = args.cmd
    ignore = []
    if args.fromfile != None:
        with open(args.fromfile) as file:
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
        for f1 in onlyMutants:
            for f2 in allTheMutants:
                if f2.split("/")[-1] == f1:
                    newMutants.append(f2)
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

    # numMutants = -1 implies no --numMutants argument was provided
    totalMutants = min(numMutants, len(allTheMutants)) if numMutants > 0 else len(allTheMutants)

    with open(os.devnull, 'w') as dnull:
        with open(killFileName, 'w') as killed:
            with open(notkillFileName, 'w') as notkilled:
                if resume:
                    for line in alreadyKilled:
                        killed.write(line + "\n")
                        killed.flush()
                    for line in alreadyNotKilled:
                        notkilled.write(line + "\n")
                        notkilled.flush()
                for f in allTheMutants:
                    if resume:
                        if (f.split("/")[-1] in alreadyKilled) or (f.split("/")[-1] in alreadyNotKilled):
                            continue
                    if f in ignore:
                        print(f, "SKIPPED")
                    if numMutants != -1 and compileCommand is not None:
                        if runCmd(compileCommand, src, f) != "VALID":
                            continue

                    print("=" * 80)
                    print("#" + str(int(count) + 1) + ":", end=" ")
                    print("[" + str(round(time.time() - allStart, 2)) + "s", end=" ")
                    print(str(round(count / totalMutants * 100.0, 2)) + "% DONE]")
                    if verbose or showM:
                        print("MUTANT:", f)
                        with open(src, 'r') as ff:
                            fromLines = ff.readlines()
                        with open(f, 'r') as tf:
                            toLines = tf.readlines()
                        diff = difflib.context_diff(fromLines, toLines, "Original", "Mutant")
                        print(''.join(diff))
                        print()
                        sys.stdout.flush()
                    print("RUNNING", f + "...")
                    sys.stdout.flush()
                    try:
                        shutil.copy(src, src + ".um.backup")
                        shutil.copy(f, src)
                        if srcEnd == ".py":
                            py_compile.compile(src)

                        if isWindows:
                            ctstCmd = ['set "CURRENT_MUTANT_SOURCE=' + f + '" && ' + tstCmd[0]]
                        else:
                            ctstCmd = ['export CURRENT_MUTANT_SOURCE="' + f + '"; ' + tstCmd[0]]
                        start = time.time()

                        if not verbose:
                            if isWindows:
                                P = subprocess.Popen(ctstCmd, shell=True, stderr=dnull, stdout=dnull,
                                                 start_new_session=True)
                            else:
                                P = subprocess.Popen(ctstCmd, shell=True, stderr=dnull, stdout=dnull,
                                                 preexec_fn=os.setsid)
                        else:
                            if isWindows:
                                P = subprocess.Popen(ctstCmd, shell=True, start_new_session=True)
                            else:
                                P = subprocess.Popen(ctstCmd, shell=True, preexec_fn=os.setsid)

                        try:
                            while P.poll() is None and (time.time() - start) < timeout:
                                time.sleep(0.05)
                        finally:
                            if P.poll() is None:
                                print()
                                print("HAD TO TERMINATE ANALYSIS (TIMEOUT OR EXCEPTION)")

                                if isWindows:
                                    os.kill(P.pid, signal.SIGTERM)
                                else:
                                    os.killpg(os.getpgid(P.pid), signal.SIGTERM)

                                # Avoid any weird race conditions from grabbing the return code
                                time.sleep(0.05)
                            r = P.returncode

                        runtime = time.time() - start

                        count += 1
                        if numMutants != -1 and count >= numMutants:
                            break
                        if r == 0:
                            print(f, "NOT KILLED")
                            notkilled.write(f.split("/")[-1] + "\n")
                            notkilled.flush()
                        else:
                            killCount += 1
                            print(f, "KILLED IN", runtime, "(RETURN CODE", str(r) + ")")
                            killed.write(f.split("/")[-1] + "\n")
                            killed.flush()
                        print("  RUNNING SCORE:", killCount / count)
                        sys.stdout.flush()
                    finally:
                        shutil.copy(src + ".um.backup", src)
                        os.remove(src + ".um.backup")
                if os.path.exists(".um.mutant_output." + str(os.getpid())):
                    os.remove(".um.mutant_output." + str(os.getpid()))

    print("=" * 80)

    if count == 0:
        print("!!! No valid mutants found! Make sure you specified the right mutant directory !!!")
        return
    print("MUTATION SCORE:", killCount / count)


def runCmd(cmd, sourceFile, mutantFile):
    if "MUTANT" not in cmd:
        # We asssume if the MUTANT isn't part of the command,
        # we need to move it into place, before, e.g., make
        backupName = sourceFile + ".um.backup." + str(os.getpid())
        shutil.copy(sourceFile, backupName)
        shutil.copy(mutantFile, sourceFile)
    try:
        with open(".um.mutant_output." + str(os.getpid()), 'w') as file:
            r = subprocess.call([cmd.replace("MUTANT", mutantFile)],
                                shell=True, stderr=file, stdout=file)
        if r == 0:
            return "VALID"
        return "INVALID"
    finally:
        # If we moved the mutant in, restore original
        if "MUTANT" not in cmd:
            shutil.copy(backupName, sourceFile)


if __name__ == '__main__':
    main()
