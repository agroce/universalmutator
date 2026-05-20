"""FunC handler.

By default the handler performs a compile check with:

  npx -y @ton-community/func-js <source-file> --fift <artifact.fif>

It runs from the source file directory so relative includes continue to work.

To override the command, set:

  UM_FUNC_CMD='npx -y @ton-community/func-js MUTANT --fift /tmp/func-out.fif'

The command must return exit code 0 for a valid mutant. If the string
"MUTANT" is not present, the handler will temporarily swap the mutant into the
source file before running the command (same behavior as genmutants --cmd).

Note that func-js performs a full compile and therefore requires a main
entrypoint even when you only request --fift or --artifact output.
"""

from __future__ import annotations

import os
import shutil
import subprocess


dumb = False


def _override_command():
    return os.environ.get("UM_FUNC_CMD") or None


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


def _default_command(target, pid):
    workdir = os.path.dirname(os.path.abspath(target)) or "."
    artifact = os.path.abspath(f".um.func_output.{pid}.fif")
    command = subprocess.list2cmdline(
        ["npx", "-y", "@ton-community/func-js", os.path.basename(target), "--fift", artifact]
    )
    return (command, workdir, True, artifact)


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
    artifact = None
    outFile = os.path.abspath(f".um.func_log.{pid}")
    configured = _override_command()

    if configured is None:
        command, cwd, shell, artifact = _default_command(target, pid)
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
        _cleanup_files(backupName, outFile, artifact)
