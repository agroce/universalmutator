from __future__ import print_function

import os
import subprocess
import sys
from unittest import TestCase


class TestTONExamples(TestCase):
    def setUp(self):
        os.chdir("examples")
        repo_root = os.path.abspath("..")
        self.subprocess_env = os.environ.copy()
        existing_pythonpath = self.subprocess_env.get("PYTHONPATH")
        if existing_pythonpath:
            self.subprocess_env["PYTHONPATH"] = repo_root + os.pathsep + existing_pythonpath
        else:
            self.subprocess_env["PYTHONPATH"] = repo_root

    def tearDown(self):
        # Clean up generated mutants
        for fn in os.listdir("."):
            if ".mutant." in fn:
                try:
                    os.remove(fn)
                except Exception:
                    pass
        if os.path.exists(".tmp_mutant." + str(os.getpid()) + ".tact"):
            try:
                os.remove(".tmp_mutant." + str(os.getpid()) + ".tact")
            except Exception:
                pass
        if os.path.exists(".tmp_mutant." + str(os.getpid()) + ".fc"):
            try:
                os.remove(".tmp_mutant." + str(os.getpid()) + ".fc")
            except Exception:
                pass
        if os.path.exists(".tmp_mutant." + str(os.getpid()) + ".tolk"):
            try:
                os.remove(".tmp_mutant." + str(os.getpid()) + ".tolk")
            except Exception:
                pass

        os.chdir("..")

    def _run_mutate(self, filename, language, rulefile):
        with open("mutate.out", "w") as f:
            r = subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "universalmutator.genmutants",
                    filename,
                    language,
                    "--only",
                    rulefile,
                    "--noCheck",
                ],
                stdout=f,
                stderr=f,
                env=self.subprocess_env,
            )
        self.assertEqual(r, 0)
        with open("mutate.out", "r") as f:
            out = f.read()
        self.assertIn("MUTANTS GENERATED", out)
        # Ensure at least one mutant was produced
        gen = None
        for line in out.splitlines():
            if "MUTANTS GENERATED" in line:
                gen = int(line.split()[0])
                break
        self.assertIsNotNone(gen)
        self.assertTrue(gen > 0)

    def test_tact(self):
        self._run_mutate("foo.tact", "tact", "tact.rules")

    def test_func(self):
        self._run_mutate("foo.fc", "func", "func.rules")

    def test_tolk(self):
        self._run_mutate("foo.tolk", "tolk", "tolk.rules")
