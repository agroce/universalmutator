"""Tact handler.

By default the handler performs a compile check with:

  tact --check <source-file>

It runs from the source file directory so relative imports continue to work.

To override the command, set:

  UM_TACT_CMD='tact --check MUTANT'

The command must return exit code 0 for a valid mutant. If the string "MUTANT"
is not present, the handler will temporarily swap the mutant into the source
file before running the command (same behavior as genmutants --cmd).
"""

from __future__ import annotations

import os
import shutil
import subprocess


dumb = False


def _override_command():
    return os.environ.get("UM_TACT_CMD") or None


def _keep_temp_files():
    value = (os.environ.get("UM_KEEP_TEMP") or "").strip().lower()
    return value not in ("", "0", "false", "no")


def _cleanup_files(*paths):
    if _keep_temp_files():
        return
    for path in paths:
        if path is None:
            continue
        try:
            os.remove(path)
        except OSError:
            pass


def _default_command(target):
    workdir = os.path.dirname(os.path.abspath(target)) or "."
    command = subprocess.list2cmdline(["tact", "--check", os.path.basename(target)])
    return (command, workdir, True)


def _run_command(command, outFile, cwd, shell):
    with open(outFile, "w") as f:
        try:
            return subprocess.call(
                command,
                shell=shell,
                cwd=cwd,
                stderr=f,
                stdout=f,
            )
        except OSError as exc:
            f.write("FAILED TO RUN COMPILER: " + str(exc) + "\n")
            return 127


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants, compileFile=None):
    target = compileFile if compileFile is not None else sourceFile
    pid = os.getpid()
    backupName = None
    outFile = os.path.abspath(f".um.tact_output.{pid}")
    configured = _override_command()

    if configured is None:
        command, cwd, shell = _default_command(target)
        needsSwap = True
    else:
        command = configured.replace("MUTANT", tmpMutantName)
        cwd = None
        shell = True
        needsSwap = "MUTANT" not in configured

    if needsSwap:
        backupName = target + ".um.backup." + str(pid)
        shutil.copy(target, backupName)
        shutil.copy(tmpMutantName, target)

    try:
        r = _run_command(command, outFile, cwd, shell)
        return "VALID" if r == 0 else "INVALID"
    finally:
        if backupName is not None:
            shutil.copy(backupName, target)
        _cleanup_files(backupName, outFile)
