from __future__ import print_function
import os
import subprocess
from unittest import TestCase


class TestFooExample(TestCase):
    def setUp(self):
        os.chdir("examples")

    def tearDown(self):
        os.chdir("..")

    def test_foo_example(self):
        with open("mutate.out", 'w') as f:
            r = subprocess.call(["mutate", "foo.py"], stdout=f, stderr=f)
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
                ["analyze_mutants", "foo.py", 'python foo.py', "--verbose", "--timeout", "5"],
                stdout=f, stderr=f)
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
