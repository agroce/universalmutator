from __future__ import print_function

import os
import shutil
import subprocess
import sys
from unittest import TestCase


class TestSolidityExample(TestCase):
    def setUp(self):
        os.chdir("examples")
        repo_root = os.path.abspath("..")
        self.subprocess_env = os.environ.copy()
        existing_pythonpath = self.subprocess_env.get("PYTHONPATH")
        if existing_pythonpath:
            self.subprocess_env["PYTHONPATH"] = repo_root + os.pathsep + existing_pythonpath
        else:
            self.subprocess_env["PYTHONPATH"] = repo_root
        self.mutant_dir = "solidity_mutants"
        self.output_file = "mutate.sol.out"

    def tearDown(self):
        if os.path.exists(self.output_file):
            try:
                os.remove(self.output_file)
            except Exception:
                pass
        if os.path.isdir(self.mutant_dir):
            shutil.rmtree(self.mutant_dir, ignore_errors=True)
        os.chdir("..")

    def test_solidity_example(self):
        with open(self.output_file, "w") as f:
            r = subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "universalmutator.genmutants",
                    "foo.sol",
                    "--noCheck",
                    "--mutantDir",
                    self.mutant_dir,
                ],
                stdout=f,
                stderr=f,
                env=self.subprocess_env,
            )
        self.assertEqual(r, 0)

        with open(self.output_file, "r") as f:
            out = f.read()

        self.assertIn("MUTANTS GENERATED", out)
        self.assertIn("VALID MUTANTS", out)

        generated_count = None
        valid_count = None
        for line in out.splitlines():
            parts = line.split()
            if len(parts) == 5 and parts[1:] == ["MUTANTS", "GENERATED", "BY", "RULES"]:
                generated_count = int(parts[0])
            if len(parts) == 3 and parts[1:] == ["VALID", "MUTANTS"]:
                valid_count = int(parts[0])

        self.assertIsNotNone(generated_count)
        self.assertIsNotNone(valid_count)
        self.assertTrue(generated_count > 0)
        self.assertTrue(valid_count > 0)
