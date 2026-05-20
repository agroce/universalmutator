from __future__ import print_function
import os
import subprocess
import sys
from unittest import TestCase

CANONICAL_FOO = """from __future__ import print_function

def myfunction(x):
    if x < 6:
        print(x)
        x = 20
    while x > 10:
        x -= 1
    return x

def main():
    y = 4
    v = myfunction(y)
    assert v==10

if __name__ == '__main__':
    main()
"""


class TestFooExample(TestCase):
    def setUp(self):
        os.chdir("examples")
        repo_root = os.path.abspath("..")
        self.subprocess_env = os.environ.copy()
        existing_pythonpath = self.subprocess_env.get("PYTHONPATH")
        if existing_pythonpath:
            self.subprocess_env["PYTHONPATH"] = repo_root + os.pathsep + existing_pythonpath
        else:
            self.subprocess_env["PYTHONPATH"] = repo_root
        with open("foo.py", "r") as f:
            self.original_foo = f.read()
        with open("foo.py", "w") as f:
            f.write(CANONICAL_FOO)

    def tearDown(self):
        with open("foo.py", "w") as f:
            f.write(self.original_foo)
        os.chdir("..")

    def test_foo_example(self):
        with open("mutate.out", 'w') as f:
            r = subprocess.call(
                [sys.executable, "-m", "universalmutator.genmutants", "foo.py"],
                stdout=f,
                stderr=f,
                env=self.subprocess_env,
            )
        with open("mutate.out", 'r') as f:
            for line in f:
                print(line, end=" ")
        self.assertEqual(r, 0)

        with open("mutate.out", 'r') as f:
            validCount = -1
            invalidCount = -1
            redundantCount = -1
            for line in f:
                if "VALID MUTANTS" in line:
                    validCount = int(line.split()[0])
                if "INVALID MUTANTS" in line:
                    invalidCount = int(line.split()[0])
                if "REDUNDANT MUTANTS" in line:
                    redundantCount = int(line.split()[0])
            self.assertTrue(validCount > 20)
            self.assertTrue(invalidCount > 10)
            self.assertTrue(redundantCount > 1)

        with open("analyze.out", 'w') as f:
            r = subprocess.call(
                [sys.executable, "-m", "universalmutator.analyze", "foo.py", 'python MUTANT', "--verbose", "--timeout", "5"],
                stdout=f,
                stderr=f,
                env=self.subprocess_env,
            )
        with open("analyze.out", 'r') as f:
            for line in f:
                print(line, end=" ")
        self.assertEqual(r, 0)

        with open("analyze.out", 'r') as f:
            lineCount = 0
            notKilledCount = 0
            killedCount = 0
            mutationScore = -1
            for line in f:
                lineCount += 1
                if "NOT KILLED" in line:
                    notKilledCount += 1
                elif "KILLED" in line:
                    killedCount += 1
                if "MUTATION SCORE" in line:
                    mutationScore = float(line.split()[2])
            self.assertTrue(lineCount > validCount)
            self.assertTrue(killedCount > 0)
            self.assertTrue(notKilledCount > 0)
            self.assertTrue(mutationScore > 0.0)
            self.assertTrue(mutationScore < 1.0)

        with open("prioritize.out", 'w') as f:
            r = subprocess.call(
                [sys.executable, "-m", "universalmutator.prioritize", "notkilled.txt", "notkilled_prioritized.txt"],
                stdout=f,
                stderr=f,
                env=self.subprocess_env,
            )
        self.assertEqual(r, 0)
